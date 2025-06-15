from pytube import YouTube

url = input("enter url video in youtube: ")

try:
    yt = YouTube(url)
    
    video_stream = yt.streams.get_highest_resolution()
    
    print(f"download video...: {yt.title}")
    video_stream.download()
    
    print("✅ Download successfully!")

except Exception as e:
    print(f"❌ An error occurred while downloading: {e}")
