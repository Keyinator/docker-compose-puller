import os
import re
import shutil
import requests
import argparse
import difflib

def update_file(download_path, compose_file_path, backup_file_path, update_regex, env_file_path, env_version_variable, show_diff=False):
    """
    Updates a file based on the given parameters.

    Args:
        download_path: Path to the download directory (can be a URL).
        compose_file_path: Path to the compose file.
        backup_file_path: Path to the backup directory.
        update_regex: Regular expression for version extraction.
        show_diff (bool, optional): Whether to show the difference between files. Defaults to False.
        env_file_path (str, optional): Path to the environment file. Defaults to "./.env".
        env_version_variable (str, optional): The variable name in the environment file to update. 
                                               Defaults to "version".
    """
    # Download file (if URL)
    if download_path.startswith("http"):
        try:
            response = requests.get(download_path, stream=True)
            response.raise_for_status()

            # Create a temporary directory for download
            temp_dir = os.path.join(os.path.dirname(compose_file_path), '.updater_temp')
            os.makedirs(temp_dir, exist_ok=True)
            temp_file = os.path.join(temp_dir, 'temp.file')

            with open(temp_file, 'wb') as f:
                f.write(response.content)

            print("\nDownload complete.\n")

            # Read downloaded content from temporary file
            with open(temp_file, 'r') as f:
                download_file_content = f.read()

            # Clean up temporary file and directory
            os.remove(temp_file)
            shutil.rmtree(temp_dir)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return
    else:
        # Read file from local path
        with open(download_path, 'r') as f:
            download_file_content = f.read()

    # Load compose file
    with open(compose_file_path, 'r') as f:
        compose_file_content = f.read()

    # Extract versions
    compose_version = re.search(update_regex, compose_file_content)
    download_version = re.search(update_regex, download_file_content)

    if not compose_version or not download_version:
        print("Warning: Could not extract version from one or both files.")
        return

    # Compare versions
    if compose_version.group(1) == download_version.group(1):
        print("Versions are equal.")
        return

    print(f"Current version: {compose_version.group(1)}")
    print(f"New version: {download_version.group(1)}")

    # Show diff if requested or ask for confirmation
    if show_diff:
        if input("Update (will show diffs first)? (y/n): ").lower() != 'y':
            return

        print("\n")
        for line in difflib.unified_diff( 
        compose_file_content.splitlines(), download_file_content.splitlines(), fromfile='Original',  
        tofile='Updated', lineterm=''): 
            print(line) 

        if input("Update? (y/n): ").lower() != 'y':
            return
    else:
        if input("Update? (y/n): ").lower() != 'y':
            return

    print("\n")

    # Backup compose file
    shutil.copy2(compose_file_path, backup_file_path)

    # Update compose file
    with open(compose_file_path, 'w') as f:
        f.write(download_file_content)

    # Check if environment file path is set and adjust env_version_variable if needed
    if env_file_path!="":
        if(os.path.exists(env_file_path)):
            with open(env_file_path, "r") as f:
                env_content = f.read()

                # Check if the "env_version_variable" line is present
                if not any(line.startswith(f"{env_version_variable}=") for line in env_content.splitlines()):
                    print(f"Error: Variable '{env_version_variable}' is not defined in '{env_file_path}'. Exiting.")
                    return

                # Check the value assigned to "env_version_variable"
                for line in env_content.splitlines():
                    if line.startswith(f"{env_version_variable}="):
                        current_value = line.split("=", 1)[1]  
                        if current_value != compose_version.group(1):
                            print(f"Warning: Expected {compose_version.group(1)}, but found '{current_value}' in '{env_file_path}'. Still updating.")
                        break  # Stop after finding the variable
                
                # Update the value in the environment file
                with open(env_file_path, "w") as f:
                    for line in env_content.splitlines():
                        if line.startswith(f"{env_version_variable}="):
                            f.write(f"{env_version_variable}={download_version.group(1)}\n")
                        else:
                            f.write(line + "\n") 
        else:
            print(f"Warning: Environment file '{env_file_path}' not found.")

    print("Update complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update file based on version')
    parser.add_argument('--download_path', type=str, default='https://raw.githubusercontent.com/example/docker-compose/main/docker-compose.yml')
    parser.add_argument('--compose_file_path', type=str, default='./docker-compose.yml')
    parser.add_argument('--backup_file_path', type=str, default='./docker-compose.yml.bck')
    parser.add_argument('--update_regex', type=str, default=r'image: [\w.\-/]*:([\w.\-/]*)')
    parser.add_argument('--show-diff', action="store_true", help="Show the difference between files after update", default=True)
    parser.add_argument("--env_file_path", type=str, help="Path to the environment file", default="")
    parser.add_argument("--env_version_variable", type=str, help="The variable name in the environment file to update", default="version")
    args = parser.parse_args()

    update_file(
        args.download_path,
        args.compose_file_path,
        args.backup_file_path,
        args.update_regex,
        args.env_file_path,
        args.env_version_variable,
        show_diff=args.show_diff,
    )