import json
import os
import platform

import requests

map_platform_gecko_os = {
    "Darwin x86_64": "macos",
    "win32 x86_32": "win32",  # Need to be validated
    "win64 x86_64": "win64",  # Need to be validated
    "linux x86_32": "linux32",  # Need to be validated
    "linux2 x86_64": "linux64",  # Need to be validated
}


def get_latest_gecko_driver(all_platforms=False):
    """
    Gets the latest gecko drivers and place it on the bin/divers directory depending on the platform
    :return:
    """
    from zipfile import ZipFile
    import tarfile

    url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"

    drivers_directory = "."
    current_platform = f"{platform.system()} {platform.machine()}"

    current_gecko_os = map_platform_gecko_os.get(current_platform, current_platform)

    payload = {}
    files = {}
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    json_load = json.loads(response.text.encode('utf8'))

    gecko_release_info = {
        "release_version": json_load.get("tag_name"),
        "assets": {r["name"]: r["browser_download_url"] for r in json_load.get("assets")},
    }

    for k, v in gecko_release_info.get("assets").items():
        file_name = k
        os_version = k.replace(".tar.gz", "").replace(".zip", "").split("-")[-1]

        if all_platforms or os_version == current_gecko_os:

            driver_dir = f"{drivers_directory}/{os_version}".replace("/", os.sep)
            file = f"{driver_dir}{os.sep}{file_name}"

            if not os.path.isfile(file):

                receive = requests.get(v)
                if not os.path.isdir(driver_dir):
                    os.mkdir(driver_dir)

                with open(file, 'wb') as f:
                    f.write(receive.content)

                if file.endswith("tar.gz"):
                    with tarfile.open(file, "r:gz") as tar:
                        tar.extractall(driver_dir)
                else:
                    with ZipFile(file, 'r') as zipObj:
                        zipObj.extractall(driver_dir)
            else:
                print(f"gecko driver {gecko_release_info['release_version']} version already on path {driver_dir}")


if __name__ == "__main__":
    # For now only gecko driver will be downloaded
    get_latest_gecko_driver()
