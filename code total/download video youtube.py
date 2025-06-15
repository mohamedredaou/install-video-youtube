from pytube import YouTube
from pytube import Playlist

print("1-download video youtube")
print("2-download playlist video youtube")

# Get user input for the download type
type = input("enter (1|2) : ")

if type == "1":
    # --- Single Video Download ---
    url = input("enter url video in youtube: ")

    try:
        # Create a YouTube object from the URL
        yt = YouTube(url)
        
        # Select the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()
        
        print(f"download video...: {yt.title}")
        # Download the video
        video_stream.download()
        
        print("✅ Download successfully!")

    except Exception as e:
        # Catch any errors during the process and print an error message
        print(f"❌ An error occurred while downloading: {e}")

elif type == "2":
    # --- Playlist Download ---
    playlist_url = input("enter url playlist video in youtube: ")

    try:
        # Create a Playlist object from the URL
        pl = Playlist(playlist_url)

        print(f"download video...: {pl.title}")
        print(f"{len(pl.video_urls)} video")

        # Loop through each video in the playlist
        for index, video in enumerate(pl.videos, start=1):
            print(f"\n[{index}/{len(pl.video_urls)}] Downloaded playlist: {video.title}")
            # Download each video to a specific folder named "Playlist_Downloads"
            video.streams.get_highest_resolution().download(output_path="Playlist_Downloads")

        print("\n✅ Downloaded successfully!")

    except Exception as e:
        # Catch any errors during the process and print an error message
        print(f"❌ An error occurred while downloading: {e}")
