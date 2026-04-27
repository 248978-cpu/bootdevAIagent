import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", target_file]
    if args is not None:
        command.extend(args)
    completed_process = subprocess.run(command, capture_output = True, text = True, timeout = 30)
    output = ""
    if completed_process.returncode != 0:
        output = f'Process exited with code {completed_process.returncode}'
        if completed_process.stdout == None and completed_process.stderr == None:
            output += f'No outpout produced'
    else:
        output = f'STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}'
    return output
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="allows you to run a python file (.py)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file path allows you to get access to the file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments.",
                items=types.Schema(
                    type=types.Type.STRING
                    )
                )
        },
        required=["file_path"],
    ),
)