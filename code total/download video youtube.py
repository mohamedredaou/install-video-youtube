from pytube import YouTube
from pytube import Playlist

print("1-download video youtube")
print("2-download playlist video youtube")

type = input("enter (1|2) : ")

if type == "1":
    url = input("enter url video in youtube: ")

    try:
        yt = YouTube(url)
    
        video_stream = yt.streams.get_highest_resolution()
    
        print(f"download video...: {yt.title}")
        video_stream.download()
    
        print("✅ Download successfully!")

    except Exception as e:
        print(f"❌ An error occurred while downloading: {e}")

elif type == "2":
    playlist_url = input("enter url playlist video in youtube: ")

    try:
        pl = Playlist(playlist_url)

        print(f"download video...: {pl.title}")
        print(f"{len(pl.video_urls)} video")

        for index, video in enumerate(pl.videos, start=1):
            print(f"\n[{index}/{len(pl.video_urls)}] Downloaded playlist: {video.title}")
            video.streams.get_highest_resolution().download(output_path="Playlist_Downloads")

        print("\n✅ Downloaded successfully!")

    except Exception as e:
        print(f"❌ An error occurred while downloading: {e}")
