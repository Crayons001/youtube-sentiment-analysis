from app.youtube_operations import get_video_title

video_url = "https://www.youtube.com/watch?v=-O9NMdvWmE8" 
video_title = get_video_title(video_url)

print(video_title)

