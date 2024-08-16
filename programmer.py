import subprocess
import os
import sys
import ollama
modelSelected = "llama3.1"

def compile_and_run_cpp(cpp_code): 
    output_binary = "Binary"   
    # Write the C++ code to a file
    cpp_file = 'temp.cpp'
    with open(cpp_file, 'w') as file:
        file.write(cpp_code)
    
    # Compile the C++ code
    compile_command = f'g++ {cpp_file} -o {output_binary}'
    compile_process = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
    
    if compile_process.returncode != 0:
        print("Compilation failed:")
        print(compile_process.stderr)
        return
    
    print("Compilation successful")
    
    # Execute the binary
    execute_command = f'./{output_binary}'
    execute_process = subprocess.run(execute_command, shell=True, capture_output=True, text=True)
    
    if execute_process.returncode != 0:
        print("Execution failed:")
        print(execute_process.stderr)
        return
    
    print("Execution output:")
    print(execute_process.stdout)




def LLMToCPP(userQuery):
    
    messages = [
        {
            'role': 'system',
            'content': f'You are a C++ expert and generate responses in C++ that will be compiled by the gcc compiler. Please show only C++ code with no comments'
        },
        {
            'role': 'user',
            'content': f'{userQuery}'
        }
    ]
    response = ollama.chat(model=modelSelected, messages=messages)
    return response['message']['content']


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: compile_and_run_cpp.py <query>")
        sys.exit(1)

    cpp_code = LLMToCPP(sys.argv[1])
    compile_and_run_cpp(cpp_code)
    
    # Cleanup
    os.remove('temp.cpp')
