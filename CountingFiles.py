import os

def list_files_in_folder(folder_path):
    files_list = []
    try:
        # Checking if the path is a valid directory
        if os.path.isdir(folder_path):
            files_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        else:
            print("The specified path is not a directory.")
    except OSError as e:
        print(f"Error: {e}")
    
    return files_list

# Replace 'folder_path' with the path to your desired folder
folder_path = '/path/to/your/folder'

files_in_folder = list_files_in_folder(folder_path)
print("Files in the folder:")
for file_name in files_in_folder:
    print(file_name)
