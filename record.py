from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput, PyavOutput
from picamera2 import Picamera2
from datetime import datetime
import time
import subprocess
import os

# Directory to save and play videos from
OUTPUT_DIR = "/home/hackathonteam_s/Documents/"

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

prev_video = None
player_process = None

# Optional: Start camera sensor ahead of time without a preview window
picam2.start()

encoder = H264Encoder(bitrate=10000000)

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{OUTPUT_DIR}video_{timestamp}.mp4"
    
    # 1. Handle previous video playback
    if player_process and player_process.poll() is None:
        player_process.terminate()  # Close the old player window if still open
        
    if prev_video and os.path.exists(prev_video):
        # Play the previous video in the background using vlc
        player_process = subprocess.Popen(["cvlc", "--play-and-exit", prev_video], env={"DISPLAY": ":0"})

    # 2. Record the new video segment
    output = FfmpegOutput(filename, audio=False)
    
    picam2.start_recording(encoder, output)
    time.sleep(65)  # Records for ~65 seconds (covers your 1-minute chunk target)
    picam2.stop_recording()
    
    # 3. Store current video as previous for the next iteration
    prev_video = filename
    time.sleep(1)