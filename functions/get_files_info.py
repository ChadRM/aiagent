import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_path = os.path.abspath(working_directory)
    if abs_working_directory.startswith(abs_path):
        if os.path.isdir(abs_working_directory):
            listdir = os.listdir(abs_working_directory)
            # if abs_working_directory == abs_path:
                # output = "Results for current directory:\n"
            # else:
                # output = f"Results for '{directory}' directory:\n"
            output = ""
            for item in listdir:
                fsize = os.path.getsize(abs_working_directory + "/" + item)
                isdir = not os.path.isfile(abs_working_directory + "/" + item)
                output += f" - {item}: file_size={fsize} bytes, is_dir={isdir}\n"
            return output
        else:
            return f'Error: "{directory}" is not a directory'
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)