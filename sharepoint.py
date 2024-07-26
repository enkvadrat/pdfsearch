import os
from dotenv import load_dotenv
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

import config 

site_url = config.site_url
sharepoint_folder_url = config.sharepoint_folder_url
local_folder_path = config.certificate_folder

# Load environment variables from .env file
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
if not all([username, password]):
    raise ValueError("One or more environment variables are missing.")
print("Environment variables loaded successfully.")

# Authenticate using username and password
ctx_auth = AuthenticationContext(site_url)
if not ctx_auth.acquire_token_for_user(username, password):
    raise ValueError("Authentication failed. Please check your username and password.")

ctx = ClientContext(site_url, ctx_auth)
print("Authentication successful.")

def download_files_from_folder(folder_url, local_path):
    folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

    for file in files:
        if file.name.endswith('.pdf'):
            download_path = os.path.join(local_path, file.name)
            if not os.path.exists(download_path):
                # File does not exist locally, proceed with download
                with open(download_path, "wb") as local_file:
                    file_data = File.open_binary(ctx, file.serverRelativeUrl)
                    local_file.write(file_data.content)
                print(f"Downloaded: {file.name}")
            else:
                print(f"Skipped (already exists): {file.name}")

    sub_folders = folder.folders
    ctx.load(sub_folders)
    ctx.execute_query()

    for sub_folder in sub_folders:
        sub_folder_local_path = os.path.join(local_path, sub_folder.name)
        os.makedirs(sub_folder_local_path, exist_ok=True)
        download_files_from_folder(sub_folder.serverRelativeUrl, sub_folder_local_path)

# Create local folder if it doesn't exist
os.makedirs(local_folder_path, exist_ok=True)

# Start downloading files
try:
    download_files_from_folder(sharepoint_folder_url, local_folder_path)
    print("Download completed!")
except Exception as e:
    print(f"An error occurred: {e}")
    raise
