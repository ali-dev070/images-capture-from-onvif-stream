import subprocess
import time
import os

import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def send_zipped_folder_via_email(sender_email, sender_password, receiver_email, folder_path):
    """Sends all files in a specified folder as a compressed zip file via email.

    Args:
        sender_email (str): Email address of the sender.
        sender_password (str): Password for the sender's email account.
        receiver_email (str): Email address of the recipient.
        folder_path (str): Path to the folder containing the files to be compressed and emailed.
    """

    # Create a zip file of the folder
    with zipfile.ZipFile(folder_path + ".zip", "w", zipfile.ZIP_DEFLATED) as zip_ref:
        for root, folders, files in os.walk(folder_path):
            for file in files:
                zip_ref.write(os.path.join(root, file))

    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Compressed Files from " + folder_path

    # Attach the zip file
    with open(folder_path + ".zip", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(folder_path)}.zip",
        )
        message.attach(part)

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)
        

#* Capturing the RTSP stream and saving a frame as an image every ~30seconds
#*

# Replace with your RTSP stream URL. Change it according to your setup
rtsp_url = "rtsp://192.168.20.16:554/onvif1"

# Set image capture interval (in seconds)
capture_interval = 30

while True:
    try:
        # Path to save the captured images
        image_path = "images/" + time.strftime('%Y-%m-%d')
        if not os.path.exists(image_path):
            # zip and send previous day's folder by email
            previous_day = "images/" + time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))
            send_zipped_folder_via_email("your_email@gmail.com", "app_password", "receiver_email@gmail.com", previous_day)

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


