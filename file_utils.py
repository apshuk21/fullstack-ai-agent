import os

def createFile(file_path):
    if is_valid_path(file_path)["result"]:
        try:
            with open(file_path, 'w') as f:
                f.write('')
            return f"File '{file_path}' created successfully."
        except Exception as e:
            return str(e)
    
def is_valid_path(file_path):
    # Check if the file alrady exists
    if os.path.exists(file_path):
        return {"result": False, "message": f"File '{file_path}' already exists."}
    
    # Extract the directory path
    directory_path = os.path.dirname(file_path)

    if not directory_path:
        return {"result": True, "message": "No directory path provided. Will create the file in the current working directory."}

    # Check if the path is valid
    if os.path.exists(directory_path):
        return {"result": True, "message": f"Directory '{directory_path}' exists."}
    else:
        return {"result": False, "message": f"Directory '{directory_path}' does not exists."}