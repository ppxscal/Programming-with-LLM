import os
import multiprocessing

def process_file(file_path):
    content = ""
    with open(file_path, 'r') as infile:
        content = f"--- {file_path} ---\n" + infile.read() + "\n\n"
    return content

def combine_files(args):
    folder_path, output_file, num_processes = args
    extensions = ['.py', '.js', '.ts', '.md', '.txt']
    exclude_dirs = {'node_modules', 'venv', '__pycache__'}

    file_paths = []
    for dirpath, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(dirpath, file))

    with multiprocessing.Pool(num_processes) as pool:
        file_contents = pool.map(process_file, file_paths)

    with open(output_file, 'w') as outfile:
        outfile.writelines(file_contents)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    output_file = "combined_output.txt"
    num_processes = 4
    combine_files((folder_path, output_file, num_processes))