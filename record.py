from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
from datetime import datetime
import time
import subprocess
import os

# Directory where videos are saved
OUTPUT_DIR = "/home/hackathonteam_s/Documents/"

# Initialize Picamera2 for Raspberry Pi 5
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

prev_video = None
player_process = None

# Start the camera sensor (no preview window will open)
picam2.start()

# High-performance software encoder configuration optimized for Pi 5 CPU
encoder = H264Encoder(bitrate=10000000)

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{OUTPUT_DIR}video_{timestamp}.mp4"
    
    # 1. Close previous player instance if it's still running
    if player_process and player_process.poll() is None:
        player_process.terminate()
        
    # 2. Play the previous video in the background while recording the new one
    if prev_video and os.path.exists(prev_video):
        # Using cvlc (Command-line VLC) which integrates cleanly with Pi 5's desktop session
        player_process = subprocess.Popen(
            ["cvlc", "--play-and-exit", prev_video], 
            env={"DISPLAY": ":0"}
        )

    # 3. Record the new 1-minute video segment
    output = FfmpegOutput(filename, audio=False)
    
    print(f"Recording: {filename}")
    picam2.start_recording(encoder, output)
    time.sleep(65)  # Records for ~65 seconds per chunk
    picam2.stop_recording()
    
    # 4. Save current file reference for the next cycle
    prev_video = filename
    time.sleep(1)