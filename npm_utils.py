# Check the Node and npm status
import subprocess
import os
from file_utils import is_valid_path, is_directory_exists as is_dir



def check_node_status():
    try:
        node_version = subprocess.check_output(['node', '-v']).decode('utf-8').strip()
        npm_version = subprocess.check_output(['npm', '-v']).decode('utf-8').strip()
        return {"node": node_version, "npm": npm_version}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}


# Check the project path

# Check the project name in the current directory, return false if it already exists.



def is_dir(path):
    return os.path.isdir(path)

def create_vite_project(**projectDetails):
    projectName = projectDetails.get("project_name", "smart-react-app")
    projectPath = projectDetails.get("project_path", ".")
    projectTechStack = projectDetails.get("project_tech_stack", "javascript")
    fullProjectPath = f"{projectPath}/{projectName}"


    if not is_dir(projectPath):
        print(f"❌ Invalid project path: {projectPath}")
        return {"error": f"Invalid project path: {projectPath}"}

    # Step 1️⃣: Create the project directory and install Vite locally
    try:
        os.makedirs(fullProjectPath, exist_ok=True)  # Ensure directory exists
        subprocess.run(["npm", "init", "-y"], check=True, cwd=fullProjectPath)  # Initialize npm in the directory
        subprocess.run(["npm", "install", "vite"], check=True, cwd=fullProjectPath)  # Install Vite locally

        # Step 2️⃣: Run the Vite project creation command inside the directory
        template = "react-ts" if projectTechStack.lower() == "typescript" else "react"
        subprocess.run(["npx", "vite", "create", "--template", template, "-y"], check=True, cwd=fullProjectPath)

        return {"success": f"✅ Project '{projectName}' created successfully at '{projectPath}' with {projectTechStack}."}
    
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}
