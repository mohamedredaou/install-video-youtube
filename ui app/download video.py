import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube, Playlist
import threading
import os

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("B-Sigma | YouTube Downloader")
        master.geometry('550x450')
        master.configure(bg="#202033")
        master.resizable(False, False) # Disable resizing

        # Title Label
        self.title_label = tk.Label(master,
                                    text='YouTube Video/Playlist Downloader',
                                    font=('arial', 20, 'bold'),
                                    fg='white',
                                    bg='#202033')
        self.title_label.pack(pady=20)

        # Link Label
        self.link_label = tk.Label(master,
                                   text='Paste Link Here:',
                                   font=('arial', 15, 'bold'),
                                   fg='white',
                                   bg='#202033')
        self.link_label.place(x=180, y=80)

        # Link Entry
        self.link_var = tk.StringVar()
        self.link_entry = tk.Entry(master,
                                   width=60,
                                   textvariable=self.link_var,
                                   font=('arial', 12))
        self.link_entry.place(x=50, y=120, height=30)

        # Message Label for status updates
        self.message_label = tk.Label(master,
                                      text='Enter URL and choose download type',
                                      font=('arial', 12),
                                      fg='lightgreen',
                                      bg='#202033')
        self.message_label.place(x=100, y=170)

        # Download Path Label and Button
        self.path_label_text = tk.StringVar(value="Download Path: Default (Current Directory)")
        self.path_label = tk.Label(master,
                                   textvariable=self.path_label_text,
                                   font=('arial', 10),
                                   fg='white',
                                   bg='#202033')
        self.path_label.place(x=50, y=210)

        self.path_button = tk.Button(master,
                                     text='Choose Download Folder',
                                     font=('arial', 10, 'bold'),
                                     bg='#4CAF50', # Greenish
                                     fg='white',
                                     command=self.choose_download_path)
        self.path_button.place(x=350, y=205)

        self.download_path = os.getcwd() # Default download path

        # Download Video Button
        self.download_video_button = tk.Button(master,
                                               text='Download Video',
                                               font=('arial', 15, 'bold'),
                                               bg='pale violet red',
                                               padx=10,
                                               command=self.start_video_download_thread)
        self.download_video_button.place(x=80, y=280)

        # Download Playlist Button
        self.download_playlist_button = tk.Button(master,
                                                  text='Download Playlist',
                                                  font=('arial', 15, 'bold'),
                                                  bg='#00BFFF', # Deep sky blue
                                                  padx=10,
                                                  command=self.start_playlist_download_thread)
        self.download_playlist_button.place(x=280, y=280)

        # Exit Button
        self.exit_button = tk.Button(master,
                                     text='Exit',
                                     font=('arial', 12, 'bold'),
                                     bg='#FF6347', # Tomato red
                                     fg='white',
                                     command=master.quit)
        self.exit_button.place(x=240, y=360)


    def choose_download_path(self):
        """Allows user to select a download directory."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path = folder_selected
            self.path_label_text.set(f"Download Path: {os.path.basename(folder_selected)}")
            self.update_message(f"Download folder set to: {os.path.basename(folder_selected)}", 'lightblue')
        else:
            self.update_message("Download folder selection cancelled.", 'orange')


    def update_message(self, message, color='lightgreen'):
        """Updates the status message label."""
        self.message_label.config(text=message, fg=color)
        self.master.update_idletasks() # Refresh the GUI


    def set_buttons_state(self, state):
        """Enables or disables download buttons."""
        self.download_video_button.config(state=state)
        self.download_playlist_button.config(state=state)
        self.path_button.config(state=state)


    def start_video_download_thread(self):
        """Starts video download in a separate thread to keep GUI responsive."""
        url = self.link_var.get()
        if not url:
            self.update_message("Please paste a YouTube video URL.", 'yellow')
            return
        self.set_buttons_state(tk.DISABLED)
        self.update_message("Starting video download...", 'yellow')
        download_thread = threading.Thread(target=self._download_single_video, args=(url,))
        download_thread.start()


    def start_playlist_download_thread(self):
        """Starts playlist download in a separate thread to keep GUI responsive."""
        url = self.link_var.get()
        if not url:
            self.update_message("Please paste a YouTube playlist URL.", 'yellow')
            return
        self.set_buttons_state(tk.DISABLED)
        self.update_message("Starting playlist download...", 'yellow')
        download_thread = threading.Thread(target=self._download_playlist, args=(url,))
        download_thread.start()


    def _download_single_video(self, url):
        """Handles the logic for downloading a single video."""
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            self.update_message(f"Downloading video: {yt.title}", 'yellow')
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_path=self.download_path)
            self.update_message(f"✅ Downloaded: {yt.title}", 'lightgreen')
        except Exception as e:
            self.update_message(f"❌ Error downloading video: {e}", 'red')
        finally:
            self.set_buttons_state(tk.NORMAL)


    def _download_playlist(self, playlist_url):
        """Handles the logic for downloading a playlist."""
        try:
            pl = Playlist(playlist_url)
            self.update_message(f"Downloading playlist: {pl.title} ({len(pl.video_urls)} videos)", 'yellow')

            # Create a specific subfolder for the playlist
            playlist_folder = os.path.join(self.download_path, f"Playlist_{pl.title.replace(' ', '_')}")
            os.makedirs(playlist_folder, exist_ok=True) # Create folder if it doesn't exist

            for index, video in enumerate(pl.videos, start=1):
                self.update_message(f"[{index}/{len(pl.video_urls)}] Downloading: {video.title}", 'yellow')
                video.streams.get_highest_resolution().download(output_path=playlist_folder)
            self.update_message(f"✅ Downloaded playlist: {pl.title}", 'lightgreen')
        except Exception as e:
            self.update_message(f"❌ Error downloading playlist: {e}", 'red')
        finally:
            self.set_buttons_state(tk.NORMAL)


    def on_progress(self, stream, chunk, bytes_remaining):
        """Callback function to update progress during download."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.update_message(f"Downloading: {percentage_of_completion:.2f}%", 'yellow')


if __name__ == '__main__':
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
