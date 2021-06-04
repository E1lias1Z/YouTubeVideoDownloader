from tkinter import * 
from tkinter import ttk, messagebox, Menu
from pytube import YouTube, exceptions, Playlist
import re

#class of thie MAIN program
class MainProgram:
    #main window
    def __init__(self, width, height, title='Youtube video downloader'):
        self.window = Tk()
        self.window.geometry('x'.join([str(width), str(height)]))
        self.window.title(title)
        self.window.resizable(width=False, height=False)
        self.progress1 = ttk.Progressbar(self.window, orient=HORIZONTAL, mode="indeterminate", length=100)
        self.progress2 = ttk.Progressbar(self.window, orient=HORIZONTAL, mode="indeterminate", length=100)

    #draw widgets
    def widgets(self):
        self.drawMenu()
        self.linkVideo()
        self.resolutionsList()
        self.downloadVideo_button()
        # self.progressBar1()
        # self.progressBar2()
        self.linkPlaylist()
        self.linkFolder()
        self.downloadPlaylist_button()
    
    #insert main menu
    def drawMenu(self):
        menu = Menu(self.window)
        exit_menu = Menu(menu, tearoff=0)
        exit_menu.add_separator()
        exit_menu.add_command(label='Exit', command=self.exit_prog)

        info_menu = Menu(menu, tearoff=0)
        info_menu.add_command(label='About', command=self.show_inform)

        menu.add_cascade(label='File', menu=exit_menu)
        menu.add_cascade(label='Help', menu=info_menu)
        self.window.configure(menu=menu)

    # def progressBar1(self):
    #     self.progress1.grid(row=4, column=0)

    # def progressBar2(self):
    #     self.progress2.grid(row=9, column=0)

    #exit program command
    def exit_prog(self):
        self.window.destroy()
    
    #show information about this program (not too much usefyl :))
    def show_inform(self):
        messagebox.showinfo('Info', 'Program helps you yo download any video or playlist from YouTube')

    #string bar for link of video
    def linkVideo(self):
        self.link = StringVar()
        Label(text="Link on video:", font="Arial 12").grid(row=1, column=0, padx = 20, pady=10)
        linkEntry = Entry(self.window, textvariable=self.link, width=60).grid(row=1, column=1)
    
    #listbox of video resolutions
    def resolutionsList(self):
        self.resols = ['1080p', '720p', '480p', '360p']    
        Label(text="Resolution:", font="Arial 12").grid(row=2, column=0, padx = 20)
        self.resolution_list = ttk.Combobox(self.window, values=self.resols)
        self.resolution_list.grid(row=2, column=1)
        self.resolution_list.current(3)
    
    #download video function
    def download_video(self):
        try:
            vid = YouTube(self.link.get(), on_complete_callback=self.progress1.start());
            video_down = vid.streams.filter(progressive=True, file_extension='mp4', resolution=self.resolution_list.get()).desc().first()
            if video_down is not None:
                #progressBar_Step()
                video_down.download('C:\\Users\\USER\\Downloads')
                Label(text="Video downloaded succesfully!", font="Arial 14 bold", fg="#32CD32").grid(row=3, column=1)
            else:
                Label(text="     Video not downloaded :(     ", font="Arial 14 bold", fg="#8B0000").grid(row=3, column=1)
        except exceptions.RegexMatchError:
            messagebox.showerror("ERROR", "Incorrect input video link!")
    
    #download video button
    def downloadVideo_button(self):
        Button(self.window, text='Download video', command=self.download_video).grid(row=3, column=0, pady=10)
    
    #string bar for link of video
    def linkPlaylist(self):
        self.link_playlist = StringVar()
        Label(text="Link on playlist:", font="Arial 12").grid(row=5, column=0, padx=20, pady=10)
        link_playlist_Entry = Entry(self.window, textvariable=self.link_playlist, width=60).grid(row=5, column=1)
    
    #string bar for link of folder
    def linkFolder(self):
        self.download_folder = StringVar()
        Label(text="Folder:", font="Arial 12").grid(row=6, column=0, padx=20)
        Label(text=r''' e. g. C:\Users\USER\Downloads''', font="Arial 10").grid(row=7, column=1)
        folder_Entry = Entry(self.window, textvariable=self.download_folder, width=60).grid(row=6, column=1)
        
#-------------------------------------------------------------------------------------------------------------------------
    #download playlist function
    def download_playlist(self):
        try:
            plyst = Playlist(self.link_playlist.get())
            folder = self.download_folder.get(); folder_correct = re.sub(r'\\', r'\\\\', folder)
            count_downloaded = 0
            for video in plyst.video_urls:
                vid = YouTube(video)
                video_pl = vid.streams.filter(progressive=True).desc().first()
                if video_pl is not None:
                    video_pl.download(folder_correct)
                count_downloaded += 1
            if(count_downloaded > 0):
                Label(text="Playlist downloaded succesfully!", font="Arial 14 bold", fg="#32CD32").grid(row=8, column=1)
            else:
                Label(text="Playlist not downloaded :(", font="Arial 14 bold", fg="#8B0000").grid(row=8, column=1)
        except KeyError:
            messagebox.showerror("ERROR", "Incorrect input playlist link!")
    
    #download playlist button
    def downloadPlaylist_button(self):
        Button(self.window, text='Download playlist', command=self.download_playlist).grid(row=8, column=0, pady=10)

    #run the program
    def run(self):
        self.widgets()
        self.window.mainloop()

#--------------------------------------------------------------------------------------------

app = MainProgram(570, 280)
app.run()

#----------------------------------------------------------------------------------------------------------------
