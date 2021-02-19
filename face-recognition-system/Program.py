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
name = ""
face_locations = []
check = False
thread_check = True
thread_stop = False
img_path = "icons"
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
    for file_name in os.listdir(image_path):  # image_path yoksa diye try except koy
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
    global frame_copy
    global new_rgb_frame
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
                        name = ""
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
                    if len(known_face_encondings) != 0 and len(known_face_names) != 0:  #
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
                cap = cv2.VideoCapture(0)
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

def keyboard(keyboard_lbl, keyboard_entry):

    buttoncolor_char = "#107dac"
    buttoncolor_num = "#4cd137"
    font= "Helvetica 20"

    keyBoard_list = {
    '0': ['Q','W','E','R','T','Y','U','I','O','P','7','8','9'],
    '1': ['A','S','D','F','G','H','J','K','L','İ','4','5','6'],
    '2': ['Z','X','C','V','B','N','M','Ö','Ç','0','1','2','3']
    }

    row0 = keyBoard_list['0']
    row1 = keyBoard_list['1']
    row2 = keyBoard_list['2']

    keyboard_lbl.columnconfigure(0, weight=2)  # bos
    keyboard_lbl.columnconfigure(1, weight=2)
    keyboard_lbl.columnconfigure(2, weight=2)
    keyboard_lbl.rowconfigure(0, weight=2)  # bos
    keyboard_lbl.rowconfigure(1, weight=2)
    keyboard_lbl.rowconfigure(2, weight=2)
    keyboard_lbl.rowconfigure(3, weight=2)
    keyboard_lbl.rowconfigure(4, weight=2)
    keyboard_lbl.rowconfigure(5, weight=2)
    keyboard_lbl.rowconfigure(6, weight=2)
    keyboard_lbl.rowconfigure(7, weight=2)
    keyboard_lbl.rowconfigure(8, weight=2)
    keyboard_lbl.rowconfigure(9, weight=2)
    keyboard_lbl.rowconfigure(10, weight=2)
    keyboard_lbl.rowconfigure(11, weight=2)
    keyboard_lbl.rowconfigure(12, weight=2)

    b0_0 = Button(keyboard_lbl, text=row0[0], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[0]))
    b0_0.grid(row=0, column=0)

    b0_1 = Button(keyboard_lbl, text=row0[1],bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[1]))
    b0_1.grid(row=0, column=1)

    b0_2 = Button(keyboard_lbl, text=row0[2], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[2]))
    b0_2.grid(row=0, column=2)

    b0_3 = Button(keyboard_lbl, text=row0[3], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[3]))
    b0_3.grid(row=0, column=3)

    b0_4 = Button(keyboard_lbl, text=row0[4],bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[4]))
    b0_4.grid(row=0, column=4)

    b0_5 = Button(keyboard_lbl, text=row0[5], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[5]))
    b0_5.grid(row=0, column=5)

    b0_6 = Button(keyboard_lbl, text=row0[6], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[6]))
    b0_6.grid(row=0, column=6)

    b0_7 = Button(keyboard_lbl, text=row0[7],bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[7]))
    b0_7.grid(row=0, column=7)

    b0_8 = Button(keyboard_lbl, text=row0[8], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[8]))
    b0_8.grid(row=0, column=8)

    b0_9 = Button(keyboard_lbl, text=row0[9], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[9]))
    b0_9.grid(row=0, column=9)

    b0_10 = Button(keyboard_lbl, text=row0[10], bg=buttoncolor_num, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[10]))
    b0_10.grid(row=0, column=10)

    b0_11 = Button(keyboard_lbl, text=row0[11],bg=buttoncolor_num,border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[11]))
    b0_11.grid(row=0, column=11)

    b0_12 = Button(keyboard_lbl, text=row0[12], bg=buttoncolor_num,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row0[12]))
    b0_12.grid(row=0, column=12)
    '''///////////////////////////////////////////////'''
    b1_0 = Button(keyboard_lbl, text=row1[0], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
            font=font, command=lambda: keyboard_entry.insert(END, row1[0]))
    b1_0.grid(row=1, column=0)

    b1_1 = Button(keyboard_lbl, text=row1[1],bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[1]))
    b1_1.grid(row=1, column=1)

    b1_2 = Button(keyboard_lbl, text=row1[2], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[2]))
    b1_2.grid(row=1, column=2)

    b1_3 = Button(keyboard_lbl, text=row1[3], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[3]))
    b1_3.grid(row=1, column=3)

    b1_4 = Button(keyboard_lbl, text=row1[4],bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[4]))
    b1_4.grid(row=1, column=4)

    b1_5 = Button(keyboard_lbl, text=row1[5], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[5]))
    b1_5.grid(row=1, column=5)

    b1_6 = Button(keyboard_lbl, text=row1[6], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[6]))
    b1_6.grid(row=1, column=6)

    b1_7 = Button(keyboard_lbl, text=row1[7],bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[7]))
    b1_7.grid(row=1, column=7)

    b1_8 = Button(keyboard_lbl, text=row1[8], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[8]))
    b1_8.grid(row=1, column=8)

    b1_9 = Button(keyboard_lbl, text=row1[9], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[9]))
    b1_9.grid(row=1, column=9)

    b1_10 = Button(keyboard_lbl, text=row1[10], bg=buttoncolor_num,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[10]))
    b1_10.grid(row=1, column=10)

    b1_11 = Button(keyboard_lbl, text=row1[11],bg=buttoncolor_num, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[11]))
    b1_11.grid(row=1, column=11)

    b1_12 = Button(keyboard_lbl, text=row1[12], bg=buttoncolor_num,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row1[12]))
    b1_12.grid(row=1, column=12)
    '''///////////////////////////////////////////////'''
    b2_0 = Button(keyboard_lbl, text=row2[0], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
            font=font, command=lambda: keyboard_entry.insert(END, row2[0]))
    b2_0.grid(row=2, column=0)

    b2_1 = Button(keyboard_lbl, text=row2[1],bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[1]))
    b2_1.grid(row=2, column=1)

    b2_2 = Button(keyboard_lbl, text=row2[2], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[2]))
    b2_2.grid(row=2, column=2)

    b2_3 = Button(keyboard_lbl, text=row2[3], bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[3]))
    b2_3.grid(row=2, column=3)

    b2_4 = Button(keyboard_lbl, text=row2[4],bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[4]))
    b2_4.grid(row=2, column=4)

    b2_5 = Button(keyboard_lbl, text=row2[5], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[5]))
    b2_5.grid(row=2, column=5)

    b2_6 = Button(keyboard_lbl, text=row2[6], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[6]))
    b2_6.grid(row=2, column=6)

    b2_7 = Button(keyboard_lbl, text=row2[7],bg=buttoncolor_char,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[7]))
    b2_7.grid(row=2, column=7)

    b2_8 = Button(keyboard_lbl, text=row2[8], bg=buttoncolor_char, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[8]))
    b2_8.grid(row=2, column=8)

    b2_9 = Button(keyboard_lbl, text=row2[9], bg=buttoncolor_num,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[9]))
    b2_9.grid(row=2, column=9)

    b2_10 = Button(keyboard_lbl, text=row2[10], bg=buttoncolor_num,  border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[10]))
    b2_10.grid(row=2, column=10)

    b2_11 = Button(keyboard_lbl, text=row2[11],bg=buttoncolor_num, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[11]))
    b2_11.grid(row=2, column=11)

    b2_12 = Button(keyboard_lbl, text=row2[12], bg=buttoncolor_num, border=0, highlightthickness=0, activebackground=buttoncolor_char,
                font=font, command=lambda: keyboard_entry.insert(END, row2[12]))
    b2_12.grid(row=2, column=12)

