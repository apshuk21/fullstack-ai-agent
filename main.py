import os
from dotenv import load_dotenv
from openai import OpenAI
from file_utils import createFile, is_valid_path
from prompts import system_prompt
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



    
    


