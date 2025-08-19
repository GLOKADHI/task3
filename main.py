import customtkinter as ctk
import threading
import time
import requests
from PIL import Image
import os
from datetime import datetime
import textwrap

# ===============================
# CONFIG
# ===============================
ctk.set_appearance_mode("light")  # default mode
ctk.set_default_color_theme("blue")  # theme

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"  # your Ollama model name

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Create unique log file for this session
log_filename = os.path.join(LOGS_DIR, f"chat_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

# ===============================
# Helper: Format Ollama output for readability
# ===============================
def format_ollama_output(raw_text, width=80):
    # Replace escaped newlines with actual newlines
    cleaned = raw_text.replace("\\n", "\n")
    # Wrap text neatly for readability
    wrapped_lines = []
    for paragraph in cleaned.split("\n\n"):
        paragraph = paragraph.strip()
        if paragraph:
            wrapped_lines.append("\n".join(textwrap.wrap(paragraph, width=width)))
    return "\n\n".join(wrapped_lines)

# ===============================
# CHATBOT CLASS
# ===============================
class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ollama Chatbot")
        self.geometry("600x500")

        # Track light/dark
        self.is_dark_mode = False

        # Frames
        self.chat_frame = ctk.CTkFrame(self, corner_radius=10)
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_area = ctk.CTkTextbox(
            self.chat_frame,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 12)
        )
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        self.user_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message...",
            font=("Segoe UI", 12)
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(5, 2), pady=5)

        # Load Send icon
        send_img = Image.open("send.png").resize((30, 30))
        self.send_icon = ctk.CTkImage(light_image=send_img, dark_image=send_img, size=(30, 30))

        self.send_button = ctk.CTkButton(
            self.input_frame,
            image=self.send_icon,
            text="",
            width=40,
            command=self.send_message
        )
        self.send_button.pack(side="left", padx=(2, 5), pady=5)

        # Loading label
        self.loading_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 11))
        self.loading_label.pack(pady=5)

        # Mode toggle
        self.toggle_button = ctk.CTkButton(self, text="🌙 Dark Mode", command=self.toggle_mode)
        self.toggle_button.pack(pady=(0, 10))

    # ===============================
    # MODE TOGGLE
    # ===============================
    def toggle_mode(self):
        if self.is_dark_mode:
            ctk.set_appearance_mode("light")
            self.toggle_button.configure(text="🌙 Dark Mode")
            self.is_dark_mode = False
        else:
            ctk.set_appearance_mode("dark")
            self.toggle_button.configure(text="☀ Light Mode")
            self.is_dark_mode = True

    # ===============================
    # LOADING ANIMATION
    # ===============================
    def show_loading(self):
        dots = ["", ".", "..", "..."]
        idx = 0
        while self.loading_active:
            self.loading_label.configure(text=f"Fetching from Ollama{dots[idx]}")
            idx = (idx + 1) % len(dots)
            time.sleep(0.4)

    # ===============================
    # SEND MESSAGE
    # ===============================
    def send_message(self):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            return
        self.append_message("You", user_msg)
        self.save_to_log("You", user_msg)
        self.user_input.delete(0, "end")

        # Start loading animation
        self.loading_active = True
        threading.Thread(target=self.show_loading, daemon=True).start()

        # Fetch from Ollama in thread
        threading.Thread(target=self.fetch_ollama, args=(user_msg,), daemon=True).start()

    def fetch_ollama(self, prompt):
        try:
            payload = {"model": MODEL, "prompt": prompt}
            response = requests.post(OLLAMA_URL, json=payload, stream=True)
            response.raise_for_status()

            output = ""
            total_bytes = 0
            received_bytes = 0

            if "Content-Length" in response.headers:
                try:
                    total_bytes = int(response.headers["Content-Length"])
                except:
                    total_bytes = 0

            for line in response.iter_lines():
                if line:
                    try:
                        data = line.decode("utf-8", errors="ignore")
                        received_bytes += len(data)

                        if total_bytes > 0:
                            percent = int((received_bytes / total_bytes) * 100)
                            self.loading_label.configure(text=f"Fetching from Ollama... {percent}%")

                        if '"response":"' in data:
                            text_piece = data.split('"response":"')[1].split('"')[0]
                            output += text_piece
                    except:
                        pass
        except Exception as e:
            output = f"[Error] {e}"

        self.loading_active = False
        self.loading_label.configure(text="")

        # Format Ollama reply before displaying
        formatted_output = format_ollama_output(output, width=70)

        self.append_message("Ollama", formatted_output)
        self.save_to_log("Ollama", formatted_output)

    # ===============================
    # APPEND MESSAGE
    # ===============================
    def append_message(self, sender, message):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", f"{sender}: {message}\n\n")
        self.text_area.configure(state="disabled")
        self.text_area.see("end")

    # ===============================
    # SAVE TO LOG
    # ===============================
    def save_to_log(self, sender, message):
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(f"{sender}: {message}\n\n")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
