# images-capture-from-onvif-stream
Python script to use ffmpeg and capture images (frames) from onvif (RTSP) stream.

It is assumed that ffmpeg and python are installed.

### Installation on linux
sudo apt update

sudo apt install ffmpeg

sudo apt install python3-dev python3-pip

pip install ffmpeg-python

### Installation on Windows
- download and install python and setup the path in environment variables, accordingly.
- download and install ffmpeg and setup the path in environment variables, accordingly.
- install the ffmpeg library in Python

### Note
- folder should have images folder before running the script.
- replace "path-to-onvif-stream" with actual stream url in the script.

### To run script in background forever in linux:
nohup python3 ipcamera.py > /dev/null 2>&1 & disown

### To run the cron job everyday at 1am
crontab -e

**Then add following cron job to the tab:**
* * 1 * * * python3 zipAndUploadToDropbox.py >> cronjob_logs.log 2>&1