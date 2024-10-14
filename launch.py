import subprocess
import os
from pathlib import Path
import sys

try:
    import streamlit
except ModuleNotFoundError:
    print(
        "Streamlit not found. ",
        "Make sure your virtual environment is activated or install streamlit with\n\n\t",
        "pip install streamlit",
    )
    sys.exit()

cwd = Path(os.getcwd())
entry_point = Path("./app/Welcome.py")

if os.path.exists(cwd / entry_point):
    subprocess.run(["streamlit", "run", "app/Welcome.py"])
else:
    print(f"You are in {os.getcwd()}. Please navigate to the project root `magpylib`.")
