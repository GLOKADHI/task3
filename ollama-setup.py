import subprocess
import platform
import shutil
import os

def is_ollama_installed():
    """Check if Ollama is already installed"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Ollama is already installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_ollama():
    """Install Ollama depending on OS"""
    system = platform.system()

    if is_ollama_installed():
        return

    if system == "Linux" or system == "Darwin":  # macOS uses same script
        print("Installing Ollama via curl...")
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)

    elif system == "Windows":
        print("Installing Ollama on Windows...")
        url = "https://ollama.com/download/OllamaSetup.exe"
        installer = "OllamaSetup.exe"

        # Download installer using PowerShell
        subprocess.run(
            f"powershell -Command \"Invoke-WebRequest -Uri {url} -OutFile {installer}\"",
            shell=True,
            check=True
        )

        # Run silent installer
        subprocess.run(f"{installer} /S", shell=True, check=True)

        print("Ollama installed successfully. You may need to restart your terminal.")

    else:
        raise Exception(f"Unsupported OS: {system}")


# Example usage:
if __name__ == "__main__":
    install_ollama()
    if is_ollama_installed():
        print("✅ Ollama is ready to use.")
    else:
        print("❌ Ollama installation failed.")
