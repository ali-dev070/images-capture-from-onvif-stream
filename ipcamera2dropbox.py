'''
One script to capture images, zip the yesterday images, and upload it to dropbox.
Not in use yet
'''

import subprocess
import time
import os

import zipfile
import dropbox

ACCESS_TOKEN = 'api_access_token'

def authenticate_dropbox():
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        account_info = dbx.users_get_current_account()
        print(f"Successfully connected to Dropbox account: {account_info.name.display_name}")
        return dbx
    except dropbox.exceptions.AuthError:
        print("Failed to authenticate. Please check your access token.")
        return None

def upload_file_to_dropbox(dbx, local_file_path, dropbox_path):
    with open(local_file_path, "rb") as file:
        try:
            dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
            print(f"Uploaded {local_file_path} to Dropbox as {dropbox_path}")
        except dropbox.exceptions.ApiError as e:
            print(f"Error uploading {local_file_path} to Dropbox: {e}")


if __name__ == "__main__":
    #* Capturing the RTSP stream and saving a frame as an image every ~30seconds

    # Replace with your RTSP stream URL
    rtsp_url = "rtsp://192.168.20.16:554/onvif1"

    # Set image capture interval (in seconds)
    capture_interval = 30
    dbx = authenticate_dropbox()

    while True:
        try:
            # Path to save the captured images
            image_path = "images/" + time.strftime('%Y-%m-%d')
            if not os.path.exists(image_path):
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
                    upload_file_to_dropbox(dbx, f"images/{filename}", f"/{filename}")

                # create folder for today
                os.mkdir(image_path)
            
            image_name = "image_" + time.strftime('%H.%M.%S')
            
            # FFmpeg command to capture a single image
            ffmpeg_command = [
                "ffmpeg",
                "-rtsp_transport", "udp",  # Specify TCP for RTSP transport
                "-i", rtsp_url,
                "-ss", "00:00:01",
                "-vframes", "1",  # Capture only one frame
                "-f", "image2",  # Output format as image2
                f"{image_path}/{image_name}.jpg"
            ]

            # Execute the FFmpeg command
            subprocess.run(ffmpeg_command, check=True)

            print(f"Image captured at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        except subprocess.CalledProcessError as e:
            print(f"Error capturing image: {e}")

        time.sleep(capture_interval)


