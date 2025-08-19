# 🤖 Ollama Chatbot

A simple AI chatbot powered by [Ollama](https://ollama.com) and Python.  
This project installs Ollama locally in your project folder (portable installation) and runs a chatbot through `main.py`.

---

## 📂 Project Structure
```
chatbot/
│── main.py               # Chatbot entry point
│── ollama_setup.py       # Prepares environment for Ollama
│── ollama_installer.py   # Downloads & installs Ollama in root
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```

---

## 🚀 Setup Instructions

Follow these steps **in order**:

1. **Run the Ollama setup script**  
   ```bash
   python ollama_setup.py
   ```
   *(prepares your project root for Ollama)*

2. **Run the Ollama installer**  
   ```bash
   python ollama_installer.py
   ```
   *(downloads & extracts Ollama files into the root folder)*

3. **Install required Python modules**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the chatbot**  
   ```bash
   python main.py
   ```

---

## 🛠 Requirements
- Windows 10/11, Linux, or macOS  
- Python 3.9+  
- Internet connection (to download Ollama & models)

---

## 💡 Notes
- On Windows, Ollama will be installed in the **same directory as your project root** (portable).  
- If you want to use additional models, run:  
  ```bash
  ollama pull llama2
  ```  
- To start Ollama manually (if needed):  
  ```bash
  ./ollama.exe serve
  ```

---

## 📜 License
This project is for educational purposes. You may modify and use it for your own projects.
