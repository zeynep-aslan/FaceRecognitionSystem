from tkinter import *
from tkinter import ttk
import threading
from PIL import Image, ImageTk
import cv2
from datetime import datetime
from tkinter import messagebox
import time
import face_recognition as fr
from configparser import ConfigParser
import numpy as np
import os
import shutil
from collections import OrderedDict

known_face_encondings = []
known_face_names = []
Ids = []
image_path = "known_faces"
TOLERANCE=0.4
frame = ""
top, right, bottom, left = 0, 0, 0, 0
name = "Unknown"
face_locations = []
check = False
thread_check = True
thread_stop = False
'''///////////////////////////////////////'''
cap = cv2.VideoCapture(0)
'''///////////////////////////////////////'''

def addToLabels():
    global known_face_encondings
    global known_face_names
    global Ids

    known_face_encondings = []
    known_face_names = []
    Ids = []
    for file_name in os.listdir(image_path):
        Id = file_name
        Ids.append(Id)
        for filename in os.listdir(f"{image_path}/{file_name}"):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".JPG"):
                # print(filename)
                image = fr.load_image_file(f'{image_path}/{file_name}/{filename}')
                isEncoding = True
                try:
                    encoding = fr.face_encodings(image)[0]
                    known_face_encondings.append(encoding)
                except:
                    isEncoding = False
                if isEncoding:
                    name = os.path.split(filename)[1].split("-")[0]
                    known_face_names.append(name)
    # print(known_face_names)
    # print(Ids)

def run():
    global known_face_encondings
    global known_face_names
    global Ids
    global frame_bg
    global frame
    global top, right, bottom, left
    global name
    global face_locations
    global check
    global thread_stop
    try:
        while root.winfo_exists() and thread_stop:
            global cap
            global tkimage1
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_copy = frame.copy()
                h, w, channels = frame_copy.shape
                rgb_frame = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)

                face_locations = fr.face_locations(rgb_frame)
                face_encodings = fr.face_encodings(rgb_frame, face_locations)
                try:
                    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                        matches = fr.compare_faces(known_face_encondings, face_encoding, TOLERANCE)
                        # print(matches)  #  [True, False, False, False, False, False, False]
                        name = "Unknown"
                        distance = ""
                        face_distances = fr.face_distance(known_face_encondings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        match = matches[best_match_index]

                        if match:
                            name = known_face_names[best_match_index]
                            distance = format(face_distances[best_match_index],".3f")
                        if not check:
                            cv2.rectangle(frame_copy, (left, top), (right, bottom), (0, 255, 0), 2)
                            cv2.rectangle(frame_copy, (left, bottom -35), (right, bottom), (0, 255, 0), cv2.FILLED)
                            cv2.putText(frame_copy, f"{name}  {str(distance)}", (left + 4, bottom - 4), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 255, 255), 2)
                        else:
                            cv2.putText(frame_copy, "lutfen bekleyin", (int(w/10), int(2*h/3)), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 3)
                except:
                    if len(known_face_encondings) != 0 and len(known_face_names) != 0:
                        cv2.putText(frame_copy, "lutfen bekleyin", (int(w/10),int(2*h/3)), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 3)

                '''///////////////////////////////////////'''
                new_rgb_frame = frame_copy.copy() 
                new_rgb_frame = new_rgb_frame[:, :, ::-1]
                img = Image.fromarray(new_rgb_frame)
                img = img.resize((frame_bg.winfo_width(), frame_bg.winfo_height()), Image.BICUBIC)
                tkimage1 = ImageTk.PhotoImage(img)
                if thread_stop:
                    video_label.configure(image=tkimage1)
                    video_label.image = tkimage1
                    video_label.grid(column=0, row=0, sticky=("nsew"))

            elif root.winfo_exists():
                answer = messagebox.askretrycancel("Camera disconnect", "Do you want to try that again?")
                if answer:
                    cap = cv2.VideoCapture(0)
                else:
                    quit_()
            root.protocol("WM_DELETE_WINDOW", destroy_)
            if root.winfo_exists():
                root.update()
        if not thread_stop:
            cap.release()
    except:
        cap.release()
        pass

def quit_():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.quit()

def destroy_():
    quit_()
    return None

def control_password(*args):
    global value1
    global account_passw_warning_lbl
    global account_btn_add
    global isCorrect

    value1 = entry_password.get()
    textt = ""
    if len(value1) < 4:
        textt = "sifreniz cok kisa!!!"
        account_btn_add.config(state=DISABLED)
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    else: isCorrect = True    
    if len(value1) > 11:
        entry_password.set(value1[:12])
        account_btn_add.config(state=DISABLED)
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    else: isCorrect = True    
    account_passw_warning_lbl.config(text=textt)
    account_passw_warning_lbl.grid(column=0, row=2, sticky="n")