def add_user():
    
    def activateEntryName(lbl, entry):
        # global account_entry_passw
        # global account_entry_name
        account_entry_passw.configure(state=DISABLED)
        account_entry_name.configure(state=NORMAL)
        keyboard(lbl, entry)
    def btn_account_add_clicker(event):
        global value1
        # global account_entry_name
        # global account_entry_passw
        global value_name

        global account_name_warning_lbl
        global isCorrect

        # global keyboard_lbl
        # global account_entry_passw

        global known_face_encondings
        global known_face_names
        global Ids
        global frame
        global top, right, bottom, left
        global name
        global face_locations
        global check
        global new_rgb_frame
        global frame_copy

        parser = ConfigParser()
        file = "config.ini"
        parser.read(file)
        password = parser.get("account", "password")
        print(len(account_entry_name.get()))
        print("00")
        if not isCorrect:
            print("11")
            account_entry_name.delete(0, END)
            account_entry_passw.delete(0, END)
            account_warning_lbl.config(text="Lutfen uyarılara uygun veri girişi yapın!!!", state="normal")
            account_warning_lbl.grid(column=0, row=6, sticky="nsew")
            print("22")
        print("33")
        if value1 != password:
            account_warning_lbl.config(text="Hatalı şifre!!!")
            account_warning_lbl.grid(column=0, row=6, sticky="nsew")
            account_entry_passw.delete(0, END)
            account_entry_name.delete(0, END)
            account_btn_add.config(state="normal")
            account_btn_add.grid(column=2, row=0, sticky="nsew")
        else:
            if len(account_entry_name.get())==0 and isCorrect:
                activateEntryName(keyboard_lbl, account_entry_name)  # bunun icindeki keyboard() i ayri verebilirim
            else:
                print("44")
                list_int = map(int, Ids)
                list_int = list(list_int)
                list_int = sorted(list_int)
                try:
                    biggest_id = list_int[-1]
                except:
                    biggest_id = 0

                for i in range(biggest_id+1):
                    if str(i) not in Ids:
                        latest = i
                        break
                    if i == biggest_id:
                        latest = i + 1         
                print("55")
                number_of_img = 3
                faces = []
                check = True
                for i in range(number_of_img):
                    print("66")
                    account_warning_lbl.config(text="3")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                    time.sleep(1)
                    account_warning_lbl.config(text="2")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                    time.sleep(1)
                    account_warning_lbl.config(text="1")
                    account_warning_lbl.grid(column=0, row=6, sticky="nsew")
                    time.sleep(1)
                    # new_rgb_frame = new_rgb_frame[:, :, ::-1]
                    face_img = frame[top: bottom, left: right]
                    print("88")
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
    def delete_char():
        account_entry_name.delete(len(account_entry_name.get()) - 1, END)
        account_entry_passw.delete(len(account_entry_passw.get()) - 1, END)
    def control_name(*args):
        global account_name_warning_lbl
        global face_locations
        global value_name
        global name
        global account_btn_add
        global isCorrect
        global account_warning_lbl 

        value_name = entry_name.get()
        print(known_face_names)
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
        else:
            account_btn_add.config(state=NORMAL)
            account_btn_add.grid(column=2, row=0, sticky="nsew")
            isCorrect = True    
        if len(value1) > 11:
            entry_password.set(value1[:12])
            isCorrect = False
        else:
            account_btn_add.config(state=NORMAL)
            account_btn_add.grid(column=2, row=0, sticky="nsew")
            isCorrect = True    
        account_passw_warning_lbl.config(text=textt)
        account_passw_warning_lbl.grid(column=0, row=2, sticky="n")

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
    buttoncolor_char = "#107dac"
    buttoncolor_num = "#4cd137"
    font= "Helvetica 20"
    button_color = "#9b59b6"

    user_top = Toplevel(background=bgg)
    user_top.overrideredirect(True)  # cercevenin cikacagi yeri belirle ve cikis butonu koy
    user_top.minsize(300, 300)
    w = frame_bg.winfo_width()
    h = frame_bg.winfo_height()
    user_top.geometry('%dx%d+%d+%d' % (int((0.3*w)), h, int(0.7*w), int(0)))
    user_top.resizable(False, False) 
    user_top.wm_attributes('-topmost', 1)
    user_top.grab_set()

    # print(user_top.winfo_geometry())

    user_top.columnconfigure(0, weight=1)
    user_top.rowconfigure(0, weight=2)
    user_top.rowconfigure(1, weight=4)
    user_top.rowconfigure(2, weight=1)
    user_top.rowconfigure(3, weight=2)
    user_top.rowconfigure(4, weight=4)
    user_top.rowconfigure(5, weight=1)
    user_top.rowconfigure(6, weight=1)

    user_top.rowconfigure(7, weight=8)
    user_top.rowconfigure(8, weight=16)
    user_top.rowconfigure(4, weight=4)
    '''////////////////////////////////////////'''

    entry_password = StringVar()
    entry_password.trace('w', control_password)
    entry_name = StringVar()
    entry_name.trace('w', control_name)

    '''////////////////////////////////////////'''
    text1 = "* ekranın karşında 1 kişi olmalı"
    text2 = "* isimde boşluk veya özel karakter olmamalı"
    text3 = "* 3 adet resim çekilecektir"
    
    isCorrect = False

    account_lbl_passw = Label(user_top, text="Sifrenizi Girin: ", bg=bgg, font=("bold", 15), border=0, width=25)
    account_lbl_passw.grid(column=0, row=0, sticky="s")

    account_entry_passw = Entry(user_top, textvar=entry_password, highlightthickness=0, border=0, show="*", disabledbackground=buttoncolor_char, width=25)
    account_entry_passw.grid(column=0, row=1)

    account_passw_warning_lbl = Label(user_top,  text="Uyarii", bg=bgg, font=("bold", 15), fg=warning_color, border=0, width=50)
    # account_passw_warning_lbl.grid(column=0, row=2, sticky="n")
    '''///////////////////////////////////////'''
    account_lbl_name = Label(user_top, text="İsminizi Girin: ", bg=bgg,  font=("bold", 15), border=0, width=25)
    account_lbl_name.grid(column=0, row=3, sticky="s")

    account_entry_name = Entry(user_top, textvar=entry_name, highlightthickness=0, state=DISABLED, border=0, width=25)
    account_entry_name.grid(column=0, row=4)

    account_name_warning_lbl = Label(user_top, text="Uyariiii", bg=bgg, font=("bold", 15), fg=warning_color, border=0, width=50)
    # account_name_warning_lbl.grid(column=0, row=5, sticky="n")

    account_warning_lbl = Label(user_top, text="Uyariiii", bg=bgg, font=("bold", 12), fg=warning_color, border=0, width=50)
    # account_warning_lbl.grid(column=0, row=6, sticky="nsew")

    account_lbl_info =  Label(user_top, text=f"{text1}\n{text2}\n{text3}", bg=bgg, font=("bold", 13), border=0)
    account_lbl_info.grid(column=0, row=7, sticky="nsew")
    '''///////////////////////////////////////////////'''
    keyboard_lbl = Label(user_top, border=0, bg=buttoncolor_char)
    keyboard_lbl.grid(column=0, row=8, sticky="nsew")

    keyboard(keyboard_lbl, account_entry_passw)

    '''////////////////////////////////////////'''
    account_lbl_buttons = Label(user_top, border=0, bg=bgg)
    account_lbl_buttons.grid(column=0, row=9, sticky="nsew")
    account_lbl_buttons.columnconfigure(0, weight=1)
    account_lbl_buttons.columnconfigure(1, weight=1)
    account_lbl_buttons.columnconfigure(2, weight=1)
    account_lbl_buttons.rowconfigure(0, weight=1)

    account_btn_back = Button(account_lbl_buttons, text="Kapat", bg=button_color, border=0, highlightthickness=0, font=font, command=user_top.destroy)
    account_btn_back.grid(column=0, row=0, sticky="nsew")

    account_btn_delete = Button(account_lbl_buttons, text="Sil", bg=button_color, border=0, highlightthickness=0, font=font, command=delete_char)
    account_btn_delete.grid(column=1, row=0, sticky="nsew")

    account_btn_add = Button(account_lbl_buttons, text="Ekle", bg=button_color, border=0, highlightthickness=0, font=font)
    account_btn_add.grid(column=2, row=0, sticky="nsew")
    account_btn_add.bind("<Button-1>", btn_account_add_clicker)

