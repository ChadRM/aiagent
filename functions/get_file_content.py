from config import BYTE_LIMIT
import os
from google.genai import types

numbytes = int(BYTE_LIMIT)
def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_path,file_path))
    if abs_file_path.startswith(abs_path):
        if os.path.isfile(abs_file_path):
            output = ""
            try:
                with open(abs_file_path, mode='r') as read_file:
                    output += read_file.read(numbytes)
                if os.path.getsize(abs_file_path) > numbytes:
                    output += f"[...File \"{file_path}\" truncated at {BYTE_LIMIT} characters]"
                return output
            except Exception:
                return f"Error:"

        else:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a given file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path":types.Schema(
                type=types.Type.STRING,
                description="This is the file to get the content out of.",
            ),
        }
    )

)