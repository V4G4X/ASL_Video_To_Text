import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *

from getLocation import getLocation
from sendMail import send_email
from textToSpeech import tts
from utility import predict, preprocess

#Variables
HEIGHT = 800
WIDTH = 800

root = tk.Tk()
root.title('Sign Language Interpreter!')

#Use canvas as root holder
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#Heading
headLabel = tk.Label(root,bg='Gray',text='Welcome to the American Sign Language Interpreter!',font=("Arial", 20))
headLabel.place(relx=0.05,relwidth=0.90,relheight=0.15)

#Use frame for actual placing of elements
def viewLiveStream():
    os.system('python3 ./record-video-model-divider.py')
    dataEntry.configure(text = os.path.abspath(r'LiveRecording'))

#hover effect
def on_enter(e):
    e.widget['background'] = 'MediumPurple1'

def on_leave(e):
    e.widget['background'] = 'Gray'

#VideoInput Frame
frame = tk.LabelFrame(root, fg='black', bg='#80c1ff', text='Video Input', font=('Helvetica',15) , relief ='groove' ,borderwidth=5)
frame.place(relx=0.05,rely=0.18,relwidth=0.90,relheight=0.5)

#Live Stream Button
liveStreamButton = tk.Button(frame,text='Record Live Video',font=('Helvetica',20),bg='white',fg='black',command=viewLiveStream)
liveStreamButton.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.15)
liveStreamButton.bind("<Enter>",on_enter)
liveStreamButton.bind("<Leave>",on_leave)

#OR Label
orLabel = tk.Label(frame, fg='black', bg='#80c1ff',text='OR',font=('Helvetica',15))
orLabel.place(relx=0.35,rely=0.30,relwidth=0.3,relheight=0.1)

#Location Label
locationLabel = tk.Label(frame, fg='black', bg='#80c1ff',text='Location:',font=('Helvetica',15))
locationLabel.place(relx=0.03,rely=0.45,relwidth=0.16,relheight=0.15)

#Button that will contain the location of the selected video
dataEntry = Label(frame, font=20)
dataEntry.place(relx=0.18,rely=0.45,relwidth=0.60,relheight=0.15)

#Function to browse and read file
def browseFile():
    file = filedialog.askdirectory(parent=frame,title='Choose the video directory')
    dataEntry.configure(text = str(file))


#Button to browse only videos from the file system that need to be interpreted for sign language
browseButton = tk.Button(frame, text='Browse',font=('Helvetica',20), bg='white', fg='black',command=browseFile)
browseButton.place(relx=0.80,rely=0.45,relwidth=0.18,relheight=0.15)
browseButton.bind("<Enter>",on_enter)
browseButton.bind("<Leave>",on_leave)

#Function to check if a file is a video
def isVideo(filePath):
    ext = filePath[filePath.rfind('.')+1:]
    # print("Extension: %s"%(ext))
    return ext == 'mp4'

# Function to pass the video_folder path given for processing
def convert_folder():
    # Initialise Progress and outputDisplay
    progress.place(relx=0.2,rely=0.85,relwidth=0.60,relheight=0.07)
    progress['value'] = 0
    outputDisplay.configure(text = '')

    # Clear out the previous face
    if os.path.isfile('face.jpeg'):
        os.remove('face.jpeg')

    folder_path = dataEntry.cget(key = "text")
    try:
        video_list = sorted([os.path.join(folder_path,each) for each in os.listdir(folder_path)])
    except Exception as e:
        # Incase where the input path may be incorrect e.g blank
        tk.messagebox.showinfo("Error", str(e))
    for each in video_list:
        if not isVideo(each):
            tk.messagebox.showinfo("Error", "Folder contains non-mp4 files.")
            return None
    try:
        step = 100/len(video_list)
        for video in video_list:
            root.update_idletasks()
            descriptor = preprocess(video)
            word = predict(descriptor)
            print("Predicted:", word)
            outputDisplay.configure(text = outputDisplay.cget(key = "text") + word + ' ')
            progress['value'] += step
    except Exception as e:
        tk.messagebox.showinfo("Error", str(e))
        raise e
    # progress.destroy()

#Upload button to upload video to the application
convertButton = tk.Button(frame, text='Translate',font=('Helvetica',20), bg='white', fg='black',command=convert_folder)
convertButton.place(relx=0.35,rely=0.65,relwidth=0.3,relheight=0.15)
convertButton.bind("<Enter>",on_enter)
convertButton.bind("<Leave>",on_leave)

# Progress Bar for Translation
progress = Progressbar(frame, orient=HORIZONTAL, len=800, mode='determinate')

#Output Frame
outputFrame = tk.LabelFrame(root, fg='black', bg='#80c1ff',text='Output',font=('Helvetica',15),relief ='groove',borderwidth=5)
outputFrame.place(relx=0.05,rely=0.7,relwidth=0.90,relheight=0.25)

#Textbox to print text output
outputDisplay = Label(outputFrame, font=('Arial',20))
outputDisplay.place(relx=0.02,rely=0.15,relheight=0.3,relwidth=0.75)

# Function that will read out text of outputDisplay
def readOutOutput():
    text = outputDisplay.cget(key="text")
    if text == '':
        tk.messagebox.showinfo("Error", "No text to read.")
    else:
        tts(text=text)

# Button to generate output
audioButton = tk.Button(outputFrame,text='Audio',font=('Helvetica',20), bg='white', fg='black',command=readOutOutput)
audioButton.place(relx=0.8,rely=0.15,relheight=0.3,relwidth=0.18)
audioButton.bind("<Enter>",on_enter)
audioButton.bind("<Leave>",on_leave)

# Function to get User's co-ordinates, face and then sends mail
def emailDetails():
    coords = None
    try:
        coords = getLocation()
        #coords = "Coords"
        msg = outputDisplay.cget(key = "text")
        if(msg != ''):
            send_email(msg, coords)
            tk.messagebox.showinfo("Success!", "Mail has been sent!")
        else:
            tk.messagebox.showinfo("Error", "No text to send.")    
    except TypeError as e:
        tk.messagebox.showinfo("Error", "Check Internet Connection.")
        raise e
    except Exception as e:
        tk.messagebox.showinfo("Error", "Check Internet Connection.")
        raise e


#Button to send Email
emailButton = tk.Button(outputFrame,text='Send Email',font=('Helvetica',20), bg='white', fg='black', command=emailDetails)
emailButton.place(relx=0.25,rely=0.55,relwidth=0.5,relheight=0.3)
emailButton.bind("<Enter>",on_enter)
emailButton.bind("<Leave>",on_leave)


# outputDisplay.configure(text = "This is some sample message text")

#Driver
root.mainloop()