def delete_user():

    def delete_char_del_user():
        entry_passw_del_user.delete(len(entry_passw_del_user.get()) - 1, END)
        entry_id_del_user.delete(len(entry_id_del_user.get()) - 1, END)
    def delete_userr(iddd):
        try: 
            path = f"{image_path}/{iddd}"
            shutil.rmtree(path)
            warning_lbl_cam_del_user.configure(text=f"{iddd} id li {name} kullanicisinin yuz verilerini silme islemi basariyla gerceklesti",bg=bgg)  
            warning_lbl_cam_del_user.grid(column=0, row=3, sticky="s")
            addToLabels()
            entry_passw_del_user.configure(state=NORMAL)
            btn_cam.configure(state=DISABLED)
            btn_cam.grid(column=0, row=0)
            entry_passw_del_user.delete(0, END)
            entry_id_del_user.delete(0, END)
            entry_id_del_user.configure(state=DISABLED)
        except Exception as e:
            warning_lbl_cam_del_user.configure(text="kullanici silinemedi",bg=bgg) 
            warning_lbl_cam_del_user.grid(column=0, row=3, sticky="s")
    def activateEntryId():
        entry_passw_del_user.configure(state=DISABLED)
        entry_id_del_user.configure(state=NORMAL)
        btn_del_user.configure(text="Id İle Sil")
        warning_lbl_del_user.configure(text="",bg=bgg)  
        keyboard(keyboard_lbl_del_user, entry_id_del_user)
    def delete_user_cam_clicker(event):
        
        textt = ""
        if len(face_locations) > 1:
            textt = "KAMERANIN KARŞISINDA BİRDEN FAZLA KİŞİ BULUNMAMALIDIR!!!"
        
        elif len(face_locations) == 1:
            print(known_face_names)
            if len(known_face_names)==0:  textt = "SİSTEME KAYITLI KULLANICI OLMADIĞINDAN SİLME İŞLEMİ YAPILAMIYOR!!!"
            else:
                name_list = []
                name_list = list(OrderedDict.fromkeys(known_face_names))
                for nme, idd in zip(name_list, Ids):
                    if nme == name:
                        delete_userr(idd)
                        break   
        else:
            textt = "KAMERANIN KARŞISINDA YUZ BULUNMAMAKTADIR!!!"
        warning_lbl_cam_del_user.configure(text=textt)
        warning_lbl_cam_del_user.grid(column=0, row=3, sticky="s")
    def btn_del_user_clicker(event):
        
        warning_text = ""
        parser.read(filee)
        password = parser.get("account", "password")  # her seferinde okumadan yapmanin yoluna bak

        if entry_passw_del_user.get() == password and len(entry_id_del_user.get())==0:
            warning_lbl_id_del_user.config(text="")
            warning_lbl_id_del_user.grid(column=0, row=5, sticky="n")
            btn_cam.configure(state=NORMAL)
            btn_cam.grid(column=0, row=0)
            activateEntryId()
        elif entry_passw_del_user.get() != password and len(entry_passw_del_user.get())>0:
            warning_text = "ŞİFRE YANLIŞ!!!"
            entry_passw_del_user.delete(0, END)
        if entry_id_del_user.get() not in Ids and len(entry_id_del_user.get())>0:
            warning_text = "GEÇERSİZ ID GİRİŞİ"
            entry_id_del_user.delete(0, END)  # burada girilen id listede degilse sifre silinebilir
        elif entry_id_del_user.get() in Ids and len(entry_id_del_user.get())>0:
            delete_userr(entry_id_del_user.get())

        if len(warning_text)==0:  
            warning_lbl_del_user.configure(text=warning_text,bg=bgg)   
            warning_lbl_del_user.grid(column=0, row=6, sticky="nsew")

        else:  
            warning_lbl_del_user.configure(text=warning_text, bg="#639a67")      # renklere bak
            warning_lbl_del_user.grid(column=0, row=6, sticky="nsew")
    def control_password_del_user(*args):

        btn_del_user.configure(text="Enter")
        warning_lbl_del_user.configure(text="",bg=bgg)   
        # warning_lbl_del_user.grid(column=0, row=6, sticky="nsew")

        password_del_user = var_password_del_user.get()
        if len(password_del_user) < 4:
            btn_del_user.config(state=DISABLED)
            btn_del_user.grid(column=2, row=0, sticky="nsew")
        else:
            btn_del_user.config(state=NORMAL)
            btn_del_user.grid(column=2, row=0, sticky="nsew")
        if len(password_del_user) > 11:
            var_password_del_user.set(password_del_user[:12])
        else:
            btn_del_user.config(state=NORMAL)
            btn_del_user.grid(column=2, row=0, sticky="nsew")    
    def control_id(*args):

        textt = ""
        id_del_user = var_id.get()
        if not id_del_user.isnumeric():  # id rakam olamaz
            textt = "Id sayi olmalidir!!!"
            btn_del_user.config(state=DISABLED)
            btn_del_user.grid(column=2, row=0, sticky="nsew")
        else:
            btn_del_user.config(state=NORMAL)
            btn_del_user.grid(column=2, row=0, sticky="nsew")    
        warning_lbl_id_del_user.configure(text=textt)
        warning_lbl_id_del_user.grid(column=0, row=5, sticky="n")

    global frame_bg
    global Ids
    global face_locations
    global known_face_names
    global name

    bgg = "#9c88ff"
    warning_color = "#fbc531"
    btn_color = "#9b59b6"
    
    parser = ConfigParser()
    filee = "config.ini"
    parser.read(filee)
    password = parser.get("account", "password")

    del_user_top = Toplevel(background=bgg)
    del_user_top.overrideredirect(True)
    w = frame_bg.winfo_width()
    h = frame_bg.winfo_height()
    del_user_top.geometry('%dx%d+%d+%d' % (int((0.3*w)), h, int(0.7*w), int(0)))
    del_user_top.resizable(False, False) 
    del_user_top.wm_attributes('-topmost', 1)
    del_user_top.grab_set()

    del_user_top.columnconfigure(0, weight=1)
    del_user_top.rowconfigure(0, weight=2)
    del_user_top.rowconfigure(1, weight=2)
    del_user_top.rowconfigure(2, weight=4)
    del_user_top.rowconfigure(3, weight=2)
    del_user_top.rowconfigure(4, weight=4)
    del_user_top.rowconfigure(5, weight=1)
    del_user_top.rowconfigure(6, weight=2)
    del_user_top.rowconfigure(7, weight=8)
    del_user_top.rowconfigure(8, weight=12)
    del_user_top.rowconfigure(9, weight=3)

    '''////////////////////////////////////////'''
    var_password_del_user = StringVar()
    var_password_del_user.trace('w', control_password_del_user)
    var_id = StringVar()
    var_id.trace('w', control_id)

    '''////////////////////////////////////////'''
    text1 = "* silinecek kişi kamera önunde olmalıdır"
    text2 = "* sabit durunuz"
    
    lbl_empty_del_user = Label(del_user_top, bg=bgg, border=0, width=25)
    lbl_empty_del_user.grid(column=0, row=0)

    lbl_passw_del_user = Label(del_user_top, text="Şifrenizi Girin: ", bg=bgg, font=("bold", 15), border=0, width=25)
    lbl_passw_del_user.grid(column=0, row=1, sticky="nsew")

    entry_passw_del_user = Entry(del_user_top, textvar=var_password_del_user, highlightthickness=0, border=0, show="*", width=25)
    entry_passw_del_user.grid(column=0, row=2, sticky="n")

    lbl_id_del_user = Label(del_user_top, text="Id Girin: ", bg=bgg,  font=("bold", 15), border=0, width=25)
    lbl_id_del_user.grid(column=0, row=3, sticky="nsew")

    entry_id_del_user = Entry(del_user_top, textvar=var_id, highlightthickness=0, state=DISABLED, show="*", border=0, width=25)
    entry_id_del_user.grid(column=0, row=4, sticky="n")

    warning_lbl_id_del_user = Label(del_user_top, text="", bg=bgg, font=("bold", 15), fg=warning_color, border=0, width=50)
    warning_lbl_id_del_user.grid(column=0, row=5, sticky="n")

    warning_lbl_del_user = Label(del_user_top, text="", bg=bgg, font=("bold", 12), fg=warning_color, border=0, width=50)
    warning_lbl_del_user.grid(column=0, row=6, sticky="nsew")
    '''////////////////////////////////////////'''
    lbl_cam_del_user =  Label(del_user_top, bg=bgg, font=("bold", 13), border=0)
    lbl_cam_del_user.grid(column=0, row=7, sticky="n")

    lbl_cam_del_user.columnconfigure(0, weight=1)
    lbl_cam_del_user.rowconfigure(0, weight=1)
    lbl_cam_del_user.rowconfigure(1, weight=1)
    lbl_cam_del_user.rowconfigure(2, weight=1)
    lbl_cam_del_user.rowconfigure(3, weight=1)

    btn_cam = Button(lbl_cam_del_user, text="Kamera İle Sil", bg=btn_color, state=DISABLED, border=0, highlightthickness=0, font="Helvetica 20")
    btn_cam.bind("<Button-1>", delete_user_cam_clicker)
    btn_cam.grid(column=0, row=0)

    lbl_empty_del_user2 = Label(lbl_cam_del_user, bg=bgg, border=0, width=10)
    lbl_empty_del_user2.grid(column=0, row=1)

    lbl_info_del_user = Label(lbl_cam_del_user, text=f"{text1}\n{text2}", bg=bgg, font=("bold", 14), fg=warning_color, border=0, width=80)
    lbl_info_del_user.grid(column=0, row=2, sticky="s")

    warning_lbl_cam_del_user = Label(lbl_cam_del_user, text="", bg=bgg, font=("bold", 14), fg=warning_color, border=0, width=80)
    warning_lbl_cam_del_user.grid(column=0, row=3, sticky="s")

    '''////////////////////////////////////////'''
    keyboard_lbl_del_user = Label(del_user_top, border=0, bg=bgg)
    keyboard_lbl_del_user.grid(column=0, row=8, sticky="nsew")
    keyboard(keyboard_lbl_del_user, entry_passw_del_user)
    '''////////////////////////////////////////'''
    lbl_buttons_del_user = Label(del_user_top, border=0)
    lbl_buttons_del_user.grid(column=0, row=9, sticky="nsew")
    lbl_buttons_del_user.columnconfigure(0, weight=1)
    lbl_buttons_del_user.columnconfigure(1, weight=1)
    lbl_buttons_del_user.columnconfigure(2, weight=1)
    lbl_buttons_del_user.rowconfigure(0, weight=1)

    btn_back = Button(lbl_buttons_del_user, text="Kapat", bg=btn_color, border=0, highlightthickness=0, font= "Helvetica 20", command=del_user_top.destroy)
    btn_back.grid(column=0, row=0, sticky="nsew")

    btn_delete = Button(lbl_buttons_del_user, text="Sil", bg=btn_color, border=0, highlightthickness=0, font="Helvetica 20", command=delete_char_del_user)
    btn_delete.grid(column=1, row=0, sticky="nsew")

    btn_del_user = Button(lbl_buttons_del_user, text="Enter", bg=btn_color, border=0, highlightthickness=0, font= "Helvetica 20")
    btn_del_user.grid(column=2, row=0, sticky="nsew")
    btn_del_user.bind("<Button-1>", btn_del_user_clicker)

