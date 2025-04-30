import os
import sys
import shutil
import subprocess
from pathlib import Path
from urllib.request import urlretrieve

# Dependencies
DEPENDENCIES = [
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "ipykernel",
    "joblib",
    "streamlit",
]

URL = "https://raw.githubusercontent.com/utkarshg1/Iris-Deployment-Proj-9-am/refs/heads/main/notebook/iris.csv"


# Create folder structure and files
def create_folder_structure():
    print("📂 Creating folder structure and files...")
    os.makedirs("notebook", exist_ok=True)
    with open("notebook/model.ipynb", "w") as f:
        pass

    with open("requirements.txt", "w") as f:
        f.write("\n".join(DEPENDENCIES))

    with open("README.md", "w") as f:
        f.write("# Streamlit End to End ML Project\n")
        f.write("\n\n## Running setup.py\n")
        f.write("```bash\npython setup.py\n```\n")

        f.write("\n\n## Activate venv\n")
        f.write("\nLinux / Mac - \n```bash\nsource .venv/bin/activate\n```\n")
        f.write("\nWindows - \n```bash\n.venv\\Scripts\\activate\n```\n")

        f.write("\n\n## Running a streamlit app\n")
        f.write("Running streamlit app command\n")
        f.write("```bash\nstreamlit run main.py\n```")

    print("📂 Folder structure and files created.\n")


def download_file(url: str, out_path: str):
    try:
        print("📥 Downloading dataset...")
        filename = url.split("/")[-1]
        out_dir = Path(out_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        output = out_dir / filename
        print(f"Downloading {filename} to {output}")
        urlretrieve(url, filename=str(output))
        print(f"📥 File saved at {output}\n")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        sys.exit(1)


def venv_setup():
    try:
        print("🔼 Upgrading pip…")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--user", "--upgrade", "pip"],
            check=True,
        )

        if shutil.which("uv") is None:
            print("uv not found → installing uv…")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--user", "uv"], check=True
            )

        print("🚀 Initializing project with uv…")
        subprocess.run(["uv", "init", "."], check=True)
        print("🎉 Virtual environment ready!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ uv setup failed: {e}")
        sys.exit(1)


def install_requirements():
    try:
        print("🔧 Adding requirements to uv lock…")
        subprocess.run(["uv", "add", "-r", "requirements.txt"], check=True)

        print("🔄 Syncing uv environment…")
        subprocess.run(["uv", "sync"], check=True)
        print("🎉 Requirements installed!\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ uv install failed: {e}")
        sys.exit(1)


def change_branch_to_main():
    print("🌿 Renaming default branch to main...")
    os.system("git branch -M main")
    print("🌿 Branch renamed to main!\n")


# Run above functions
if __name__ == "__main__":
    if os.path.exists(".venv") and os.path.exists("pyproject.toml"):
        print(".venv and pyproject.toml already exist")
        print("❌ This script is for first time usage only")
        exit(0)

    print("🚀 Setting up project...")
    create_folder_structure()
    download_file(URL, "notebook")
    venv_setup()
    install_requirements()
    change_branch_to_main()
    print("💻 Activate venv with below command : ")
    print("Linux / Mac - source .venv/bin/activate")
    print("Windows - .venv\\Scripts\\activate")
    print("✅ Setup Complete ✅")