def control_name(*args):
    global account_name_warning_lbl
    global face_locations
    global value_name
    global name
    global account_btn_add
    global isCorrect

    value_name = entry_name.get()

    if len(face_locations) > 1:
        account_name_warning_lbl.config(text="kameranin karsisinda birden fazla kisi bulunmamalidir")
        account_name_warning_lbl.grid(column=0, row=5, sticky="n")
        account_btn_add.config(state=DISABLED)  # new
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    elif name in known_face_names:
        account_name_warning_lbl.config(text="kayitli kullaniciyi bir daha ekleyemezsiniz!")
        account_name_warning_lbl.grid(column=0, row=5, sticky="n")
        account_btn_add.config(state=DISABLED)
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    elif " " in value_name:
        account_name_warning_lbl.config(text="isimde bosluk bulunmamalidir")
        account_name_warning_lbl.grid(column=0, row=5, sticky="n") 
        account_btn_add.config(state=DISABLED)
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    elif any(char.isdigit() for char in value_name):  # add special character condition
        account_name_warning_lbl.config(text="isimde sayi bulunmamalidir")
        account_name_warning_lbl.grid(column=0, row=5, sticky="n")
        account_btn_add.config(state=DISABLED)
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = False
    else:
        account_name_warning_lbl.config(text="")
        account_name_warning_lbl.grid(column=0, row=5, sticky="n")
        account_btn_add.config(state="normal")
        account_btn_add.grid(column=2, row=0, sticky="nsew")
        isCorrect = True