def password_register():
    
    def delete_char():
        entry_passw.delete(len(entry_passw.get()) - 1, END)
        entry_new_passw.delete(len(entry_new_passw.get()) - 1, END)
        entry_again_new_passw.delete(len(entry_again_new_passw.get()) - 1, END)
    def activateEntryNewPassword():
        entry_passw.configure(state=DISABLED)
        entry_new_passw.configure(state=NORMAL)
        keyboard(keyboard_lbl, entry_new_passw)
    def activateEntryAgainNewPassword():
        entry_new_passw.configure(state=DISABLED)
        entry_again_new_passw.configure(state=NORMAL)
        keyboard(keyboard_lbl, entry_again_new_passw)
    def control_old_password(*args):

        btn_change_passw.configure(text="Enter")
        warning_lbl.configure(text="",bg=bgg)    
        password1 = var_password.get()
        if len(password1) < 4:
            btn_change_passw.config(state=DISABLED)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        if len(password1) > 11:
            var_password.set(password1[:12])
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
    def control_new_password(*args):

        warning_lbl.configure(text="",bg=bgg)    
        password2 = var_new_password.get()
        textt = ""
        if len(password2) == 0:
            btn_change_passw.config(state=DISABLED)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        elif len(password2) < 4:
            textt = "sifreniz cok kisa!!!"
            btn_change_passw.config(state=DISABLED)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        if len(password2) > 11:
            textt = "şifreniz daha uzun olamaz!!!"
            var_new_password.set(password2[:12])
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        warning_lbl_new_passw.config(text=textt)
        warning_lbl_new_passw.grid(column=0, row=4, sticky="n")
    def control_again_new_password(*args):
        
        btn_change_passw.configure(text="Kaydet")
        warning_lbl.configure(text="",bg=bgg)    
        password3 = var_again_new_password.get()
        textt = ""
        if len(password3) == 0:
            btn_change_passw.config(state=DISABLED)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        elif len(password3) < 4:
            textt = "şifreniz cok kisa!!!"
            btn_change_passw.config(state=DISABLED)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        if len(password3) > 11:
            textt = "şifreniz daha uzun olamaz!!!"
            var_again_new_password.set(password3[:12])
        else:
            btn_change_passw.config(state=NORMAL)
            btn_change_passw.grid(column=2, row=0, sticky="nsew")
        warning_lbl_again_new_passw.config(text=textt)
        warning_lbl_again_new_passw.grid(column=0, row=7, sticky="n")
    def changePassword():

        parser.set("account", "password", entry_again_new_passw.get())
        with open("config.ini", 'w') as configfile:
            parser.write(configfile)
        
        entry_passw.configure(state=NORMAL)
        entry_new_passw.configure(state=NORMAL)
        entry_again_new_passw.configure(state=NORMAL)
        entry_passw.delete(0, END)
        entry_new_passw.delete(0, END)
        entry_again_new_passw.delete(0, END)
        entry_new_passw.configure(state=DISABLED)
        entry_again_new_passw.configure(state=DISABLED)
        keyboard(keyboard_lbl, entry_passw)
    def btn_change_password_clicker(event):
        warning_text = ""
        parser.read(filee)
        password = parser.get("account", "password")

        if entry_passw.get() == password and len(entry_new_passw.get())==0 and len(entry_again_new_passw.get())==0:
            warning_lbl_new_passw.config(text="")
            warning_lbl_new_passw.grid(column=0, row=4, sticky="n")
            # warning_lbl_again_new_passw.config(text="")
            # warning_lbl_again_new_passw.grid(column=0, row=7, sticky="n")
            activateEntryNewPassword()
        elif entry_passw.get() != password and len(entry_passw.get())>0:
            warning_text = "ŞİFRE YANLIŞ!!!"
            entry_passw.delete(0, END)
        if entry_passw.get() != entry_new_passw.get() and len(entry_new_passw.get())>3 and len(entry_new_passw.get())<13:  # 4-12
            warning_lbl_again_new_passw.config(text="")
            warning_lbl_again_new_passw.grid(column=0, row=7, sticky="n")
            activateEntryAgainNewPassword()
        elif entry_passw.get() == entry_new_passw.get() and len(entry_passw.get())>0:
            warning_text = "YENİ ŞİFRE ESKİ ŞİFREYLE AYNI OLAMAZ!!!"
            entry_new_passw.delete(0, END)
        if len(entry_again_new_passw.get())>3 and len(entry_again_new_passw.get())<13 and entry_again_new_passw.get()==entry_new_passw.get():
            warning_text = "ŞİFRE DEĞİŞTİRİLDİ!!!"
            changePassword()
        elif len(entry_new_passw.get())>3 and len(entry_new_passw.get())<13 and entry_again_new_passw.get()!=entry_new_passw.get() and len(entry_again_new_passw.get())>0:
            warning_text = "2.GİRDİĞİNİZ YENİ ŞİFRE İLKİYLE AYNI DEĞİL!!!"
            entry_again_new_passw.delete(0, END)
            activateEntryNewPassword()
            entry_new_passw.delete(0, END)
        if len(warning_text)==0:  warning_lbl.configure(text=warning_text,bg=bgg)    
        else:  warning_lbl.configure(text=warning_text,bg="#639a67")    

    global frame_bg
    global password

    bgg = "#4cd137"
    warning_color = "#fbc531"
    btn_color = "#9b59b6"
    
    parser = ConfigParser()
    filee = "config.ini"
    parser.read(filee)
    password = parser.get("account", "password")

    password_top = Toplevel(background=bgg)
    password_top.overrideredirect(True)
    w = frame_bg.winfo_width()
    h = frame_bg.winfo_height()
    password_top.geometry('%dx%d+%d+%d' % (int((0.3*w)), h, int(0.7*w), int(0)))
    password_top.resizable(False, False) 
    password_top.wm_attributes('-topmost', 1)
    password_top.grab_set()

    password_top.columnconfigure(0, weight=1)
    password_top.rowconfigure(0, weight=2)
    password_top.rowconfigure(1, weight=4)
    password_top.rowconfigure(2, weight=2)
    password_top.rowconfigure(3, weight=4)
    password_top.rowconfigure(4, weight=1)
    password_top.rowconfigure(5, weight=2)
    password_top.rowconfigure(6, weight=4)
    password_top.rowconfigure(7, weight=1)
    password_top.rowconfigure(8, weight=2)
    password_top.rowconfigure(9, weight=3)
    password_top.rowconfigure(10, weight=12)
    password_top.rowconfigure(11, weight=3)
    '''////////////////////////////////////////'''
    var_password = StringVar()
    var_password.trace('w', control_old_password)
    var_new_password = StringVar()
    var_new_password.trace('w', control_new_password)
    var_again_new_password = StringVar()
    var_again_new_password.trace('w', control_again_new_password)
    '''////////////////////////////////////////'''
    text1 = "* Yeni şifreniz 4-12 karakter uzunluğunda olmalıdır"
    text2 = "* Özel karakter bulundurmamali, boşluk içermemelidir"

    lbl_passw = Label(password_top, text="Mevcut Şifrenizi Girin: ", bg=bgg, font=("bold", 15), border=0, width=25)
    lbl_passw.grid(column=0, row=0, sticky="s")

    entry_passw = Entry(password_top, textvar=var_password, highlightthickness=0, border=0, show="*", width=25)
    entry_passw.grid(column=0, row=1)

    lbl_new_passw = Label(password_top, text="Yeni Şifrenizi Girin: ", bg=bgg,  font=("bold", 15), border=0, width=25)
    lbl_new_passw.grid(column=0, row=2, sticky="s")

    entry_new_passw = Entry(password_top, textvar=var_new_password, highlightthickness=0, state=DISABLED, show="*", border=0, width=25)
    entry_new_passw.grid(column=0, row=3)

    warning_lbl_new_passw = Label(password_top, text="", bg=bgg, font=("bold", 15), fg=warning_color, border=0, width=50)
    warning_lbl_new_passw.grid(column=0, row=4, sticky="n")

    lbl_again_new_passw = Label(password_top, text="Yeni Şifrenizi Tekrar Girin: ", bg=bgg,  font=("bold", 15), border=0, width=25)
    lbl_again_new_passw.grid(column=0, row=5, sticky="s")

    entry_again_new_passw = Entry(password_top, textvar=var_again_new_password, highlightthickness=0, state=DISABLED, border=0, show="*", width=25)
    entry_again_new_passw.grid(column=0, row=6)

    warning_lbl_again_new_passw = Label(password_top, text="", bg=bgg, font=("bold", 15), fg=warning_color, border=0, width=50)
    warning_lbl_again_new_passw.grid(column=0, row=7, sticky="n")

    warning_lbl = Label(password_top, text="", bg=bgg, font=("bold", 12), fg=warning_color, border=0, width=50)
    warning_lbl.grid(column=0, row=8, sticky="nsew")

    account_lbl_info =  Label(password_top, text=f"{text1}\n{text2}", bg=bgg, font=("bold", 13), border=0)
    account_lbl_info.grid(column=0, row=9, sticky="n")
    '''////////////////////////////////////////'''
    keyboard_lbl = Label(password_top, border=0, bg=bgg)
    keyboard_lbl.grid(column=0, row=10, sticky="nsew")
    keyboard(keyboard_lbl, entry_passw)
    '''////////////////////////////////////////'''
    buttons_lbl_passw = Label(password_top, border=0)
    buttons_lbl_passw.grid(column=0, row=11, sticky="nsew")
    buttons_lbl_passw.columnconfigure(0, weight=1)
    buttons_lbl_passw.columnconfigure(1, weight=1)
    buttons_lbl_passw.columnconfigure(2, weight=1)
    buttons_lbl_passw.rowconfigure(0, weight=1)

    btn_back = Button(buttons_lbl_passw, text="Kapat", bg=btn_color, border=0, highlightthickness=0, font= "Helvetica 20", command=password_top.destroy)
    btn_back.grid(column=0, row=0, sticky="nsew")

    btn_delete = Button(buttons_lbl_passw, text="Sil", bg=btn_color, border=0, highlightthickness=0, font="Helvetica 20", command=delete_char)
    btn_delete.grid(column=1, row=0, sticky="nsew")

    btn_change_passw = Button(buttons_lbl_passw, text="Enter", bg=btn_color, border=0, highlightthickness=0, font= "Helvetica 20")
    btn_change_passw.grid(column=2, row=0, sticky="nsew")
    btn_change_passw.bind("<Button-1>", btn_change_password_clicker)

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
        icon_left = PhotoImage(file=f"{img_path}/left.png")
        icon_left = icon_left.subsample(6, 6)
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
        # t_add_user = threading.Thread(target=add_user)  ##
        t_rec.start()
        # t_add_user.start()  ##
        thread_check = False
        time.sleep(1)
    add_user()
