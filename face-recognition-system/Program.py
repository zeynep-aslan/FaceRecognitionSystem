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
import cvlib as cv

known_face_encondings = []
known_face_names = []
Ids = []
image_path = "known_faces"
TOLERANCE = 0.4
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

# cap = cv2.VideoCapture(1+cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_SETTINGS,1)

# cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
# #cap.set(cv2.CAP_PROP_SETTINGS,0)
# codec = 0x47504A4D  # MJPG
# cap.set(cv2.CAP_PROP_FPS, 30.0)
# cap.set(cv2.CAP_PROP_FOURCC, codec)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# #cap.set(cv2.CAP_PROP_SETTINGS,0)
'''///////////////////////////////////////'''
frame_copy = ""
CONFIDANCE = 0.95
confidence = []

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
    global ret
    global face_locations
    global thread_stop
    global frame
    global confidence
    # global frame_copy
    ret = False
    try:
        global cap
        global tkimage1
        while root.winfo_exists() and thread_stop:
            ret, frame_ = cap.read()
            if ret:
                frame = cv2.flip(frame_, 1)
                frame_copy = frame.copy()
                h, w, channels = frame_copy.shape
                isThereLogo = False
                '''///////////////////////////////////////'''
                try:
                    if confidence[0] > 0:  #  if isThereFace
                        for top, right, bottom, left in face_locations:
                            if not check:  # buraya veya daha ustune confidance koy, 0.99 dan buyukse cizdir
                                cv2.rectangle(frame_copy, (left, top), (right, bottom), (0, 255, 0), 2)
                                cv2.rectangle(frame_copy, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                                cv2.putText(frame_copy, f"{name}  {str(distance)}", (left + 4, bottom - 4),cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 255, 255), 2)
                            else:
                                cv2.putText(frame_copy, "lutfen bekleyin", (int(w / 10), int(2 * h / 3)), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 3)
                except:
                    # cv2.putText(frame_copy, "lutfen bekleyinnnn", (int(w / 10), int(2 * h / 3)),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 3)
                    isThereLogo = True            
                    logo = PhotoImage(file=f"{img_path}/black_blu_2.png")
                    video_label.configure(image=logo)
                    video_label.image = logo
                '''///////////////////////////////////////'''
                new_rgb_frame = frame_copy
                new_rgb_frame = new_rgb_frame[:, :, ::-1]
                img = Image.fromarray(new_rgb_frame)
                img = img.resize((video_label.winfo_width(), video_label.winfo_height()), Image.BICUBIC)
                # print(frame_bg.winfo_width(), frame_bg.winfo_height())
                if thread_stop and not isThereLogo:
                    tkimage1 = ImageTk.PhotoImage(img)
                    video_label.configure(image=tkimage1)
                    video_label.image = tkimage1
            elif root.winfo_exists():
                cap = cv2.VideoCapture(0)
                # cap = cv2.VideoCapture(1+cv2.CAP_DSHOW)
                # cap.set(cv2.CAP_PROP_SETTINGS,1)

                # cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
                # cap.set(cv2.CAP_PROP_SETTINGS,0)
                # codec = 0x47504A4D  # MJPG
                # cap.set(cv2.CAP_PROP_FPS, 30.0)
                # cap.set(cv2.CAP_PROP_FOURCC, codec)
                # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            if root.winfo_exists():
                root.update()
        if not thread_stop:
            cap.release()
    except:
        cap.release()
        pass

def run_info():
    global known_face_encondings
    global known_face_names
    global name
    global face_locations
    global thread_stop
    global frame
    # global frame_copy
    global distance
    global ret
    global left, top, right, bottom
    global confidence
    global isThereFace

    while thread_stop:
        if ret:
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                locations, confidence = cv.detect_face(rgb_frame)
                isThere = (True for x in confidence if float(
                    x) > CONFIDANCE)  # generator, disa [] koyarsan ['True] doner, bu sekilde generator adresini atadik next ile ulasicaz
                name, distance = "", ""
                face_locations = []
                isThereFace = next(isThere)
                if isThereFace:
                    left, top, right, bottom = locations[0][0], locations[0][1], locations[0][2], locations[0][3]
                    face_locations = [(top, right, bottom, left)]
                    face_encodings = fr.face_encodings(rgb_frame, face_locations)
                    try:
                        for face_encoding in face_encodings:
                            matches = fr.compare_faces(known_face_encondings, face_encoding, TOLERANCE)
                            face_distances = fr.face_distance(known_face_encondings, face_encoding)
                            if len(face_distances) > 0:
                                best_match_index = np.argmin(face_distances)
                                match = matches[best_match_index]
                                if match:
                                    name = known_face_names[best_match_index]
                                    distance = format(face_distances[best_match_index], ".3f")
                    except Exception as e:
                        print("hata: ", e)
            except:
                pass

def quit_():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.quit()
def destroy_():
    quit_()
    return None
