import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_path,file_path))
    if abs_file_path.startswith(abs_path):
        if os.path.exists(abs_path):
            pass
        else:
            os.makedirs(abs_path)
        try:
            with open(abs_file_path, mode='w') as write_file:
                write_file.write(content)
        except Exception:
            return f"Error:"
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="This is the file path of the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="This is the content to write to the file."
            )

        }
    )
)