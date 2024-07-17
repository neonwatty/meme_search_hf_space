import os
import requests

def download_file_from_github(repo_url, file_path, save_dir):
    raw_url = f"https://raw.githubusercontent.com/{repo_url}/main/{file_path}"
    response = requests.get(raw_url)
    
    if response.status_code == 200:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, os.path.basename(file_path))
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f"File downloaded successfully: {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def list_files_in_github_directory(owner, repo, directory_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{directory_path}"
    response = requests.get(url)
    
    if response.status_code == 200:
        files = response.json()
        names = []
        for file in files:
            names.append(file["name"])
        return names
    else:
        print(f"Failed to retrieve directory contents. Status code: {response.status_code}")


def collect_repo_file_names():
    owner = "neonwatty"            
    repo = "meme_search"           
    input_path = "/data/input"
    input_names = list_files_in_github_directory(owner, repo, input_path)

    db_path = "/data/dbs"
    db_names = list_files_in_github_directory(owner, repo, db_path)
    db_names = [v for v in db_names if ".db" in v or ".faiss" in v]
    return input_path, db_path, input_names, db_names

def check_directory_exists(directory_path):
    return os.path.isdir(directory_path)

def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory '{directory_path}' created successfully.")
    except OSError as error:
        print(f"Error creating directory '{directory_path}': {error}")

def check_files_in_directory(directory_path, file_list):
    missing_files = []
    for file_name in file_list:
        if not os.path.isfile(os.path.join(directory_path, file_name)):
            missing_files.append(file_name)
    return missing_files

def list_files_in_directory(directory_path):
    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return files
    except OSError as error:
        print(f"Error accessing directory '{directory_path}': {error}")
        return []
    
def delete_file(directory_path, file_name):
    try:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"File '{file_name}' deleted successfully.")
        else:
            print(f"File '{file_name}' does not exist in the directory '{directory_path}'.")
    except OSError as error:
        print(f"Error deleting file '{file_name}': {error}")
        
def pull_demo_data():
    repo_url = "neonwatty/meme_search"
    input_path, db_path, repo_input_names, repo_db_names = collect_repo_file_names()
    if not check_directory_exists("." + input_path):
        create_directory("." + input_path)
        for name in repo_input_names:
            file_path = input_path + "/" + name
            download_file_from_github(repo_url, file_path, "." + input_path)
    else:
        local_input_files = list_files_in_directory("." + input_path)
        input_files_to_pull = [item for item in repo_input_names if item not in local_input_files]
        input_files_to_delete = [item for item in local_input_files if item not in repo_input_names]

        for name in input_files_to_delete:
            delete_file("." + input_path, name)
        for name in input_files_to_pull:
            file_path = input_path + "/" + name
            download_file_from_github(repo_url, file_path, "." + input_path)
        
    if not check_directory_exists("." + db_path):
        create_directory("." + db_path)
        repo_url = "neonwatty/meme_search"
        for name in repo_db_names:
            file_path = db_path + "/" + name
            download_file_from_github(repo_url, file_path, "." + db_path)
    else:
        local_db_files = list_files_in_directory("." + db_path)
        db_files_to_pull = [item for item in repo_db_names if item not in local_db_files]
        db_files_to_delete = [item for item in local_db_files if item not in repo_db_names]
        for name in db_files_to_delete:
            delete_file("." + db_path, name)
        for name in db_files_to_pull:
            file_path = db_path + "/" + name
            download_file_from_github(repo_url, file_path, "." + db_path)