def keyboard(keyboard_lbl, keyboard_entry):
    # buttoncolor_char = "#107dac"
    # buttoncolor_num = "#4cd137"
    buttoncolor_char = "#07a0c3"
    buttoncolor_num = "#086788"
    font = "Helvetica 20"

    keyBoard_list = {
        '0': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '7', '8', '9'],
        '1': ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'İ', '4', '5', '6'],
        '2': ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Ö', 'Ç', '0', '1', '2', '3']
    }

    row0 = keyBoard_list['0']
    row1 = keyBoard_list['1']
    row2 = keyBoard_list['2']

    keyboard_lbl.rowconfigure(0, weight=2)  # bos
    keyboard_lbl.rowconfigure(1, weight=2)
    keyboard_lbl.rowconfigure(2, weight=2)
    keyboard_lbl.columnconfigure(0, weight=2)  # bos
    keyboard_lbl.columnconfigure(1, weight=2)
    keyboard_lbl.columnconfigure(2, weight=2)
    keyboard_lbl.columnconfigure(3, weight=2)
    keyboard_lbl.columnconfigure(4, weight=2)
    keyboard_lbl.columnconfigure(5, weight=2)
    keyboard_lbl.columnconfigure(6, weight=2)
    keyboard_lbl.columnconfigure(7, weight=2)
    keyboard_lbl.columnconfigure(8, weight=2)
    keyboard_lbl.columnconfigure(9, weight=2)
    keyboard_lbl.columnconfigure(10, weight=2)
    keyboard_lbl.columnconfigure(11, weight=2)
    keyboard_lbl.columnconfigure(12, weight=2)

    b0_0 = Button(keyboard_lbl, text=row0[0], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[0]))
    b0_0.grid(row=0, column=0)

    b0_1 = Button(keyboard_lbl, text=row0[1], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[1]))
    b0_1.grid(row=0, column=1)

    b0_2 = Button(keyboard_lbl, text=row0[2], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[2]))
    b0_2.grid(row=0, column=2)

    b0_3 = Button(keyboard_lbl, text=row0[3], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[3]))
    b0_3.grid(row=0, column=3)

    b0_4 = Button(keyboard_lbl, text=row0[4], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[4]))
    b0_4.grid(row=0, column=4)

    b0_5 = Button(keyboard_lbl, text=row0[5], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[5]))
    b0_5.grid(row=0, column=5)

    b0_6 = Button(keyboard_lbl, text=row0[6], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[6]))
    b0_6.grid(row=0, column=6)

    b0_7 = Button(keyboard_lbl, text=row0[7], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[7]))
    b0_7.grid(row=0, column=7)

    b0_8 = Button(keyboard_lbl, text=row0[8], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[8]))
    b0_8.grid(row=0, column=8)

    b0_9 = Button(keyboard_lbl, text=row0[9], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row0[9]))
    b0_9.grid(row=0, column=9)

    b0_10 = Button(keyboard_lbl, text=row0[10], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row0[10]))
    b0_10.grid(row=0, column=10)

    b0_11 = Button(keyboard_lbl, text=row0[11], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row0[11]))
    b0_11.grid(row=0, column=11)

    b0_12 = Button(keyboard_lbl, text=row0[12], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row0[12]))
    b0_12.grid(row=0, column=12)
    '''///////////////////////////////////////////////'''
    b1_0 = Button(keyboard_lbl, text=row1[0], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[0]))
    b1_0.grid(row=1, column=0)

    b1_1 = Button(keyboard_lbl, text=row1[1], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[1]))
    b1_1.grid(row=1, column=1)

    b1_2 = Button(keyboard_lbl, text=row1[2], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[2]))
    b1_2.grid(row=1, column=2)

    b1_3 = Button(keyboard_lbl, text=row1[3], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[3]))
    b1_3.grid(row=1, column=3)

    b1_4 = Button(keyboard_lbl, text=row1[4], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[4]))
    b1_4.grid(row=1, column=4)

    b1_5 = Button(keyboard_lbl, text=row1[5], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[5]))
    b1_5.grid(row=1, column=5)

    b1_6 = Button(keyboard_lbl, text=row1[6], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[6]))
    b1_6.grid(row=1, column=6)

    b1_7 = Button(keyboard_lbl, text=row1[7], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[7]))
    b1_7.grid(row=1, column=7)

    b1_8 = Button(keyboard_lbl, text=row1[8], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[8]))
    b1_8.grid(row=1, column=8)

    b1_9 = Button(keyboard_lbl, text=row1[9], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row1[9]))
    b1_9.grid(row=1, column=9)

    b1_10 = Button(keyboard_lbl, text=row1[10], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row1[10]))
    b1_10.grid(row=1, column=10)

    b1_11 = Button(keyboard_lbl, text=row1[11], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row1[11]))
    b1_11.grid(row=1, column=11)

    b1_12 = Button(keyboard_lbl, text=row1[12], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row1[12]))
    b1_12.grid(row=1, column=12)
    '''///////////////////////////////////////////////'''
    b2_0 = Button(keyboard_lbl, text=row2[0], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[0]))
    b2_0.grid(row=2, column=0)

    b2_1 = Button(keyboard_lbl, text=row2[1], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[1]))
    b2_1.grid(row=2, column=1)

    b2_2 = Button(keyboard_lbl, text=row2[2], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[2]))
    b2_2.grid(row=2, column=2)

    b2_3 = Button(keyboard_lbl, text=row2[3], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[3]))
    b2_3.grid(row=2, column=3)

    b2_4 = Button(keyboard_lbl, text=row2[4], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[4]))
    b2_4.grid(row=2, column=4)

    b2_5 = Button(keyboard_lbl, text=row2[5], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[5]))
    b2_5.grid(row=2, column=5)

    b2_6 = Button(keyboard_lbl, text=row2[6], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[6]))
    b2_6.grid(row=2, column=6)

    b2_7 = Button(keyboard_lbl, text=row2[7], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[7]))
    b2_7.grid(row=2, column=7)

    b2_8 = Button(keyboard_lbl, text=row2[8], bg=buttoncolor_char, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[8]))
    b2_8.grid(row=2, column=8)

    b2_9 = Button(keyboard_lbl, text=row2[9], bg=buttoncolor_num, border=0, highlightthickness=0,
                  activebackground=buttoncolor_char,
                  font=font, command=lambda: keyboard_entry.insert(END, row2[9]))
    b2_9.grid(row=2, column=9)

    b2_10 = Button(keyboard_lbl, text=row2[10], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row2[10]))
    b2_10.grid(row=2, column=10)

    b2_11 = Button(keyboard_lbl, text=row2[11], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row2[11]))
    b2_11.grid(row=2, column=11)

    b2_12 = Button(keyboard_lbl, text=row2[12], bg=buttoncolor_num, border=0, highlightthickness=0,
                   activebackground=buttoncolor_char,
                   font=font, command=lambda: keyboard_entry.insert(END, row2[12]))
    b2_12.grid(row=2, column=12)
