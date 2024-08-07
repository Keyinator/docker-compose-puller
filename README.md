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

## Usage

Adjust the call to ``docker-compose-puller.py`` or update default values within.