import os
from dotenv import load_dotenv
from openai import OpenAI
from file_utils import createFile, is_valid_path
import json


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# print("openai_api_key", openai_api_key)
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = OpenAI(api_key=openai_api_key)
# print("client", client)

available_tools = {
    "createFile": {
        "function": createFile,
        "description": "Creates a file at the specified path."
    },
    "is_valid_path": {
        "function": is_valid_path,
        "description": "Checks if the specified path is valid."
    }
}


system_prompt = """
You are a helpful AI assistant. Your task is to assist the user with the file system operations.
If user asks for any other operations, you should politely decline and say that you are only capable of file system operations.
You work through a systematic process where you analyse the query, identify or observe the user's intent, plan the action using available tools and execute it.
You follow a step-by-step approach to answer the users's query using available set of tools.
Based on your analysis, select the relevant tool. Based on tool selection you perform an action and wait for the response.
Based on the response you get from the tool, you will provide a final answer to the user.

You can help the user with the following operations:
1. Create a file
2. Create a directory
3. Delete a file
4. Delete a directory
5. Create a React project using Vite
6. Create a React component
7. Add a new dependency to a React project

Rules:
1. Follow the output JSON format strictly.
2. Always perform one step at a time and wait for the next input.
3. Carefully analyse the user query and identify the intent.
4. Please analyse the user's request and observe the following rules:
    1. If the user asks for the creation of a new file OR directory, you should look out for the file path in the user's request. 
    2. If user does not provide the file path, you should ask the user to provide the file path.
    3. If user does not provide the file path, you should create the file in the current working directory.
    4. If user provides multiple file names, you should create all the files in the current working directory. 
    5. If user provides multiple file paths, you should create all the files in the respective directories.
    6. If the user provided directory path does not exist, you should create the directory first and then create the file in that directory.

Available tools:
1. createFile: Creates a file at the specified path.
2. is_valid_path: Checks if the specified path is valid.

Output format:
    {{  step: "This should be the output step.",
        "content": "The final output to the user.",
        "function": "The function name to be called",
        "filePath": "The file path to be passed to the function",    
    }}


Example 1:
User: Create a file named 'test.txt'.
Assistant: {{ "step": "analysis", "content": "The user wants to create a file named 'test.txt'." }}
Assistant: {{ "step": "observation", "content": "Check the file path. Find if it's a valid path OR not." }}
Assistant: {{ "step": "action", "function": "is_valid_path", "filePath": "test.txt" }}
Assistant: {{ "step": "observation", "content": "The file path is valid" }}
Assistant: {{ "step": "action", "function": "createFile", "filePath": "test.txt" }}
Assistant: {{ "step": "observation", "content": "The file 'test.txt' created successfully." }}
Assistant: {{ "step": "response", "content": "File 'test.txt' created successfully." }}

Example 2:
User: Create a file named '/dir/main/test.txt'.
Assistant: {{ "step": "analysis", "content": "The user wants to create a file named '/dir/main/test.txt'." }}
Assistant: {{ "step": "observation", "content": "Check the file path. Find if it's a valid path OR not." }}
Assistant: {{ "step": "action", "function": "is_valid_path", "filePath": "/dir/main/test.txt" }}
Assistant: {{ "step": "observation", "content": "The file path is invalid" }}
Assistant: {{ "step": "response", "content": "The user provided an invalid file path. I'm aborting the operation." }}

Example 3:
User: Can you please find some good restaurants in London.
Assistant: {{ "step": "analysis", "content": "The user wants to find some good restaurants in London." }}
Assistant: {{ "step": "observation", "content": "The user's query is not related to file operations. I'm aborting the operation" }}
Assistant: {{ "step": "response", "content": "I'm here to assist you with file system operations. How can I help you today with file operations?" }}

"""

messages = [{
    "role": "system",
    "content": system_prompt
}]

user_input = input("You >>: ")

messages.append({
    "role": "user",
    "content": user_input
})
    
while True:
    response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"}, 
            messages=messages,
            temperature=0.5,
        )
    assistant_response = response.choices[0].message.content
    parsed_response = json.loads(assistant_response)
    print("Assistant Response:", parsed_response)
    


    if parsed_response.get("step") == "analysis" or parsed_response.get("step") == "observation":
        print("🧠 >>:", parsed_response["content"])
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        continue
    
    elif parsed_response.get("step") == "action":
        function_name = parsed_response["function"]
        file_path = parsed_response["filePath"]
        print("🔦 >>:", f"Function name: {parsed_response["function"]} File path: {parsed_response["filePath"]}")

        if (function_name in available_tools):
            function = available_tools[function_name]["function"]

            if function_name == "is_valid_path":
                # Check if the path is valid
                result = function(file_path)
                if result.get("result"):
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "observation",
                            "content": "The file path is valid."
                        })
                    })
                else:
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "observation",
                            "content": "The file path is invalid."
                        })
                    })
            if function_name == "createFile":
                # Create the file
                result = function(file_path)
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "step": "observation",
                        "content": result
                    })
                })
            
    elif parsed_response.get("step") == "response":
        print("🤖 >>:", parsed_response["content"])
        break



    
    


