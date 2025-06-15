from pytube import Playlist

playlist_url = input("enter url playlist video in youtube: ")

try:
    pl = Playlist(playlist_url)

    print(f"جارٍ تنزيل قائمة التشغيل: {pl.title}")
    print(f"تحتوي على {len(pl.video_urls)} فيديو")

    for index, video in enumerate(pl.videos, start=1):
        print(f"\n[{index}/{len(pl.video_urls)}] Downloaded playlist: {video.title}")
        video.streams.get_highest_resolution().download(output_path="Playlist_Downloads")

    print("\n✅ Downloaded successfully!")

except Exception as e:
    print(f"❌ An error occurred while downloading: {e}")
