import subprocess

# 下载YouTube视频并提取音频为mp3
video_url = " "
output_audio = "audio.mp3"

# 使用yt-dlp下载并转换为mp3
subprocess.run([
    "yt-dlp",
    "-x",
    "--audio-format", "mp3",
    "-o", output_audio,
    video_url
], check=True)