def btn_delete_user_clicker(event):
    global thread_check
    global thread_stop
    
    if thread_check:
        thread_stop = True
        t_rec = threading.Thread(target=run)
        t_rec.start()
        thread_check = False
        time.sleep(1)
    delete_user()
def btn_register_password_clicker(event):
    global thread_check
    global thread_stop
    
    if thread_check:
        thread_stop = True
        t_rec = threading.Thread(target=run)
        t_rec.start()
        thread_check = False
        time.sleep(1)
    password_register()

'''///////////////////////////////////////'''
root = Tk()
root.geometry("750x500")
root.wm_attributes('-fullscreen', 'true')
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

icon_recog = PhotoImage(file=f"{img_path}/face-scan.png")
icon_recog = icon_recog.subsample(6, 6)

icon_add = PhotoImage(file=f"{img_path}/add-userr.png")
icon_add = icon_add.subsample(6, 6)

icon_delete = PhotoImage(file=f"{img_path}/delete-user.png")
icon_delete = icon_delete.subsample(6, 6)

icon_door = PhotoImage(file=f"{img_path}/open-door.png")
icon_door = icon_door.subsample(6 ,6)

icon_passw = PhotoImage(file=f"{img_path}/padlock.png")
icon_passw = icon_passw.subsample(6, 6)

