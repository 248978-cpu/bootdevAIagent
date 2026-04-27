import os
from config import max_file_length
from google.genai import types

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(os.path.abspath(target_file)) as f:
        file_string = f.read(max_file_length)
        if f.read(1):
            file_string += f'[...File "{file_path}" truncated at {max_file_length} characters]'
    return file_string
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="allows you to read the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file path allows you to get access to the file",
            ),
        },
        required=["file_path"],
    ),
)
    