def add_user():
    def delete_char_add_user():
        entry_passw_add_user.delete(len(entry_passw_add_user.get()) - 1, END)
        entry_name_add_user.delete(len(entry_name_add_user.get()) - 1, END)
    def add_userr():
        global isThereFace

        number_of_img = 3
        temp = 0
        list_int = map(int, Ids)
        list_int = list(list_int)
        list_int = sorted(list_int)
        try:
            biggest_id = list_int[-1]
        except:
            biggest_id = 0

        for i in range(biggest_id + 1):
            if str(i) not in Ids:
                latest = i
                break
            if i == biggest_id:
                latest = i + 1

        faces = []
        check = True
        for i in range(5):
            if temp == number_of_img:  ###
                break
            lbl_info_add_user.config(text="3")
            time.sleep(.5)
            lbl_info_add_user.config(text="2")
            time.sleep(.5)
            lbl_info_add_user.config(text="1")
            time.sleep(.5)
            lbl_info_add_user.config(text="0")
            try:
                face_img = frame[top: bottom, left: right]
                # print("okii")
                # cv2.imshow("face_img", face_img)
                # cv2.waitKey(1)
                print("top, bottom, left, right:::: ", top, bottom, left, right)
            except:
                print("frame kirpamiyorz: ", e)    
                pass
            if isThereFace:
                print("yuz")
                try:
                    img_encoding = fr.face_encodings(face_img)[0]  #  list index out of range
                    faces.append(img_encoding)
                    try:
                        os.mkdir(f"{image_path}/{latest}")
                    except:
                        pass
                    temp += 1
                    path = f"{image_path}/{latest}/{entry_name_add_user.get()}-{temp}.jpeg"
                    cv2.imwrite(path, face_img)
                except Exception as e:
                    print(i)
                    # print("frame kirpamiyor cunku yuz bulamadi: ", e)
                    print(e)        
                    pass
                    # warning_lbl_add_user.config(text=f"yuz bulunamadi!!aldigim error: {e}")
        check = False
        if len(faces) > 1:  #  if len(faces) > 0:  idi
            try:
                known_face_encondings.append(img_encoding)
                Ids.append(str(latest))
                for i in faces:
                    known_face_names.append(entry_name_add_user.get())
                lbl_info_add_user.config(text=f"kullanici basariyla eklendi, id bilgisi: {latest}", bg=warning_color_add_user)
                # time.sleep(1)  # label in text ine yazdirmiyor
                entry_passw_add_user.configure(state=NORMAL)
                entry_passw_add_user.delete(0, END)
                entry_name_add_user.delete(0, END)
                entry_name_add_user.configure(state=DISABLED)
                keyboard(keyboard_lbl_add_user, entry_passw_add_user)
            except Exception as e:
                print("len(faces) kismi: ", e)
                lbl_info_add_user.config(text=f"yuz bilgileri eklenemedi!!! aldigim error: {e}", bg=warning_color_add_user)
        else:
            lbl_info_add_user.config(text="yuz bilgileri eklenemedi!!", bg=warning_color_add_user)
            temp = 0
            try:
                shutil.rmtree(f"{image_path}/{latest}")
                print("klasor silindi")
            except:
                print("klasor silinemedi")
                pass    
    def activateEntryName():

        entry_passw_add_user.configure(state=DISABLED)
        entry_name_add_user.configure(state=NORMAL)
        btn_add_user.configure(text="Enter")
        lbl_info_add_user.configure(text=info_add, bg=bg_add_user)
        keyboard(keyboard_lbl_add_user, entry_name_add_user)
    def control_password_add_user(*args):

        btn_add_user.configure(text="Enter")
        lbl_info_add_user.configure(text=info_add, bg=bg_add_user)
        password_add_user = var_password_add_user.get()
        btn_add_user.config(state="normal")
        if len(password_add_user) < 4:
            btn_add_user.config(state=DISABLED)
        else:
            btn_add_user.config(state="normal")
        if len(password_add_user) > 11:
            var_password_add_user.set(password_add_user[:12])
    def control_name_add_user(*args):
        global isCorrectName

        btn_add_user.configure(text="Kaydet")
        var_name = var_name_add_user.get()
        textt = info_add
        btn_add_user.config(state=DISABLED)

        if len(face_locations) > 1:  #
            textt = "kameranin karsisinda birden fazla kisi bulunmamalidir"
            isCorrectName = False
            btn_add_user.config(state=DISABLED)
        elif name in known_face_names:
            textt = "kayitli kullaniciyi bir daha ekleyemezsiniz!"
            isCorrectName = False
            btn_add_user.config(state=DISABLED)
        elif " " in var_name:  #
            textt = "isimde bosluk bulunmamalidir"
            isCorrectName = False
            btn_add_user.config(state=DISABLED)
        elif any(char.isdigit() for char in var_name):
            textt = "isimde sayi bulunmamalidir"
            isCorrectName = False
            btn_add_user.config(state=DISABLED)
        else:
            btn_add_user.config(state=NORMAL)
            isCorrectName = True
        # print(btn_add_user['state'])    
        if textt == info_add:  lbl_info_add_user.configure(text=textt, bg=bg_add_user)    
        else:  lbl_info_add_user.configure(text=textt, bg=warning_color_add_user)  # buna veya bi ustundekine gerek yok 
    def btn_add_user_clicker(event):
        global isCorrectName
        
        parser = ConfigParser()
        file = "config.ini"
        parser.read(file)
        password = parser.get("account", "password")
        warning_text = info_add

        if entry_passw_add_user.get() == password and len(entry_name_add_user.get()) == 0:
            btn_add_user.configure(state=NORMAL)
            activateEntryName()
        elif entry_passw_add_user.get() != password and len(entry_passw_add_user.get()) > 0:
            warning_text = "ŞİFRE YANLIŞ!!!"
            entry_passw_add_user.delete(0, END)
        elif isCorrectName and entry_passw_add_user.get() == password and len(entry_name_add_user.get()) > 3:
            t3 = threading.Thread(target=add_userr)
            t3.start()
        elif entry_passw_add_user.get() == password and len(entry_name_add_user.get()) > 3:
            entry_name_add_user.delete(0, END)
        elif entry_passw_add_user.get() == password and len(entry_name_add_user.get()) <= 3:
            warning_text = "isim çok kısa!!!"
            entry_name_add_user.delete(0, END)
        if warning_text == info_add:  lbl_info_add_user.configure(text=warning_text,bg=bg_add_user)    
        else:  lbl_info_add_user.configure(text=warning_text,bg=warning_color_add_user)  # buna veya bi ustundekine gerek yok 

    global name
    global Ids
    global check
    global frame
    global known_face_encondings
    global known_face_names
    global face_locations
    global left, top, right, bottom
    
    bg_add_user = "#e9eb87"
    warning_font_color_add_user = "#8ff18c"
    warning_color_add_user = "#639a67"
    btn_color_add_user = "#938274"
    close_color_add_user = "#7b5e7b"
    font_add_user = "Helvetica 20"

    # warning_font_color_del_user = "#14bdeb"
    # warning_color_del_user = "#639a67"


    user_top = Toplevel(background=bg_add_user)
    user_top.overrideredirect(True)
    user_top.minsize(300, 300)
    w = frame_bg.winfo_width()
    h = root.winfo_height()

    bg_w = video_label.winfo_width()
    ww = int(0.4 * w)
    user_top.geometry('%dx%d+%d+%d' % (ww, h, w - ww, 0))
    user_top.resizable(False, False)
    user_top.wm_attributes('-topmost', 1)
    user_top.wait_visibility()  # Wait until the visibility of a WIDGET changes
    user_top.grab_set()

    # print(user_top.winfo_geometry())

    user_top.columnconfigure(0, weight=1)
    user_top.rowconfigure(0, weight=1)
    user_top.rowconfigure(1, weight=2)
    user_top.rowconfigure(2, weight=2)
    user_top.rowconfigure(3, weight=1)
    user_top.rowconfigure(4, weight=2)
    user_top.rowconfigure(5, weight=2)
    user_top.rowconfigure(6, weight=1)
    user_top.rowconfigure(7, weight=4)
    user_top.rowconfigure(8, weight=1)
    user_top.rowconfigure(9, weight=12)
    user_top.rowconfigure(10, weight=3)
    '''////////////////////////////////////////'''

    var_password_add_user = StringVar()
    var_password_add_user.trace('w', control_password_add_user)
    var_name_add_user = StringVar()
    var_name_add_user.trace('w', control_name_add_user)

    '''////////////////////////////////////////'''
    info_add = "* 3 adet resim çekilecektir *"
    '''////////////////////////////////////////'''
    lbl_empty_add_user = Label(user_top, bg=bg_add_user, border=0, width=15)
    lbl_empty_add_user.grid(column=0, row=0, sticky="n")
    '''////////////////////////////////////////'''

    lbl_passw_add_user = Label(user_top, text="Sifrenizi Girin: ", bg=bg_add_user, font=("bold", 15), border=0, width=25)
    lbl_passw_add_user.grid(column=0, row=1, sticky="s")

    entry_passw_add_user = Entry(user_top, textvar=var_password_add_user, highlightthickness=0, border=0, show="*",
                                 width=25)
    entry_passw_add_user.grid(column=0, row=2)

    lbl_empty_add_user_p = Label(user_top, text="", bg=bg_add_user, fg=warning_font_color_add_user, border=0,
                                       width=25)
    lbl_empty_add_user_p.grid(column=0, row=3, sticky="n")
    '''///////////////////////////////////////'''
    lbl_name_add_user = Label(user_top, text="İsminizi Girin: ", bg=bg_add_user, font=("bold", 15), border=0,
                                 width=25)
    lbl_name_add_user.grid(column=0, row=4, sticky="s")

    entry_name_add_user = Entry(user_top, textvar=var_name_add_user, highlightthickness=0, state=DISABLED, border=0,
                                width=25)
    entry_name_add_user.grid(column=0, row=5)

    lbl_empty_add_user_n = Label(user_top, text="", bg=bg_add_user, fg=warning_font_color_add_user, border=0,
                                      width=25)
    lbl_empty_add_user_n.grid(column=0, row=6, sticky="n")

    lbl_info_add_user = Label(user_top, text=f"{info_add}", width=50, fg=warning_font_color_add_user, bg=bg_add_user, font=("bold", 15), border=0)
    lbl_info_add_user.grid(column=0, row=7, sticky="nsew")
    '''///////////////////////////////////////'''
    lbl_empty_add_user_ = Label(user_top, bg=bg_add_user, border=0, width=25)
    lbl_empty_add_user_.grid(column=0, row=8, sticky="n")
    '''///////////////////////////////////////////////'''
    keyboard_lbl_add_user = Label(user_top, border=0, bg=bg_add_user)
    keyboard_lbl_add_user.grid(column=0, row=9, sticky="nsew")

    keyboard(keyboard_lbl_add_user, entry_passw_add_user)

    '''////////////////////////////////////////'''
    lbl_buttons_add_user = Label(user_top, font=("bold", 13), border=0, bg=bg_add_user)
    lbl_buttons_add_user.grid(column=0, row=10, sticky="nsew")
    lbl_buttons_add_user.columnconfigure(0, weight=1)
    lbl_buttons_add_user.columnconfigure(1, weight=1)
    lbl_buttons_add_user.columnconfigure(2, weight=1)
    lbl_buttons_add_user.rowconfigure(0, weight=1)
    btn_back_add_user = Button(lbl_buttons_add_user, text="Kapat", bg=close_color_add_user, border=0, highlightthickness=0,
                               font=font_add_user, command=user_top.destroy)
    btn_back_add_user.grid(column=0, row=0, sticky="nsew")

    btn_delete_add_user = Button(lbl_buttons_add_user, text="Sil", bg=btn_color_add_user, border=0, highlightthickness=0,
                                 font=font_add_user, command=delete_char_add_user)
    btn_delete_add_user.grid(column=1, row=0, sticky="nsew")

    btn_add_user = Button(lbl_buttons_add_user, text="Enter", bg=btn_color_add_user, border=0, highlightthickness=0,
                          font=font_add_user)
    btn_add_user.grid(column=2, row=0, sticky="nsew")
    btn_add_user.bind("<Button-1>", btn_add_user_clicker)

