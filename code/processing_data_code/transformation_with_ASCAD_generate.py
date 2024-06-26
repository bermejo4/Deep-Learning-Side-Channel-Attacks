import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
ASCAD_generate_path = os.getenv("ASCAD_GENERATE_PATH")
params_folder_path = os.getenv("PARAMS_FOLDER")

param_files = [f for f in os.listdir(params_folder_path) if os.path.isfile(os.path.join(params_folder_path, f))]

# Iteration through each file in the directory
for param_file in param_files:
    print(f"Ejecutando ASCAD_generate.py con {param_file}")
    result = subprocess.run(
        ["python3", ASCAD_generate_path, os.path.join(params_folder_path, param_file)],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
