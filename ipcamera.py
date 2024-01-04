import subprocess
import time
import os

# Replace with your RTSP stream URL
rtsp_url = "rtsp://path-to-onvif-stream"

# Set image capture interval (in seconds)
capture_interval = 30
    

while True:
    try:
        # Path to save the captured images
        image_path = "images/" + time.strftime('%Y-%m-%d')
        if not os.path.exists(image_path):
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
