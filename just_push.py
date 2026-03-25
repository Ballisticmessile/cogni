import os
import subprocess
os.chdir(r"C:\Users\samruddhi\Desktop\cogni")
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\Program Files\Git\bin\git.exe"

result = subprocess.run([r"C:\Program Files\Git\bin\git.exe", "push", "-u", "origin", "main", "-f"], 
                       capture_output=True, text=True, timeout=120)
print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn Code: {result.returncode}")
