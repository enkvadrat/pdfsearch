import os
from dotenv import load_dotenv
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

import config 

def download_files_from_folder(ctx, folder_url, local_path):
    folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    files = folder.files
    ctx.load(files)
    ctx.execute_query()

    # Get the list of existing files in the local directory
    existing_files = set(os.listdir(local_path))

    for file in files:
        if file.name.endswith('.pdf'):
            download_path = os.path.join(local_path, file.name)
            if file.name not in existing_files:
                try:
                    # File does not exist locally, proceed with download
                    with open(download_path, "wb") as local_file:
                        file_data = File.open_binary(ctx, file.serverRelativeUrl)
                        local_file.write(file_data.content)
                    print(f"Downloaded: {file.name}")
                except Exception as e:
                    print(f"Failed to download {file.name}: {e}")
            else:
                print(f"Skipped (already exists): {file.name}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    if not all([username, password]):
        raise ValueError("One or more environment variables are missing.")
    print("Environment variables loaded successfully.")

    # Authenticate using username and password
    site_url = config.site_url
    ctx_auth = AuthenticationContext(site_url)
    if not ctx_auth.acquire_token_for_user(username, password):
        raise ValueError("Authentication failed. Please check your username and password.")

    ctx = ClientContext(site_url, ctx_auth)
    print("Authentication successful.")

    # Setup paths
    sharepoint_folder_url = config.sharepoint_folder_url
    local_folder_path = config.certificate_folder
    os.makedirs(local_folder_path, exist_ok=True)

    # Start downloading files
    try:
        download_files_from_folder(ctx, sharepoint_folder_url, local_folder_path)
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
