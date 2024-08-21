import subprocess
import sys
import ollama
import re

modelSelected = "llama3.1"

def remove_quotes_and_comments(code):
    # Remove single and triple quotes and any following text (comments)
    #pattern = r"(?:'''(?:.|\n)*?'''|\"\"\"(?:.|\n)*?\"\"\"|#.*?$|'(?:\\.|[^'])*'|\"(?:\\.|[^\"])*\")"
    cleaned_code = re.sub(r'`', '', code)

    return cleaned_code

def run_bash(bash_code): 
    
    bash_file = 'temp.sh'
    with open(bash_file, 'w') as file:
        file.write(bash_code)
    
    process = subprocess.Popen(["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=bash_code)
    print(stdout)
    print(stderr)

    # compile_command = f'{bash_code}'
    # compile_process = subprocess.run(compile_command)
    
    # if compile_process.returncode != 0:
    #     print(compile_process.stderr)
    #     return
    
    # print("Compilation successful")

def LLMToBash(userQuery):
    messages = [
        {
            'role': 'system',
            'content': 'You are a linux bash expert and generate responses in bash that will run on an Ubuntu system. No comments or additional commentary. Just plain bash'
        },
        {
            'role': 'user',
            'content': userQuery
        }
    ]
    response = ollama.chat(model=modelSelected, messages=messages)
    return response['message']['content']

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: programmer <query>")
        sys.exit(1)

    bash_code = LLMToBash(sys.argv[1])
    #cpp_code=remove_quotes_and_comments(cpp_code)
    #cleaned_text = re.sub(r"'''", "", cpp_code)

    #print(cleaned_text)
    run_bash(remove_quotes_and_comments(bash_code))