def delete_user():
    def delete_char_del_user():
        entry_passw_del_user.delete(len(entry_passw_del_user.get()) - 1, END)
        entry_id_del_user.delete(len(entry_id_del_user.get()) - 1, END)
    def delete_userr(iddd):
        try:
            path = f"{image_path}/{iddd}"
            shutil.rmtree(path)

            lbl_info_del_user.configure(
                text=f"{name} kullanıcısı silindi", bg=warning_color_del_user)
            # addToLabels()
            t5 = threading.Thread(target=addToLabels)
            t5.start()
            entry_passw_del_user.configure(state=NORMAL)
            btn_cam.configure(state=DISABLED)
            entry_passw_del_user.delete(0, END)
            entry_id_del_user.delete(0, END)
            entry_id_del_user.configure(state=DISABLED)
            keyboard(keyboard_lbl_del_user, entry_passw_del_user)
        except Exception as e:
            lbl_info_del_user.configure(text="kullanıcısı silinemedi", bg=warning_color_del_user)
    def activateEntryId():

        entry_passw_del_user.configure(state=DISABLED)
        entry_id_del_user.configure(state=NORMAL)
        btn_del_user.configure(text="Id İle Sil")
        lbl_info_del_user.configure(text=text1, bg=bg_del_user)
        keyboard(keyboard_lbl_del_user, entry_id_del_user)
    def delete_user_cam_clicker(event):

        if len(entry_passw_del_user.get()) == 0:
            lbl_info_del_user.configure(text="şifre girin!!!", bg=warning_color_del_user)
        elif entry_passw_del_user.get() == password:
            if len(face_locations) > 1:
                lbl_info_del_user.configure(text="kamera karşısında bir kişi olmalı!!!", bg=warning_color_del_user)

            elif len(face_locations) == 1:

                if len(known_face_names) == 0:
                    lbl_info_del_user.configure(
                        text="sistemde hiç kullanıcı yok!!!", bg=warning_color_del_user)
                else:
                    name_list = []
                    name_list = list(OrderedDict.fromkeys(known_face_names))
                    # print(Ids)
                    for nme, idd in zip(name_list, Ids):
                        if nme == name:
                            delete_userr(idd)
                            # t4 = threading.Thread(target=delete_userr, args=(idd))
                            # t4.start()
                            break
            else:
                lbl_info_del_user.configure(text="kamera karşısında yuz yok!!!", bg=warning_color_del_user)
        else:
            lbl_info_del_user.configure(
                        text="ŞİFRE YANLIŞ!!!", bg=warning_color_del_user)
    def btn_del_user_clicker(event):

        warning_text = text1
        parser.read(filee)
        password = parser.get("account", "password")

        if entry_passw_del_user.get() == password and len(entry_id_del_user.get()) == 0:
            btn_cam.configure(state=NORMAL)
            activateEntryId()
        elif entry_passw_del_user.get() != password and len(entry_passw_del_user.get()) > 0:
            warning_text = "ŞİFRE YANLIŞ!!!"
            # isPasswCorrect = False
            entry_passw_del_user.delete(0, END)
        if entry_id_del_user.get() not in Ids and len(entry_id_del_user.get()) > 0:
            warning_text = "GEÇERSİZ ID GİRİŞİ"
            entry_id_del_user.delete(0, END)
        elif entry_id_del_user.get() in Ids and len(entry_id_del_user.get()) > 0:
            delete_userr(entry_id_del_user.get())
            # t5 = threading.Thread(target=delete_userr, args=(entry_id_del_user.get()))
            # t5.start()
        if warning_text == text1:  lbl_info_del_user.configure(text=warning_text, bg=bg_del_user)
        else:  lbl_info_del_user.configure(text=warning_text, bg=warning_color_del_user)  # renklere bak
    def control_password_del_user(*args):

        btn_del_user.configure(text="Enter")
        lbl_info_del_user.configure(text=text1, bg=bg_del_user)  # burasi neden calismadi

        password_del_user = var_password_del_user.get()
        if len(password_del_user) < 4:
            btn_del_user.config(state=DISABLED)
        else:
            btn_del_user.config(state=NORMAL)
        if len(password_del_user) > 11:
            var_password_del_user.set(password_del_user[:12])
        else:
            btn_del_user.config(state=NORMAL)
    def control_id(*args):

        lbl_info_del_user.configure(text=text1, bg=bg_del_user)
        id_del_user = var_id.get()

        if not id_del_user.isnumeric() and len(id_del_user) > 0:  # id rakam olamaz
            textt = "Id sayi olmalidir!!!"
            lbl_info_del_user.configure(text=textt, bg=warning_color_del_user)
            btn_del_user.config(state=DISABLED)
        else:
            btn_del_user.config(state=NORMAL)
            lbl_info_del_user.configure(text=text1, bg=bg_del_user)

    global Ids
    global face_locations
    global known_face_names
    global name

    text1 = "* sabit durunuz *"

    bg_del_user = "#dccde8"
    warning_font_color_del_user = "#14bdeb"
    warning_color_del_user = "#639a67"
    btn_color_del_user = "#d99ac5"
    close_btn_del_user = "#b37ba4"

    parser = ConfigParser()
    filee = "config.ini"
    parser.read(filee)
    password = parser.get("account", "password")

    del_user_top = Toplevel(background=bg_del_user)
    del_user_top.overrideredirect(True)
    w = frame_bg.winfo_width()
    h = root.winfo_height()

    bg_w = video_label.winfo_width()
    ww = int(0.4 * w)
    del_user_top.geometry('%dx%d+%d+%d' % (ww, h, w - ww, 0))  # +sol ust kose koordinatlari
    del_user_top.resizable(False, False)
    del_user_top.wm_attributes('-topmost', 1)
    del_user_top.wait_visibility()  # Wait until the visibility of a WIDGET changes
    del_user_top.grab_set()

    del_user_top.columnconfigure(0, weight=1)
    del_user_top.rowconfigure(0, weight=2)
    del_user_top.rowconfigure(1, weight=2)
    del_user_top.rowconfigure(2, weight=4)
    del_user_top.rowconfigure(3, weight=1)
    del_user_top.rowconfigure(4, weight=2)
    del_user_top.rowconfigure(5, weight=4)
    del_user_top.rowconfigure(6, weight=2)
    del_user_top.rowconfigure(7, weight=4)
    del_user_top.rowconfigure(8, weight=12)
    del_user_top.rowconfigure(9, weight=3)

    '''////////////////////////////////////////'''
    var_password_del_user = StringVar()
    var_password_del_user.trace('w', control_password_del_user)
    var_id = StringVar()
    var_id.trace('w', control_id)
    '''////////////////////////////////////////'''

    lbl_empty_del_user = Label(del_user_top, bg=bg_del_user, border=0, width=25)
    lbl_empty_del_user.grid(column=0, row=0, sticky="n")

    lbl_passw_del_user = Label(del_user_top, text="Şifrenizi Girin: ", bg=bg_del_user, font=("bold", 15), border=0, width=25)
    lbl_passw_del_user.grid(column=0, row=1, sticky="s")

    entry_passw_del_user = Entry(del_user_top, textvar=var_password_del_user, highlightthickness=0, border=0, show="*",
                                 width=25)
    entry_passw_del_user.grid(column=0, row=2)

    '''///////////////////////////////////////'''
    lbl_empty_del_user_ = Label(del_user_top, bg=bg_del_user, border=0, width=25)
    lbl_empty_del_user_.grid(column=0, row=3, sticky="n")
    '''///////////////////////////////////////'''

    lbl_id_del_user = Label(del_user_top, text="Id Girin: ", bg=bg_del_user, font=("bold", 15), border=0, width=25)
    lbl_id_del_user.grid(column=0, row=4, sticky="s")

    entry_id_del_user = Entry(del_user_top, textvar=var_id, highlightthickness=0, state=DISABLED, show="*", border=0,
                              width=25)
    entry_id_del_user.grid(column=0, row=5)

    warning_lbl_del_user = Label(del_user_top, text="", bg=bg_del_user, font=("bold", 15), fg=warning_font_color_del_user, border=0, 
                                    width=50)
    warning_lbl_del_user.grid(column=0, row=6, sticky="nsew")
    '''////////////////////////////////////////'''
    lbl_cam_del_user = Label(del_user_top, bg=bg_del_user, font=("bold", 13), border=0)
    lbl_cam_del_user.grid(column=0, row=7, sticky="n")

    lbl_cam_del_user.columnconfigure(0, weight=1)
    lbl_cam_del_user.rowconfigure(0, weight=1)
    lbl_cam_del_user.rowconfigure(1, weight=1)
    lbl_cam_del_user.rowconfigure(2, weight=1)
    lbl_cam_del_user.rowconfigure(3, weight=1)

    btn_cam = Button(lbl_cam_del_user, text="Kamera İle Sil", bg=btn_color_del_user, state=DISABLED, border=0,
                     highlightthickness=0, font="Helvetica 20")
    btn_cam.bind("<Button-1>", delete_user_cam_clicker)
    btn_cam.grid(column=0, row=0)

    lbl_empty_del_user2 = Label(lbl_cam_del_user, bg=bg_del_user, border=0, width=10)
    lbl_empty_del_user2.grid(column=0, row=1)

    lbl_info_del_user = Label(lbl_cam_del_user, text=text1, bg=bg_del_user, font=("bold", 15), fg=warning_font_color_del_user,
                              border=0, width=40)
    lbl_info_del_user.grid(column=0, row=2, sticky="s")

    warning_lbl_cam_del_user = Label(lbl_cam_del_user, text="", bg=bg_del_user, font=("bold", 14), fg=warning_font_color_del_user, border=0,
                                     width=10)
    warning_lbl_cam_del_user.grid(column=0, row=3, sticky="s")

    '''////////////////////////////////////////'''
    keyboard_lbl_del_user = Label(del_user_top, border=0, bg=bg_del_user)
    keyboard_lbl_del_user.grid(column=0, row=8, sticky="nsew")
    keyboard(keyboard_lbl_del_user, entry_passw_del_user)
    '''////////////////////////////////////////'''
    lbl_buttons_del_user = Label(del_user_top, border=0)
    lbl_buttons_del_user.grid(column=0, row=9, sticky="nsew")
    lbl_buttons_del_user.columnconfigure(0, weight=1)
    lbl_buttons_del_user.columnconfigure(1, weight=1)
    lbl_buttons_del_user.columnconfigure(2, weight=1)
    lbl_buttons_del_user.rowconfigure(0, weight=1)

    btn_back = Button(lbl_buttons_del_user, text="Kapat", bg=close_btn_del_user, border=0, highlightthickness=0,
                      font="Helvetica 20", command=del_user_top.destroy)
    btn_back.grid(column=0, row=0, sticky="nsew")

    btn_delete = Button(lbl_buttons_del_user, text="Sil", bg=btn_color_del_user, border=0, highlightthickness=0,
                        font="Helvetica 20", command=delete_char_del_user)
    btn_delete.grid(column=1, row=0, sticky="nsew")

    btn_del_user = Button(lbl_buttons_del_user, text="Enter", bg=btn_color_del_user, border=0, highlightthickness=0,
                          font="Helvetica 20")
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
        warning_lbl.configure(text=info_passw, bg=bg_passw)    
        password1 = var_password.get()
        btn_change_passw.config(state=NORMAL)
        if len(password1) < 4:
            btn_change_passw.config(state=DISABLED)
        if len(password1) > 11:
            var_password.set(password1[:12])
    def control_new_password(*args):

        warning_lbl.configure(text=info_passw, bg=bg_passw)    
        password2 = var_new_password.get()
        textt = info_passw
        btn_change_passw.config(state=NORMAL)

        if len(password2) == 0:
            btn_change_passw.config(state=DISABLED)
        elif len(password2) < 4:
            textt = "sifreniz cok kisa!!!"
            btn_change_passw.config(state=DISABLED)
        if len(password2) > 11:
            textt = "şifreniz daha uzun olamaz!!!"
            var_new_password.set(password2[:12])
        if textt == info_passw:  warning_lbl.configure(text=textt,bg=bg_passw)    
        else:  warning_lbl.configure(text=textt,bg=warning_color_passw)
    def control_again_new_password(*args):
        
        btn_change_passw.configure(text="Kaydet")
        warning_lbl.configure(text=info_passw, bg=bg_passw)    
        password3 = var_again_new_password.get()
        textt = info_passw
        btn_change_passw.config(state=NORMAL)

        if len(password3) == 0:
            btn_change_passw.config(state=DISABLED)
        elif len(password3) < 4:
            textt = "şifreniz cok kisa!!!"
            btn_change_passw.config(state=DISABLED)
        if len(password3) > 11:
            textt = "şifreniz daha uzun olamaz!!!"
            var_again_new_password.set(password3[:12])
        if textt == info_passw:  warning_lbl.configure(text=textt,bg=bg_passw)    
        else:  warning_lbl.configure(text=textt,bg=warning_color_passw)
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

        warning_text = info_passw
        parser.read(filee)
        password = parser.get("account", "password")

        if entry_passw.get() == password and len(entry_new_passw.get())==0 and len(entry_again_new_passw.get())==0:
            warning_text = info_passw  #### kontrol et
            activateEntryNewPassword()
        elif entry_passw.get() != password and len(entry_passw.get())>0:
            warning_text = "şifre yanlış!!!"
            entry_passw.delete(0, END)
        if entry_passw.get() != entry_new_passw.get() and len(entry_new_passw.get())>3 and len(entry_new_passw.get())<13:  # 4-12
            warning_text = info_passw  #### kontrol et
            activateEntryAgainNewPassword()
        elif entry_passw.get() == entry_new_passw.get() and len(entry_passw.get())>0:
            warning_text = "yeni şifre eski şifreyle aynı olamaz"
            entry_new_passw.delete(0, END)
        if len(entry_again_new_passw.get())>3 and len(entry_again_new_passw.get())<13 and entry_again_new_passw.get()==entry_new_passw.get():
            warning_text = "şifre değiştirildi"
            changePassword()
        elif len(entry_new_passw.get())>3 and len(entry_new_passw.get())<13 and entry_again_new_passw.get()!=entry_new_passw.get() and len(entry_again_new_passw.get())>0:
            warning_text = "girdiğiniz şifreler aynı değil"
            entry_again_new_passw.delete(0, END)
            activateEntryNewPassword()
            entry_new_passw.delete(0, END)
        if warning_text == info_passw:  warning_lbl.configure(text=warning_text,bg=bg_passw)    # burayi duzelt
        else:  warning_lbl.configure(text=warning_text,bg=warning_color_passw)    

    global password

    bg_passw = "#f3de2c"
    warning_font_color_passw = "#fb6107"
    warning_color_passw = "#639a67"
    btn_color_passw = "#7cb518"
    close_btn_passw = "#5c8001"

    parser = ConfigParser()
    filee = "config.ini"
    parser.read(filee)
    password = parser.get("account", "password")

    password_top = Toplevel(background=bg_passw)
    password_top.overrideredirect(True)
    w = frame_bg.winfo_width()
    h = root.winfo_height()

    bg_w = video_label.winfo_width()
    ww = int(0.4 * w)
    password_top.geometry('%dx%d+%d+%d' % (ww, h, w - ww, 0))
    password_top.resizable(False, False)
    password_top.wm_attributes('-topmost', 1)
    password_top.wait_visibility()  # Wait until the visibility of a WIDGET changes
    password_top.grab_set()

    password_top.columnconfigure(0, weight=1)
    password_top.rowconfigure(0, weight=2)
    password_top.rowconfigure(1, weight=2)
    password_top.rowconfigure(2, weight=1)
    password_top.rowconfigure(3, weight=2)
    password_top.rowconfigure(4, weight=2)
    password_top.rowconfigure(5, weight=1)
    password_top.rowconfigure(6, weight=2)
    password_top.rowconfigure(7, weight=2)
    password_top.rowconfigure(8, weight=1)
    password_top.rowconfigure(9, weight=4)
    password_top.rowconfigure(10, weight=16)
    password_top.rowconfigure(11, weight=3)
    '''////////////////////////////////////////'''
    var_password = StringVar()
    var_password.trace('w', control_old_password)
    var_new_password = StringVar()
    var_new_password.trace('w', control_new_password)
    var_again_new_password = StringVar()
    var_again_new_password.trace('w', control_again_new_password)
    '''////////////////////////////////////////'''
    info_passw = "* yeni şifre 4-12 uzunluğunda olmalıdır *"
    '''////////////////////////////////////////'''
    lbl_empty_add_user_ = Label(password_top, bg=bg_passw, border=0, width=15)
    lbl_empty_add_user_.grid(column=0, row=0, sticky="n")
    '''////////////////////////////////////////'''

    lbl_passw = Label(password_top, text="Mevcut Şifrenizi Girin: ", bg=bg_passw, font=("bold", 15), border=0, width=25)
    lbl_passw.grid(column=0, row=1, sticky="s")

    entry_passw = Entry(password_top, textvar=var_password, highlightthickness=0, border=0, show="*", width=25)
    entry_passw.grid(column=0, row=2)

    '''////////////////////////////////////////'''
    lbl_empty_add_user_p = Label(password_top, bg=bg_passw, border=0, width=15)
    lbl_empty_add_user_p.grid(column=0, row=3, sticky="n")
    '''////////////////////////////////////////'''

    lbl_new_passw = Label(password_top, text="Yeni Şifrenizi Girin: ", bg=bg_passw, font=("bold", 15), border=0, width=25)
    lbl_new_passw.grid(column=0, row=4, sticky="s")

    entry_new_passw = Entry(password_top, textvar=var_new_password, highlightthickness=0, state=DISABLED, show="*",
                            border=0, width=25)
    entry_new_passw.grid(column=0, row=5)

    '''////////////////////////////////////////'''
    lbl_empty_add_user_n = Label(password_top, bg=bg_passw, border=0, width=15)
    lbl_empty_add_user_n.grid(column=0, row=6, sticky="n")
    '''////////////////////////////////////////'''

    lbl_again_new_passw = Label(password_top, text="Yeni Şifrenizi Tekrar Girin: ", bg=bg_passw, font=("bold", 15), border=0,
                                width=25)
    lbl_again_new_passw.grid(column=0, row=7, sticky="s")

    entry_again_new_passw = Entry(password_top, textvar=var_again_new_password, highlightthickness=0, state=DISABLED,
                                  border=0, show="*", width=25)
    entry_again_new_passw.grid(column=0, row=8)

    '''////////////////////////////////////////'''
    lbl_empty_add_user_g = Label(password_top, bg=bg_passw, border=0, width=15)
    lbl_empty_add_user_g.grid(column=0, row=9, sticky="n")
    '''////////////////////////////////////////'''

    warning_lbl = Label(password_top, text=f"{info_passw}", bg=bg_passw, font=("bold", 15), fg=warning_font_color_passw, border=0, width=50)
    warning_lbl.grid(column=0, row=10, sticky="nsew")

    '''////////////////////////////////////////'''
    keyboard_lbl = Label(password_top, font=("bold", 13), border=0, bg=bg_passw)
    keyboard_lbl.grid(column=0, row=11, sticky="nsew")
    keyboard(keyboard_lbl, entry_passw)
    '''////////////////////////////////////////'''
    buttons_lbl_passw = Label(password_top, border=0)
    buttons_lbl_passw.grid(column=0, row=12, sticky="nsew")
    buttons_lbl_passw.columnconfigure(0, weight=1)
    buttons_lbl_passw.columnconfigure(1, weight=1)
    buttons_lbl_passw.columnconfigure(2, weight=1)
    buttons_lbl_passw.rowconfigure(0, weight=1)

    btn_back = Button(buttons_lbl_passw, text="Kapat", bg=close_btn_passw, border=0, highlightthickness=0,
                      font="Helvetica 20", command=password_top.destroy)
    btn_back.grid(column=0, row=0, sticky="nsew")

    btn_delete = Button(buttons_lbl_passw, text="Sil", bg=btn_color_passw, border=0, highlightthickness=0,
                        font="Helvetica 20", command=delete_char)
    btn_delete.grid(column=1, row=0, sticky="nsew")

    btn_change_passw = Button(buttons_lbl_passw, text="Enter", bg=btn_color_passw, border=0, highlightthickness=0,
                              font="Helvetica 20")
    btn_change_passw.grid(column=2, row=0, sticky="nsew")
    btn_change_passw.bind("<Button-1>", btn_change_password_clicker)

