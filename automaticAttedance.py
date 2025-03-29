# Importing required libraries
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
import tkinter.ttk as tkk
import tkinter.font as font

# File paths for required resources
haarcasecade_path = "haarcascade_frontalface_default.xml"  # Path to Haar Cascade XML file for face detection
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"  # Path to trained model file
trainimage_path = "TrainingImage"  # Path to folder containing training images
studentdetail_path = "StudentDetails\\studentdetails.csv"  # Path to CSV file containing student details
attendance_path = "Attendance"  # Path to folder where attendance records will be stored

# Function to choose a subject and fill attendance
def subjectChoose(text_to_speech):
    # Nested function to handle attendance filling
    def FillAttendance():
        sub = tx.get()  # Get the subject name from the input field
        now = time.time()  # Current timestamp
        future = now + 20  # Set a 20-second time limit for attendance
        print(now)
        print(future)
        if sub == "":  # Check if the subject name is empty
            t = "Please enter the subject name!!!"
            text_to_speech(t)  # Notify the user to enter a subject name
        else:
            try:
                # Initialize face recognizer
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)  # Load the trained model
                except:
                    # Notify if the model is not found
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return

                # Load Haar Cascade for face detection
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                # Read student details from CSV
                df = pd.read_csv(studentdetail_path)
                # Open webcam for capturing video
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX  # Font for displaying text on video
                col_names = ["Enrollment", "Name"]  # Columns for attendance DataFrame
                attendance = pd.DataFrame(columns=col_names)  # Initialize attendance DataFrame

                while True:
                    # Capture frame-by-frame
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)  # Detect faces in the frame

                    for (x, y, w, h) in faces:
                        global Id
                        # Predict the ID of the detected face
                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:  # Confidence threshold for valid recognition
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()  # Get the subject name
                            ts = time.time()  # Current timestamp
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )  # Current date
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )  # Current time
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values  # Get student name
                            global tt
                            tt = str(Id) + "-" + aa  # Combine ID and name
                            attendance.loc[len(attendance)] = [Id, aa]  # Add to attendance DataFrame
                            # Draw rectangle around the face and display ID and name
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            # Handle unknown faces
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )

                    if time.time() > future:  # Stop after 20 seconds
                        break

                    # Remove duplicate entries in attendance
                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)  # Display video feed
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:  # Exit on pressing 'Esc'
                        break

                # Save attendance to a CSV file
                ts = time.time()
                attendance[date] = 1  # Mark attendance for the current date
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)  # Create folder for the subject
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)  # Save attendance to CSV

                # Notify user of successful attendance filling
                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()  # Release the webcam
                cv2.destroyAllWindows()  # Close all OpenCV windows

                # Display attendance in a new window
                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            except:
                # Notify user if no face is found
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    # Create a new window for subject selection
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title label
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)

    # Notification label
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    # Function to open attendance folder for the selected subject
    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    # Button to check attendance sheets
    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    # Label and input field for subject name
    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    # Button to fill attendance
    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()  # Run the subject selection window
