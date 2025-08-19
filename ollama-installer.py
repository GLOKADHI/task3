import os
import subprocess
import platform

def install_ollama_local():
    if platform.system() != "Windows":
        raise Exception("This script is only for Windows!")

    # Directory where this .py file is located
    root_dir = os.path.dirname(os.path.abspath(__file__))
    installer = os.path.join(root_dir, "OllamaSetup.exe")

    # Download Ollama installer if not present
    if not os.path.exists(installer):
        print("Downloading Ollama installer...")
        url = "https://ollama.com/download/OllamaSetup.exe"
        subprocess.run(
            f"powershell -Command \"Invoke-WebRequest -Uri {url} -OutFile {installer}\"",
            shell=True,
            check=True
        )
    else:
        print("Installer already exists.")

    # Run silent install into root_dir
    print(f"Installing Ollama into: {root_dir}")
    install_cmd = f"\"{installer}\" /S /D={root_dir}"
    subprocess.run(install_cmd, shell=True, check=True)

    print("✅ Ollama installation completed in local root directory.")

if __name__ == "__main__":
    install_ollama_local()