def door_register():
    pass

def btn_recog_clicker(event):
    global icon_left
    global press
    global thread_check
    global thread_stop
    global user_top

    if thread_check:
        thread_stop = True
        btn_recog.config(image=icon_left)
        t_rec = threading.Thread(target=run)
        t_run_info = threading.Thread(target=run_info, daemon=True)
        t_rec.start()
        t_run_info.start()
        thread_check = False

    else:
        thread_stop = False
        time.sleep(1)
        video_label.configure(image=img1)
        btn_recog.config(image=icon_recog)
        thread_check = True
def btn_add_user_clicker(event):
    global thread_check
    global thread_stop

    if thread_check:
        thread_stop = True
        btn_recog.config(image=icon_left)
        t_rec = threading.Thread(target=run)
        t_run_info = threading.Thread(target=run_info)
        t_rec.start()
        t_run_info.start()
        thread_check = False
        time.sleep(1)
    add_user()
def btn_delete_user_clicker(event):
    global thread_check
    global thread_stop

    if thread_check:
        thread_stop = True
        btn_recog.config(image=icon_left)
        t_rec = threading.Thread(target=run)
        t_run_info = threading.Thread(target=run_info)
        t_rec.start()
        t_run_info.start()
        thread_check = False
        time.sleep(1)
    delete_user()
