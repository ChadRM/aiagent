from config import BYTE_LIMIT
import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_path,file_path))
    # print(abs_path)
    # print(abs_file_path)
    if abs_file_path.startswith(abs_path):
        if os.path.isfile(abs_file_path):
            if abs_file_path.endswith('.py'):
                output = subprocess.run(['python3',abs_file_path] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, 
                    timeout=30)
                if (output.stdout is None) and (output.stderr is None) and (output.returncode == 0):
                    return "No output produced"
                output_text = f"STDOUT: {output.stdout.decode() if output.stdout else f'No STDOUT'}\n"
                output_text += f"STDERR: {output.stderr.decode() if output.stderr else f'No STDERR'}"
                if output.returncode != 0:
                    output_text += f"Process exited with code {output.returncode}"
                return output_text
            else:
                 return f'Error: "{file_path}" is not a Python file.'
        else:
            return f'Error: File "{file_path}" not found.'
    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'