'''
zip the yesterday's images and upload the zip to dropbox.
create a cron job to schedule running this script.
e.g. to run it everyday 1am
    * 1 * * * python3 /path-to-this-script/zipAndUploadToDropbox.py
'''
import time
import os

import zipfile
import dropbox

APP_KEY = "client-key"
APP_SECRET = "client-secret"
REFRESH_TOKEN = "refresh-token"

def authenticate_dropbox():
    try:
        dbx = dropbox.Dropbox(
            app_key = APP_KEY,
            app_secret = APP_SECRET,
            oauth2_refresh_token = REFRESH_TOKEN
        )
        return dbx
    except dropbox.exceptions.AuthError:
        print("Failed to authenticate. Please check your access token.")
        return None

def upload_file_to_dropbox(dbx, local_file_path, dropbox_path):
    with open(local_file_path, "rb") as file:
        try:
            dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            print(f"Uploaded {local_file_path} to Dropbox as {dropbox_path}")
            return True
        except dropbox.exceptions.ApiError as e:
            print(f"Error uploading {local_file_path} to Dropbox: {e}")
            return False


if __name__ == "__main__":

    dbx = authenticate_dropbox()

    try:
        # zip and send previous day's folder by email
        previous_day = "images/" + time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
        
        # Create a zip file of the folder
        with zipfile.ZipFile(previous_day + ".zip", "w", zipfile.ZIP_DEFLATED) as zip_ref:
            for root, folders, files in os.walk(previous_day):
                for file in files:
                    zip_ref.write(os.path.join(root, file))
        
        filename = f"{os.path.basename(previous_day)}.zip"
        
        if dbx:
            # Example: Uploading a file to Dropbox
            uploaded = upload_file_to_dropbox(dbx, f"images/{filename}", f"/{filename}")

            if uploaded:
                os.remove(f"images/{filename}")

    except Exception as e:
        print(f"Error uploading files to dropbox: {e}")