def btn_register_password_clicker(event):
    global thread_check
    global thread_stop

    if thread_check:
        thread_stop = True
        # btn_recog.config(image=icon_left)
        # t_rec = threading.Thread(target=run)
        # t_run_info = threading.Thread(target=run_info)
        # t_rec.start()
        # t_run_info.start()
        thread_check = False
        time.sleep(1)
    password_register()

'''///////////////////////////////////////'''
root = Tk()
root.geometry("800x480")
# root.wm_attributes('-fullscreen', 'true')
# root.wm_attributes('-topmost', 1)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
press = 0
'''///////////////////////////////////////'''

content = ttk.Frame(root)
content.grid(column=0, row=0)
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=3)
content.rowconfigure(1, weight=1)
'''///////////////////////////////////////'''

frame_bg = Label(content, border=0, bg="#f7f7f7")
frame_bg.grid(column=0, row=0, sticky=("nsew"))

video_label = Label(frame_bg, border=0, bg="#8d3f76")
video_label.grid(column=0, row=0, sticky=("nsew"))  ##
image = Image.open(f"{img_path}/black_blu_2.png")
img1 = ImageTk.PhotoImage(image)
video_label.configure(image=img1)
'''///////////////////////////////////////'''
options_lbl = Label(content, border=0, bg="#fbc531")  # , height=int(content.winfo_height()/5)
options_lbl.grid(column=0, row=1, sticky="nsew")

