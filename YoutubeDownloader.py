import os
import subprocess
from pytube import YouTube, Playlist
from tkinter import *
from tkinter import ttk, filedialog, messagebox


class Interface:
    def __init__(self, parent):
        self.parent = parent
        self.notebook = ttk.Notebook(self.parent)

        self.single = Frame(self.parent)
        self.playlist = Frame(self.parent)

        self.notebook.grid(row=0)

        self.notebook.add(self.single, text="Single Video")
        self.notebook.add(self.playlist, text="Playlist")

        self.title = ttk.Label(self.single, text="Youtube Downloader").grid(
            row=1, columnspan=4
        )
        self.title = ttk.Label(self.playlist, text="Youtube Downloader").grid(
            row=1, columnspan=4
        )

        self.urlLabel1 = ttk.Label(self.single, text="URL").grid(row=2)
        self.urlEntry1 = ttk.Entry(self.single)
        self.urlEntry1.grid(row=2, column=1)

        self.urlLabel2 = ttk.Label(self.playlist, text="URL").grid(row=2)
        self.urlEntry2 = ttk.Entry(self.playlist)
        self.urlEntry2.grid(row=2, column=1)

        self.streamLabel1 = ttk.Label(self.single, text="Stream").grid(row=2, column=2)
        self.streamEntry1 = ttk.Combobox(
            self.single, values=["Progressive", "Only Audio"]
        )
        self.streamEntry1.grid(row=2, column=3)

        self.streamLabel2 = ttk.Label(self.playlist, text="Stream").grid(
            row=2, column=2
        )
        self.streamEntry2 = ttk.Combobox(
            self.playlist, values=["Progressive", "Only Audio"]
        )
        self.streamEntry2.grid(row=2, column=3)

        self.checkAvail1 = ttk.Button(
            self.single,
            text="Check Availability",
            command=lambda: self.process("single"),
        ).grid(row=3, columnspan=4)
        self.checkAvail2 = ttk.Button(
            self.playlist,
            text="Check Availability",
            command=lambda: self.process("playlist"),
        ).grid(row=3, columnspan=4)

        self.status1 = ttk.Label(self.single, text="Status").grid(row=4)
        self.statusEntry1 = ttk.Label(self.single, text="")
        self.statusEntry1.grid(row=4, column=1)

        self.status2 = ttk.Label(self.playlist, text="Status").grid(row=4)
        self.statusEntry2 = ttk.Label(self.playlist, text="")
        self.statusEntry2.grid(row=4, column=1)

    def process(self, type):
        if type == "single":
            try:
                self.url = self.urlEntry1.get()
                self.stream = self.streamEntry1.get()
                print(self.url)
                self.youtube = self.yt = YouTube(self.url)
                if self.stream == "Progressive":
                    self.yt = self.yt.streams.filter(progressive=True)
                    resValues = self.getResolutions(self.yt)

                    self.resLabel = ttk.Label(self.single, text="Resolution").grid(
                        row=5
                    )
                    self.resEntry = ttk.Combobox(self.single, values=resValues)
                    self.resEntry.grid(row=5, column=1)
                else:
                    self.yt = self.yt.streams.filter(only_audio=True)

                self.saveasLabel = ttk.Label(self.single, text="Save As").grid(row=6)
                self.saveas = ttk.Entry(self.single)
                self.saveas.grid(row=6, column=1)

                self.location1 = ttk.Label(self.single, text="Download Location").grid(
                    row=7
                )
                self.locationEntry1 = ttk.Label(self.single, text="")
                self.locationEntry1.grid(row=7, column=1)

                self.browse1 = ttk.Button(
                    self.single,
                    text="Browse",
                    command=lambda: self.downloadLocation("single"),
                ).grid(row=7, column=2)

                self.download1 = ttk.Button(
                    self.single, text="Download", command=self.download
                ).grid(row=8, columnspan=4)

                self.statusEntry1.config(text="Video available")

            except Exception as e:
                self.statusEntry1.config(text="Video not available")
                messagebox.showerror(
                    title="Youtube Video Downloader",
                    message="Video not available for download",
                )
                self.parent.quit()
        else:
            try:
                self.url = self.urlEntry2.get()
                self.stream = self.streamEntry2.get()
                self.pl = Playlist(self.url)
                self.pl._video_regex = re.compile(r"(/watch\?v=[\w-]*)")
                print(self.pl)
                if not self.pl:
                    raise Exception

                self.saveasLabel = ttk.Label(
                    self.playlist, text="Save As(Folder Name)"
                ).grid(row=6)
                self.saveas = ttk.Entry(self.playlist)
                self.saveas.grid(row=6, column=1, columnspan=3)

                self.location2 = ttk.Label(
                    self.playlist, text="Download Location"
                ).grid(row=7)
                self.locationEntry2 = ttk.Label(self.playlist, text="")
                self.locationEntry2.grid(row=7, column=1)

                self.browse2 = ttk.Button(
                    self.playlist,
                    text="Browse",
                    command=lambda: self.downloadLocation("playlist"),
                ).grid(row=7, column=2)

                self.download2 = ttk.Button(
                    self.playlist, text="Download", command=self.downloadPlaylist
                ).grid(row=8, columnspan=4)

                self.statusEntry2.config(text="Playlist available")

            except Exception as e:
                print(e)
                self.statusEntry2.config(text="Playlist not available")
                messagebox.showerror(
                    title="Youtube Video Downloader",
                    message="Playlist not available for download!",
                )
                self.parent.quit()

    def downloadLocation(self, type):
        self.directory = filedialog.askdirectory()
        if type == "single":
            self.locationEntry1.config(text=self.directory)
        else:
            self.locationEntry2.config(text=self.directory)

    def getResolutions(self, yt):
        self.resolutions = dict()

        for stream in yt:
            self.resolutions[stream.resolution] = stream

        res = [key for key in self.resolutions.keys() if key]

        return res

    def onComplete(self, stream, file_handle):
        # subprocess.Popen(['notify-send', 'Youtube Download', 'DONE'])
        print("Download Complete")

    def download(self):
        try:
            self.youtube.register_on_complete_callback(self.onComplete)
            name = self.saveas.get()
            if self.stream == "Progressive":
                r = self.resEntry.get()
                toDownload = self.resolutions[r]
                toDownload.download(self.directory, filename=name)
            else:
                toDownload = self.yt.first()
                toDownload.download(self.directory, filename="audio")
                inp = f"{self.directory}\\audio.mp4"
                out = f"{self.directory}\\{name}.mp3"
                subprocess.call(["ffmpeg", "-i", inp, out], shell=True)

                os.remove(inp)

            messagebox.showinfo(
                title="Youtube Video Downloader",
                message="Download successfully completed",
            )
            self.parent.quit()
        except Exception as e:
            messagebox.showerror(
                title="Youtube Video Downloader",
                message="Unfortunately download stopped! Please try again later",
            )
            print(e)
            self.parent.quit()

    def downloadPlaylist(self):
        try:
            saveAs = self.saveas.get()
            path = os.path.join(self.directory, saveAs)
            os.mkdir(path)
            i = 1
            if self.stream == "Progressive":
                for url in self.pl:
                    name = f"video {i}"
                    yt = (
                        YouTube(url)
                        .streams.filter(progressive=True, file_extension="mp4")
                        .order_by("resolution")
                        .desc()
                        .first()
                        .download(path, filename=name)
                    )
                    i += 1
                    print(f"{name} Done")
            else:
                for url in self.pl:
                    title = YouTube(url).title
                    name = f"Audio {i}"
                    yt = (
                        YouTube(url)
                        .streams.filter(only_audio=True)
                        .first()
                        .download(path, filename=name)
                    )
                    i += 1

                    toDelete = os.path.join(path, f"{name}.mp4")
                    toCreate = os.path.join(path, f"{name}.mp3")
                    subprocess.call(["ffmpeg", "-i", toDelete, toCreate], shell=True)
                    os.remove(toDelete)
                    print(f"{name} Done")

            messagebox.showinfo(
                title="Youtube Video Downloader",
                message="Download successfully completed",
            )
            self.parent.quit()
        except Exception as e:
            messagebox.showerror(
                title="Youtube Video Downloader",
                message="Unfortunately download stopped! Please try again later",
            )
            print(e)
            self.parent.quit()


if __name__ == "__main__":
    root = Tk()
    Interface(root)
    root.mainloop()
