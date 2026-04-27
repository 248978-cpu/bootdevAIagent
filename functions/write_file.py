import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        f'Error: Cannot write to "{file_path}" as it is a directory'
    target_dir = os.path.dirname(target_file)
    os.makedirs(target_dir, mode=0o777, exist_ok=True)
    with open(os.path.abspath(target_file), mode='w') as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="allows you to make changes to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file path allows you to get access to the file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the things you want to write to a file",
                )
        },
        required=["file_path"],
    ),
)