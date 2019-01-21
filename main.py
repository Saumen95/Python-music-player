import os
import time
import threading
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer

root = Tk()

tatusbar = Label(root, text='welcome to Melody', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# create menu
menubar = Menu(root)
root.config(menu=menubar)

#  create submenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=submenu)
submenu.add_command(label='new file')
submenu.add_command(label='open', command=browse_file)
submenu.add_command(label='exit', command=root.destroy)

submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=submenu)
submenu.add_command(label='about', command=about_us)
submenu.add_command(label='version info')


def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    print(file_path)
    add_to_playlist(file_path)


# adding file to playlist
# playlistbox contains only the filename
# playlist contains filename and path
def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, file_path)
    index += 1


def about_us():
    tkinter.messagebox.showinfo('about Melody', 'info on us')


mixer.init()  # initializing mixer
root.title('Melody')
root.iconbitmap(r'Melody.ico')

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30)

rightFrame = Frame(root)
rightFrame.pack()

topFrame = Frame(rightFrame)
topFrame.pack()


lengthlabel = Label(topFrame, text='length- 00:00')
lengthlabel.pack(pady=10)

currenttimelabel = Label(topFrame, text='currenttime- 00:00', relief=GROOVE)
currenttimelabel.pack(pady=10)


btn1 = Button(leftFrame, text="+ add", command=browse_file)
btn1.pack(side=LEFT)


def del_song():
    selected_songs = playlistbox.curselection()
    selected_songs = int(selected_songs[0])
    play_it = playlist[selected_songs]
    playlistbox.delete(selected_songs)
    playlist.pop(selected_songs)


btn2 = Button(leftFrame, text="-Del", command=del_song)
btn2.pack(side=LEFT)

playlistbox = Listbox(leftFrame)
playlistbox.pack()

photo = PhotoImage(file='play-button.png')


def show_details(play_song):

    file_data = os.path.splitext(play_song)
    print(file_data)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        a.get_length()

    mins, secs = divmod(total_length, 60)
    print(round(mins))
    print(round(secs))
    timeFormat = '(:02d):(:02d)'.format(mins, secs)
    lengthlabel['text'] = "total length" + " " + os.path.basename(file_path)
    t1 = threading.Thread(target=start_count, args=(total_length))  # threading implied
    t1.start()
    start_count(total_length)


# display current playtime of a music
def start_count(t):
    global paused
    # mixer.music.get_busy() stops the music when stop button is pressed
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            print(round(mins))
            print(round(secs))
            timeFormat = '(:02d):(:02d)'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + " " + os.path.basename(file_path)
            time.sleep(1)
            current_time += 1


# Playing music
def play_btn():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"
        paused = FALSE
    else:
        try:
            stop_btn()
            time.sleep(1)
            selected_songs = playlist.curselection()
            selected_songs = int(selected_songs[0])
            play_it = playlist2[selected_songs]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + " " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('file not found', 'Melody cant find the file')


paused = FALSE


def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music paused"


def stop_btn():
    mixer.music.stop()
    statusbar['text'] = "Stopping Music" + ' ' + file_path


def set_vol(vol):
    volume = int(vol)/100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_btn():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        volumebtn.configure(image=volumePhoto)
        Scale.set(5)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumebtn.configure(image=mutePhoto)
        Scale.set(0)
        muted = TRUE


def rewind_btn():
    play_btn()
    statusbar['text'] = "Music rewinded"


middleFrame = Frame(rightFrame)
middleFrame.pack(padx=40, pady=40)

# bottomframe for vol,mute,rewind etc
bottomFrame = Frame(rightFrame)
bottomFrame.pack()

rewindPhoto = PhotoImage(file='rewind-circular-button.png')
rewindbtn = Button(bottomFrame, image=rewindPhoto, command=rewind_btn)
rewindbtn.grid(row=0, column=0)

mutePhoto = PhotoImage(file='mute.png')
volumePhoto = PhotoImage(file='volume.png')
volumebtn = Button(bottomFrame, image=volumePhoto, command=mute_btn)
volumebtn.grid(row=0, column=0)


playPhoto = PhotoImage(file='play-button.png')
playbtn = Button(middleFrame, image=playPhoto, command=play_btn)
playbtn.grid(row=0, column=0, padx=10)

PausePhoto = PhotoImage(file='pause.png')
pausebtn = Button(middleFrame, image=PausePhoto, command=pause_btn)
pausebtn.grid(row=0, column=1, padx=10)

StopPhoto = PhotoImage(file='stop.png')
stopbtn = Button(middleFrame, image=StopPhoto, command=stop_btn)
stopbtn.grid(row=0, column=2, padx=10)

scale = Scale(root, from=0, to=10, orient=HORIZONTAL, command=set_vol)  # controlling music volume
Scale.set(5)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=0, padx=30)


def on_closing():
    stop_btn()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
