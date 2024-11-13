import cv2 as cv
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.messagebox import showinfo
import random
import os

def resize_window(width,height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def runDetectionAlgo():
    selection = category_selected.get().lower()
    if selection == "please select a category":
        showinfo("Error","Please Choose one of the Category")
    else:
        if selection == "cars":
            video_name = "cars_" + str(random.randint(1,6))
        elif selection == "bus":
            video_name = "bus_1"
        elif selection == "two wheeler":
            video_name = "two_wheeler_1"
        else:
            video_name = "pedestrian_" + str(random.randint(1,2))
        cap = cv.VideoCapture('../assets/Video Files/' + video_name + '.mp4')
        classifier = cv.CascadeClassifier('../assets/Trained XML Files/' + selection.replace(" ","_") + '.xml')
        
        while cap.isOpened():
            ret,frame = cap.read()
            if ret == True:
                frame = cv.resize(frame,(600,400))
                grey_image = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                detected_objects = classifier.detectMultiScale(grey_image,1.1,1)
                for (x,y,w,h) in detected_objects:
                    cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
                cv.imshow("Road Object Detection",frame)

                key = cv.waitKey(25)
                if key in [8, 13, 27, 32, ord('q'), ord('p')]:
                    break
            else:
                break
        
        cap.release()
        cv.destroyAllWindows()

window = tk.Tk()
window.title('Road Object Detection')
resize_window(400,200)
window.wm_iconbitmap('../assets/Logo/Detection.ico')
window.resizable(False,False)
window.configure(bg="#53868B")

heading = tk.Label(window, text="Road Object Detection", font=("Arial",18,"bold"), fg="white", bg="#53868B")
heading.pack(side="top", pady=(20,10))

normal_font = tkFont.Font(family="Arial",size=10,weight=tkFont.NORMAL)

detection_algo_list = os.listdir('../assets/Trained XML Files/')
categories_name = ['Cars','Bus','Two Wheeler','Pedestrian']
video_list = os.listdir('../assets/Video Files/')

category_selected = tk.StringVar(value="Please Select a Category")

category_style = ttk.Style()
category_style.theme_use("clam")
category_style.configure("Custom.TCombobox", font=("Arial", 12), foreground="black", background="lightgrey")
category_combobox = ttk.Combobox(window, textvariable=category_selected, values=categories_name, style="Custom.TCombobox", width=40)
category_combobox.pack(pady=20)

tk.Button(window, text="Detect", font=normal_font, bg="#000000", fg="#ffffff", command=runDetectionAlgo, cursor="hand2", padx=10, pady=2).pack(padx=20)

window.mainloop()