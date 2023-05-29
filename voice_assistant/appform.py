import threading
from tkinter import *
from PIL import Image
from tools import *
import customtkinter as CTk
import os


class App(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.answer = None
        CTk.set_appearance_mode("light")
        self.win_width = CTk.CTk.winfo_screenwidth(self)
        self.win_height = CTk.CTk.winfo_screenheight(self)
        self.geometry(f"+{self.win_width-350}+{self.win_height-650}")
        self.maxsize(290, 510), self.minsize(290, 510)
        self.resizable(False, False)
        self.title('abc')
        self.input_image = CTk.CTkImage(light_image=Image.open('image/btn3.png'),
                                        size=(29, 29))
        self.voice_image = CTk.CTkImage(light_image=Image.open('image/btn4.png'),
                                        size=(25, 25))
        self.text_field = CTk.CTkScrollableFrame(master=self, height=380, fg_color='#ebebeb')
        self.text_field.pack(side=TOP, fill=BOTH)
        self.voice_btn = CTk.CTkButton(master=self, image=self.voice_image, command=self.voice_record,
                                       fg_color='transparent',
                                       width=3, height=3, hover=False)
        self.voice_btn.place(x=5, y=480)
        self.entry = CTk.CTkEntry(master=self, width=210)
        self.entry.pack(side=BOTTOM)
        self.send_btn = CTk.CTkButton(master=self, image=self.input_image, command=self.msg_send,
                                      fg_color='transparent',
                                      width=3, height=3, hover=False)
        self.send_btn.place(x=250, y=477)
        self.bind("<KP_Enter>", self.msg_send)

    def add_button(self, values, btn_type):
        if btn_type == 1:
            self.answer_btn = CTk.CTkSegmentedButton(master=self, values=values,
                                                     command=self.segmented_button_callback)
            self.answer_btn.pack(side=BOTTOM, fill=X, pady=5)
        elif btn_type == 2:
            self.answer_btn = CTk.CTkOptionMenu(master=self, values=values,
                                                command=self.segmented_button_callback)
            self.answer_btn.pack(side=BOTTOM, fill=X, pady=5)

    def segmented_button_callback(self, value):
        self.answer_btn.destroy()
        self.answer = value
        self.add_label(2, value)

    def msg_send(self, event=None):
        msg = self.entry.get()
        try:
            self.answer_btn.destroy()
        except AttributeError:
            pass
        self.entry.delete(0, len(msg))
        self.add_label(2, msg)
        self.answer = msg

    def add_label(self, face, text):
        if face == 1:
            new_label = CTk.CTkLabel(master=self.text_field, text=f'{text}',
                                     wraplength=150, fg_color='#FFE4B5', corner_radius=10)
            new_label.pack(ipadx=10, anchor=NW, pady=10)
        else:
            new_label = CTk.CTkLabel(master=self.text_field, text=f'{text}',
                                     wraplength=150, fg_color='#87CEEB', corner_radius=10)
            new_label.pack(ipadx=10, anchor=NE)

    def voice_record(self):
        thread = threading.Thread(target=self.voice_record_thread, args=())
        thread.start()

    def voice_record_thread(self):
        self.record = record_and_recognize_audio()
        self.add_label(2, self.record)
        os.remove("microphone-results.wav")

    def return_link(self, tag, city_id, city):
        link = f'https://job.alfabank.ru/api/vacancies?city={city_id}&radius=0000&tag={tag}&take=20'
        print(link)
        response = requests.get(link)
        result = response.json()
        if len(result['items']) == 0:
            self.add_label(1, "Нет подходящих вакансий")
        for i in range(len(result['items'])):
            job_link = f"https://job.alfabank.ru/vacancies{result['items'][i]['slug']}"
            name = result['items'][i]['name']
            link1 = CTk.CTkLabel(master=self.text_field, text=name, wraplength=150, fg_color='#FFE4B5',
                                 corner_radius=10, cursor='hand2')
            link1.pack(ipadx=10, anchor=NW)
            link1.bind("<Button-1>", lambda e: callback(job_link))