def add_user():

    def btn_account_add_clicker(event):
        global value1
        global account_entry_name
        global account_entry_passw
        global value_name

        global account_name_warning_lbl
        global isCorrect

        global known_face_encondings
        global known_face_names
        global Ids
        global frame
        global top, right, bottom, left
        global name
        global face_locations
        global check

        parser = ConfigParser()
        file = "config.ini"
        parser.read(file)
        password = parser.get("account", "password")

        if not isCorrect:
            account_entry_name.delete(0, END)
            account_entry_passw.delete(0, END)
            account_warning_lbl.config(text="Lutfen uyarılara uygun veri girişi yapın!!!", state="normal")
            account_warning_lbl.grid(column=0, row=6, sticky="nsew")

        if value1 != password:
            account_warning_lbl.config(text="Boyle bir kullanici yoktur!!!")
            account_warning_lbl.grid(column=0, row=6, sticky="nsew")
            account_entry_passw.delete(0, END)
            account_entry_name.delete(0, END)
            account_btn_add.config(state="normal")
            account_btn_add.grid(column=2, row=0, sticky="nsew")
        else:
            list_int = map(int, Ids)
            list_int = list(list_int)
            list_int = sorted(list_int)
            biggest_id = list_int[-1]

            for i in range(biggest_id+1):
                if str(i) not in Ids:
                    latest = i
                    break
                if i == biggest_id:
                    latest = i + 1         

            number_of_img = 3
            faces = []
            check = True
            for i in range(number_of_img):
                # print("3")
                account_warning_lbl.config(text="3")
                account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                time.sleep(1)
                # print("2")
                account_warning_lbl.config(text="2")
                account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                time.sleep(1)
                # print("1")
                account_warning_lbl.config(text="1")
                account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                time.sleep(1)
                face_img = frame[top: bottom, left: right]
                try:
                    img_encoding = fr.face_encodings(face_img)[0]
                    faces.append(img_encoding)
                    # print(Ids)
                    try:
                        os.mkdir(f"{image_path}/{latest}")
                    except:
                        pass   
                    # print(Ids) 
                    path = f"{image_path}/{latest}/{value_name}-{i}.jpeg"
                    cv2.imwrite(path, face_img)
                except Exception as e:
                    # print(f"yuz bulunamadi!!, aldigim error: {e}\n")
                    account_warning_lbl.config(text=f"yuz bulunamadi!!, aldigim error: {e}")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
            check = False
            if len(faces) > 0:
                try:
                    known_face_encondings += faces
                    Ids.append(str(latest))
                    for i in faces:
                        known_face_names.append(value_name)
                    account_warning_lbl.config(text=f"kullanici basariyla eklendi! id bilgisi: {latest}")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                except Exception as e:
                    account_warning_lbl.config(text=f"yuz bilgileri eklenemedi!, aldigim error: {e}")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
            else:        
                account_warning_lbl.config(text="yuz bilgileri eklenemedi!!")
                account_warning_lbl.grid(column=0, row=6, sticky="nsew")   

    def btn_account_back_clicker(event):
        pass

    global frame_bg
    global account_passw_warning_lbl
    global value1
    global value_name
    global entry_password
    global entry_name
    global account_name_warning_lbl
    global account_btn_add

    bgg = "#7f8c8d"
    warning_color = "#dc1200"

    user_top = Toplevel(background=bgg)
    # user_top.overrideredirect(True)  # cercevenin cikacagi yeri belirle ve cikis butonu koy
    user_top.wm_title("Kullanici Ekleme Ekrani")
    user_top.minsize(300, 300)
    w = frame_bg.winfo_width()
    h = frame_bg.winfo_height()
    user_top.geometry('%dx%d' % (int(w/4), h))
    user_top.resizable(False, False) 
    user_top.wm_attributes('-topmost', 1)
    user_top.grab_set()

    user_top.columnconfigure(0, weight=1)
    user_top.rowconfigure(0, weight=2)
    user_top.rowconfigure(1, weight=4)
    user_top.rowconfigure(2, weight=1)
    user_top.rowconfigure(3, weight=2)
    user_top.rowconfigure(4, weight=4)
    user_top.rowconfigure(5, weight=1)
    user_top.rowconfigure(6, weight=1)

    user_top.rowconfigure(7, weight=8)
    user_top.rowconfigure(8, weight=4)
    '''////////////////////////////////////////'''

    entry_password = StringVar()
    entry_password.trace('w', control_password)
    entry_name = StringVar()
    entry_name.trace('w', control_name)

    '''////////////////////////////////////////'''
    textt = "* ekranın karşında sisteme eklenecek kullanıcıdan başkası olmamalı\n* isimde boşluk veya özel karakter olmamalı\n* 3 adet resim çekilecektir"
    isCorrect = False

    account_lbl_passw = Label(user_top, text="Sifrenizi Girin: ", font=("bold", 15), border=0, width=25)
    account_lbl_passw.grid(column=0, row=0, sticky="s")

    account_entry_passw = Entry(user_top, textvar=entry_password, highlightthickness=0, border=0, show="*", width=25)
    account_entry_passw.grid(column=0, row=1)

    account_passw_warning_lbl = Label(user_top,  text="Uyarii", font=("bold", 15), fg=warning_color, border=0, width=50)
    # account_passw_warning_lbl.grid(column=0, row=2, sticky="n")

    account_lbl_name = Label(user_top, text="İsminizi Girin: ",  font=("bold", 15), border=0, width=25)
    account_lbl_name.grid(column=0, row=3, sticky="s")

    account_entry_name = Entry(user_top, textvar=entry_name, highlightthickness=0, border=0, width=25)
    account_entry_name.grid(column=0, row=4)

    account_name_warning_lbl = Label(user_top, text="Uyariiii", font=("bold", 15), fg=warning_color, border=0, width=50)
    # account_name_warning_lbl.grid(column=0, row=5, sticky="n")

    account_warning_lbl = Label(user_top, text="Uyariiii", font=("bold", 8), fg=warning_color, border=0, width=50)
    # account_warning_lbl.grid(column=0, row=6, sticky="nsew")

    account_lbl_info =  Label(user_top, text=textt, font=("bold", 15), border=0)
    account_lbl_info.grid(column=0, row=7, sticky="nsew")

    account_lbl_buttons = Label(user_top, border=0)
    account_lbl_buttons.grid(column=0, row=8, sticky="nsew")
    account_lbl_buttons.columnconfigure(0, weight=3)
    account_lbl_buttons.columnconfigure(1, weight=2)
    account_lbl_buttons.columnconfigure(2, weight=3)
    account_lbl_buttons.rowconfigure(0, weight=1)

    account_btn_back = Button(account_lbl_buttons, text="Geri", bg="#9b59b6", border=0, highlightthickness=0, font= "Helvetica 20", activebackground="#7f8c8d")
    account_btn_back.grid(column=0, row=0, sticky="nsew")
    account_btn_back.bind("<Button-1>", btn_account_back_clicker)

    account_btn_add = Button(account_lbl_buttons, text="Ekle", bg="#9b59b6", border=0, highlightthickness=0, font= "Helvetica 20", activebackground="#7f8c8d")
    account_btn_add.grid(column=2, row=0, sticky="nsew")
    account_btn_add.bind("<Button-1>", btn_account_add_clicker)