'''///////////////////////////////////////'''
addToLabels()
'''///////////////////////////////////////'''

btn_recog = Button(options_lbl, image=icon_recog, justify="center",padx=4 , border=0, bg="#7bed9f", highlightthickness=0)
btn_recog.bind("<Button-1>", btn_recog_clicker)
btn_recog.grid(column=0, row=0, sticky="nsew")

btn_user_add = Button(options_lbl, image=icon_add, justify="center",padx=4 , border=0, bg="#70a1ff", highlightthickness=0)
btn_user_add.bind("<Button-1>", btn_add_user_clicker)
btn_user_add.grid(column=1, row=0, sticky="nsew")

btn_user_delete = Button(options_lbl, image=icon_delete, justify="center",padx=4 , border=0, bg="#B33771", highlightthickness=0, command=delete_user)
btn_user_delete.bind("<Button-1>", btn_delete_user_clicker)
btn_user_delete.grid(column=2, row=0, sticky="nsew")

btn_door = Button(options_lbl, image=icon_door, justify="center",padx=4 , border=0, bg="#a4b0be", highlightthickness=0, command=door_register)
btn_door.grid(column=3, row=0, sticky="nsew")

btn_passw = Button(options_lbl, image=icon_passw, justify="center",padx=4 , border=0, bg="#A75454", highlightthickness=0)
btn_passw.bind("<Button-1>", btn_register_password_clicker)

btn_passw.grid(column=4, row=0, sticky="nsew")


# t0 = threading.Thread(target=run)
# t0.start()
root.mainloop()