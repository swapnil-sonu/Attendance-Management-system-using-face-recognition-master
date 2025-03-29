import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Function to convert text to speech
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# File paths for required resources
haarcasecade_path = "haarcascade_frontalface_default.xml"  # Path to Haar Cascade XML file for face detection
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"  # Path to trained model file
trainimage_path = "/TrainingImage"  # Path to folder containing training images
if not os.path.exists(trainimage_path):  # Create the folder if it doesn't exist
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"  # Path to CSV file containing student details
attendance_path = "Attendance"  # Path to folder where attendance records will be stored

# Initialize the main application window
window = Tk()
window.title("SmartAttend")  # Title of the application
window.geometry("1280x720")  # Set the window size
window.configure(background="#3f3f3f")  # Set a dark theme for the application

# Function to destroy the error screen
def del_sc1():
    sc1.destroy()

# Function to display an error message when enrollment or name is missing
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")  # Set the size of the error window
    sc1.iconbitmap("AMS.ico")  # Set the icon for the error window
    sc1.title("Warning!!")  # Title of the error window
    sc1.configure(background="#3f3f3f")  # Set a dark background
    sc1.resizable(0, 0)  # Disable resizing
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#3f3f3f",
        font=("Verdana", 16, "bold"),
    ).pack()  # Display the error message
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)  # Add an OK button to close the error window

# Function to validate input (only digits allowed for enrollment number)
def testVal(inStr, acttyp):
    if acttyp == "1":  # Insert action
        if not inStr.isdigit():  # Check if the input is not a digit
            return False
    return True

# Load and display the application logo
logo = Image.open("UI_Image/0001.png")
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#3f3f3f", relief=GROOVE, bd=10, font=("Verdana", 30, "bold"))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#3f3f3f")
l1.place(relx=0.01, rely=0.02, anchor="nw")  # Position the logo

# Display the application title
titl = tk.Label(
    window, text="GOVERNMENT AUTONOMOUS COLLEGE", bg="#3f3f3f", fg="yellow", font=("Verdana", 27, "bold"),
)
titl.place(relx=0.5, rely=0.05, anchor="center")  # Center the title

# Display a welcome message
a = tk.Label(
    window,
    text="Welcome to MCA",
    bg="#3f3f3f",
    fg="yellow",
    bd=10,
    font=("Verdana", 35, "bold"),
)
a.place(relx=0.5, rely=0.15, anchor="center")  # Center the welcome message

# Load and display images for different functionalities
ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(relx=0.1, rely=0.4, anchor="center")  # Register image

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(relx=0.9, rely=0.4, anchor="center")  # Attendance image

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(relx=0.5, rely=0.4, anchor="center")  # Verify image

# Function to open the "Take Image" UI
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")  # Title of the window
    ImageUI.geometry("780x480")  # Set the window size
    ImageUI.configure(background="#3f3f3f")  # Set a dark background
    ImageUI.resizable(0, 0)  # Disable resizing
    titl = tk.Label(ImageUI, bg="#3f3f3f", relief=GROOVE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)

    # Title for the "Take Image" window
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#3f3f3f", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(relx=0.5, rely=0.05, anchor="center")  # Center the title

    # Heading for the details section
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#3f3f3f",
        fg="yellow",
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(relx=0.5, rely=0.2, anchor="center")  # Center the heading

    # Enrollment number input
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=12,
        height=2,
        bg="#3f3f3f",
        fg="yellow",
        bd=5,
        relief=GROOVE,
        font=("Verdana", 14),
    )
    lbl1.place(relx=0.15, rely=0.3, anchor="center")  # Label for enrollment number
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",
        fg="yellow",
        relief=GROOVE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.4)  # Input field for enrollment number
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name input
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=12,
        height=2,
        bg="#3f3f3f",
        fg="yellow",
        bd=5,
        relief=GROOVE,
        font=("Verdana", 14),
    )
    lbl2.place(relx=0.15, rely=0.45, anchor="center")  # Label for name
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=GROOVE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.4)  # Input field for name

    # Notification label
    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=12,
        height=2,
        bg="#3f3f3f",
        fg="yellow",
        bd=5,
        relief=GROOVE,
        font=("Verdana", 14),
    )
    lbl3.place(relx=0.15, rely=0.6, anchor="center")  # Label for notifications

    # Notification message display
    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=GROOVE,
        font=("Verdana", 14, "bold"),
    )
    message.place(relx=0.6, rely=0.6, anchor="center", relwidth=0.6)  # Notification message display

    # Function to capture student image
    def take_image():
        l1 = txt1.get()  # Get enrollment number
        l2 = txt2.get()  # Get name
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")  # Clear the enrollment input field
        txt2.delete(0, "end")  # Clear the name input field

    # Button to capture student image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=GROOVE,
    )
    takeImg.place(relx=0.25, rely=0.8, anchor="center")  # Position the button

    # Function to train the model with captured images
    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Button to train the model
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=GROOVE,
    )
    trainImg.place(relx=0.7, rely=0.8, anchor="center")  # Position the button

# Button to open the "Take Image" UI
r = tk.Button(
    window,
    text="Register new student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(relx=0.1, rely=0.75, anchor="center")  # Position the button

# Function to take attendance
def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

# Button to take attendance
r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(relx=0.5, rely=0.75, anchor="center")  # Position the button

# Function to view attendance
def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

# Button to view attendance
r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(relx=0.9, rely=0.75, anchor="center")  # Position the button

# Run the main application window
window.mainloop()
