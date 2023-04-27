import os
import sqlite3


def grab_clipboard_content(file_path):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()
    query = "SELECT ClipboardPayload FROM ActivityOperation WHERE ClipboardPayload is not null"
    cursor.execute(query)

    all_data = cursor.fetchall()

    cursor.close()
    con.close()
    return all_data


def main():
    full_path = os.path.join(os.environ["LOCALAPPDATA"], "ConnectedDevicesPlatform")
    if os.path.exists(full_path):
        file_system_entries = os.listdir(full_path)
        dirs_to_scan = []
        db_files = []
        clipboard_data = []

        # scanning for folders
        for file in file_system_entries:
            dirs_to_scan.append(os.path.join(full_path, file))

        # search for db files
        for directory in dirs_to_scan:
            try:
                found_files = os.listdir(directory)
                for found_file in found_files:
                    if found_file.endswith("ActivitiesCache.db"):
                        db_files.append(os.path.join(directory, found_file))
            except:
                pass

        # read clipboard content from sqlite db files
        for db_file in db_files:
            clipboard_data.append(grab_clipboard_content(db_file))

        print(clipboard_data)


main()
