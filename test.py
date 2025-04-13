from file_utils import createFile, is_valid_path, is_directory_exists
from npm_utils import create_vite_project


file_path = r"C:\Users\apshu\Desktop\Apoorva\2025\Gen-AI\Cohort\test.txt"
file_path_updated = r"C:\Users\apshu\Desktop\Apoorva\2025\React-2025".replace("\\", "/")
# print(file_path_updated)

# print(is_directory_exists(file_path_updated))

# print(createFile(file_path))

# print(createFile('sample.py'))

# Example Usage
create_vite_project(project_tech_stack="typescript", project_path=file_path_updated)