def delete_user():
    pass

def password_register():
    pass

def door_register():
    pass

def btn_recog_clicker(event):
    global icon_left
    global press
    global t_rec
    global thread_check
    global thread_stop
    global user_top

    if thread_check:
        thread_stop = True
        icon_left = PhotoImage(file=r"icons/left.png")
        icon_left = icon_left.subsample(5, 5)
        btn_recog.config(image=icon_left)
        t_rec = threading.Thread(target=run)
        t_rec.start()
        # time.sleep(2)
        thread_check = False

    else:
        thread_stop = False
        time.sleep(1)
        video_label.configure(image=img1)
        btn_recog.config(image=icon_recog)
        thread_check = True
        
def btn_recog_clicker_main(event):
    global press
    global t_rec
    btn_recog.config(image=icon_recog)
    t_rec.join()
    press += 1

def btn_add_user_clicker(event):
    global thread_check
    global thread_stop
    
    if thread_check:
        thread_stop = True
        t_rec = threading.Thread(target=run)
        t_rec.start()
        thread_check = False
    add_user()

'''///////////////////////////////////////'''
root = Tk()
root.geometry("750x500")
# root.wm_attributes('-topmost', 1)

root.minsize(750, 400)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
press = 0
'''///////////////////////////////////////'''

content = ttk.Frame(root)
content.grid(column=0, row=0, sticky=(N, S, E, W))
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=3)
content.rowconfigure(1, weight=1)
'''///////////////////////////////////////'''

frame_bg = ttk.Frame(content, border=0)
frame_bg.grid(column=0, row=0, sticky=(N, S, E, W))

image = Image.open("orange.jpeg")
img1 = ImageTk.PhotoImage(image)

video_label = Label(frame_bg, image=img1, border=0)
video_label.grid(column=0, row=0, sticky=("nsew"))  ##

'''///////////////////////////////////////'''
options_lbl = Label(content, border=0)
options_lbl.grid(column=0, row=1, sticky="nsew")
options_lbl.columnconfigure(0, weight=1)
options_lbl.columnconfigure(1, weight=1)
options_lbl.columnconfigure(2, weight=1)
options_lbl.columnconfigure(3, weight=1)
options_lbl.columnconfigure(4, weight=1)
options_lbl.rowconfigure(0, weight=1)

icon_recog = PhotoImage(file=r"icons/face-scan.png")
icon_recog = icon_recog.subsample(5, 5)

icon_add = PhotoImage(file=r"icons/add-userr.png")
icon_add = icon_add.subsample(5, 5)

icon_delete = PhotoImage(file=r"icons/delete-user.png")
icon_delete = icon_delete.subsample(5, 5)

icon_door = PhotoImage(file=r"icons/open-door.png")
icon_door = icon_door.subsample(5,5)

icon_passw = PhotoImage(file=r"icons/padlock.png")
icon_passw = icon_passw.subsample(5, 5)


'''///////////////////////////////////////'''
addToLabels()
'''///////////////////////////////////////'''

btn_recog = Button(options_lbl, image=icon_recog, justify="center",padx=4 , border=0, bg="#7bed9f", highlightthickness=0)
btn_recog.bind("<Button-1>", btn_recog_clicker)
'''if press % 2 == 0:
    btn_recog.bind("<Button-1>", btn_recog_clicker)
else:
    btn_recog.bind("<Button-1>", btn_recog_clicker_main)'''

btn_recog.grid(column=0, row=0, sticky="nsew")

btn_user_add = Button(options_lbl, image=icon_add, justify="center",padx=4 , border=0, bg="#70a1ff", highlightthickness=0)
btn_user_add.bind("<Button-1>", btn_add_user_clicker)
btn_user_add.grid(column=1, row=0, sticky="nsew")

btn_user_delete = Button(options_lbl, image=icon_delete, justify="center",padx=4 , border=0, bg="#B33771", highlightthickness=0, command=delete_user)
btn_user_delete.grid(column=2, row=0, sticky="nsew")

btn_door = Button(options_lbl, image=icon_door, justify="center",padx=4 , border=0, bg="#a4b0be", highlightthickness=0, command=door_register)
btn_door.grid(column=3, row=0, sticky="nsew")

btn_passw = Button(options_lbl, image=icon_passw, justify="center",padx=4 , border=0, bg="#A75454", highlightthickness=0, command=password_register)
btn_passw.grid(column=4, row=0, sticky="nsew")


# t0 = threading.Thread(target=run)
# t0.start()
root.mainloop()