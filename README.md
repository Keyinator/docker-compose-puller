# docker-compose-puller
Utility to download a remote docker-compose.yml file for updating purposes

## Arguments

Name | Description | Default
:--|:--|:--
download_path | The url to download the docker-compose.yml file from | ``https://raw.githubusercontent.com/example/docker-compose/main/docker-compose.yml``
compose_file_path | Path of the file to update | ``./docker-compose.yml``
backup_file_path | Path of the backup | ``./docker-compose.yml.bck``
update_regex | Regex to determine the version of respective docker-compose.yml files | ``image: [\w.\-/]*:([\w.\-/]*)``
show-diff | Whether to show the difference of local and remote | ``True``
env_file_path | Path of the environment file | ``­`` = disabled<br />(activated example: ``./.env``)
env_version_variable | Variable that stores the current version in your environment file. | ``version``

## Usage

Adjust the call to ``docker-compose-puller.py`` or update default values within.

## Doing

This script will do the following:

- Download the docker-compose.yml file from ``download_path``
- Show current and new version 
  - Display your current version from ``compose_file_path`` searched using the regex ``update_regex``
  - Display your new version from ``download_path`` searched using the regex ``update_regex``
- Ask for confirmation to update
- Show diffs if ``show-diff`` is set to True
  - Asks for confirmation
- Update files accordingly
  - Move ``compose_file_path`` into ``backup_file_path``
  - Save ``download_path`` to ``compose_file_path``
  - Update the variable ``update_regex`` in ``env_file_path`` to new version