options_lbl.columnconfigure(0, weight=1)
options_lbl.columnconfigure(1, weight=1)
options_lbl.columnconfigure(2, weight=1)
options_lbl.columnconfigure(3, weight=1)
options_lbl.columnconfigure(4, weight=1)
options_lbl.rowconfigure(0, weight=1)

icon_left = PhotoImage(file=f"{img_path}/left.png")
icon_left = icon_left.subsample(5, 5)

icon_recog = PhotoImage(file=f"{img_path}/face-scan.png")
icon_recog = icon_recog.subsample(5, 5)

icon_add = PhotoImage(file=f"{img_path}/add-userr.png")
icon_add = icon_add.subsample(5, 5)

icon_delete = PhotoImage(file=f"{img_path}/delete-user.png")
icon_delete = icon_delete.subsample(5, 5)

icon_door = PhotoImage(file=f"{img_path}/open-door.png")
icon_door = icon_door.subsample(5, 5)

icon_passw = PhotoImage(file=f"{img_path}/padlock.png")
icon_passw = icon_passw.subsample(5, 5)

'''///////////////////////////////////////'''
addToLabels()
'''///////////////////////////////////////'''

btn_recog = Button(options_lbl, image=icon_recog, justify="center", border=0, bg="#7bed9f", highlightthickness=0)
btn_recog.bind("<Button-1>", btn_recog_clicker)
btn_recog.grid(column=0, row=0, sticky="nsew")

btn_user_add = Button(options_lbl, image=icon_add, justify="center", border=0, bg="#70a1ff", highlightthickness=0)
btn_user_add.bind("<Button-1>", btn_add_user_clicker)
btn_user_add.grid(column=1, row=0, sticky="nsew")

btn_user_delete = Button(options_lbl, image=icon_delete, justify="center", border=0, bg="#B33771",
                         highlightthickness=0)  # , command=delete_user
btn_user_delete.bind("<Button-1>", btn_delete_user_clicker)
btn_user_delete.grid(column=2, row=0, sticky="nsew")

btn_door = Button(options_lbl, image=icon_door, justify="center", border=0, bg="#a4b0be", highlightthickness=0,
                  command=door_register)
btn_door.grid(column=3, row=0, sticky="nsew")

btn_passw = Button(options_lbl, image=icon_passw, justify="center", border=0, bg="#A75454", highlightthickness=0)
btn_passw.bind("<Button-1>", btn_register_password_clicker)

btn_passw.grid(column=4, row=0, sticky="nsew")

root.mainloop()