import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer

root = Tk()

# create menu
menubar = Menu(root)
root.config(menu=menubar)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)


#  create submenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=submenu)
submenu.add_command(label='new file')
submenu.add_command(label='open', command=browse_file)
submenu.add_command(label='exit', command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('about Melody', 'info on us')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=submenu)
submenu.add_command(label='about', command=about_us)
submenu.add_command(label='version info')


mixer.init()  # initializing mixer
root.title('Melody')
root.iconbitmap(r'Melody.ico')

text = Label(root, text='lets rock!')
text.pack(pady=10)

photo = PhotoImage(file='play-button.png')


def play_btn():
    try:
        paused  # whether music is paused or not
    except NameError:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            + ' ' + os.path.basename(filename)
            print('Its working!!')
        except:
            tkinter.messagebox.showerror('file not found', 'Melody cant find the music')
            print("error")
        else:
            mixer.music.unpause()


def pause_btn():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music paused"


def stop_btn():
    mixer.music.stop()
    statusbar['text'] = "Stopping Music" + ' ' + filename


def set_vol(vol):
    volume = int(vol)/100
    mixer.music.set_volume(volume)


def rewind_btn():
    play_btn()
    statusbar['text'] = "Music rewinded"



middleFrame = Frame(root)
middleFrame.pack(padx=40, pady=40)

bottomFrame = Frame(root)
bottomFrame.pack()

rewindPhoto = PhotoImage(file='rewind-circular-button.png')
rewindbtn = Button(bottomFrame, image=rewindPhoto, command=rewind_btn)
rewindbtn.grid(row=0, column=0)



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
scale.set(5)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=0)

statusbar = Label(root, text='welcome to Melody', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()
