# images-capture-from-onvif-stream
Python script to use ffmpeg and capture images (frames) from onvif (RTSP) stream

It is assumed that ffmpeg and python is installed.

if on linux:
sudo apt update
sudo apt install ffmpeg
sudo apt install python3-dev python3-pip
pip install ffmpeg-python



folder should have images folder before running the script
replate "path-to-onvif-stream" with actual stream url.

to run script in background forever:
nohup python3 ipcamera.py > /dev/null 2>&1 & disown