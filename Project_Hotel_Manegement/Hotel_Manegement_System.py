import tkinter as tk
import os
import sqlite3
from tkcalendar import *
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import scrolledtext
import hashlib
from datetime import date
from Project_Hotel_Manegement import database
from LanguagePack import I18N
from PIL import ImageTk, Image
import re


class GlobalVariables:

    def __init__(self):
        self.usernameLogin = ""
        self.i18n = I18N("en")

    def setUsername(self, u):
        self.usernameLogin = u

    def getUsername(self):
        return self.usernameLogin

    def validation_check(self, input_string, regex_string):
        regex = re.compile(regex_string)
        match = regex.match(input_string)
        return bool(match)


myVars = GlobalVariables()


class Win1:

    def __init__(self):
        self.welcome_win = tk.Tk()
        self.welcome_win.title(myVars.i18n.welcome)
        self.welcome_win.resizable(False, False)
        self.welcome_win.iconbitmap("hotel.ico")
        self.create_widgets()

        win_width = 450
        win_height = 500

        screen_width = self.welcome_win.winfo_screenwidth()
        screen_height = self.welcome_win.winfo_screenheight()

        x = int((screen_width / 2) - (win_width / 2))
        y = int((screen_height / 2) - (win_height / 2))

        self.welcome_win.geometry(f"{win_width}x{win_height}+{x}+{y}")

    def login_handler(self):
        self.welcome_win.destroy()
        w2 = Win2()
        w2.login_window.focus_force()

    def signup_handler(self):
        self.welcome_win.destroy()
        w3 = Win3()
        w3.signup_window.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.welcome_win.title(myVars.i18n.welcome)
        self.button_login.configure(text=myVars.i18n.login)
        self.button_signup.configure(text=myVars.i18n.signup)
        self.welcome_label.configure(text=myVars.i18n.elipor)
        self.language_label.configure(text=myVars.i18n.lang_select_note)

    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.welcome_win)
        main_frame.pack(expand=True)

        image = Image.open('welcomePage.png')
        resized = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=0, columnspan=2)

        self.welcome_label = tk.Label(main_frame, font=('OpenSans', 13, "bold"), text=myVars.i18n.elipor)
        self.welcome_label.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.button_login = ttk.Button(main_frame, text=myVars.i18n.login, style='my.TButton',
                                       command=self.login_handler)
        self.button_login.grid(column=0, row=2, padx=5, pady=25)

        self.button_signup = ttk.Button(main_frame, text=myVars.i18n.signup, style='my.TButton',
                                        command=self.signup_handler)
        self.button_signup.grid(column=1, row=2, padx=5, pady=25)

        self.language_label = tk.Label(main_frame, text=myVars.i18n.lang_select_note, font=('FontAwesome', 9, "italic"))
        self.language_label.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

        self.welcome_win.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.welcome_win.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win2:

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title(myVars.i18n.login)
        self.login_window.geometry("550x450+710+290")
        self.login_window.resizable(False, False)
        self.login_window.iconbitmap("hotel.ico")
        self.create_widgets()

    def homepage_handler(self):
        if self.username.get() == "":
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.name_error)
        elif self.password.get() == "":
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.password_error)
        else:
            conn = sqlite3.connect("hotel.db")
            cur = conn.cursor()

            cur.execute("SELECT COUNT(username) FROM tblUser WHERE username=:username AND password=:password",
                        {"username": self.username.get(),
                         "password": hashlib.md5(self.password.get().encode()).hexdigest()})
            row = cur.fetchone()
            conn.close()
            if len(row) > 0 and int(row[0]) > 0:
                myVars.setUsername(self.username.get())
                self.login_window.destroy()
                w4 = Win4()
                w4.homepage_window.focus_force()
            else:
                msg.showerror(title=myVars.i18n.error, message=myVars.i18n.mismatched)

    def return_welcome_page(self):
        self.login_window.destroy()
        w1 = Win1()
        w1.welcome_win.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.login_window.title(myVars.i18n.login)
        self.username_label.configure(text=myVars.i18n.username)
        self.password_label.configure(text=myVars.i18n.password)
        self.login_button.configure(text=myVars.i18n.login)
        self.back_button.configure(text=myVars.i18n.back)

    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.login_window)
        main_frame.pack(expand=True)

        image = Image.open('login.png')
        resized = image.resize((512, 290), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        self.username_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.username)
        self.username_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)

        self.password_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.password)
        self.password_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)

        self.username = tk.StringVar()
        self.username_entered = ttk.Entry(main_frame, textvariable=self.username, font=('OpenSans', 11))
        self.username_entered.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
        self.username_entered.focus()

        self.password = tk.StringVar()
        self.password_entered = ttk.Entry(main_frame, textvariable=self.password, font=('OpenSans', 11))
        self.password_entered.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)
        self.password_entered.config(show="*")

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.login_button = ttk.Button(main_frame, text=myVars.i18n.login, style='my.TButton',
                                       command=self.homepage_handler)
        self.login_button.grid(column=1, row=3, padx=5, pady=5, sticky=tk.E)

        self.back_button = ttk.Button(main_frame, text=myVars.i18n.back, style='my.TButton',
                                      command=self.return_welcome_page)
        self.back_button.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.login_window.bind("<Escape>", lambda e: self.return_welcome_page())
        self.login_window.bind("<Return>", lambda e: self.homepage_handler())
        self.login_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.login_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win3:

    def __init__(self):
        self.signup_window = tk.Tk()
        self.signup_window.title(myVars.i18n.signup)
        self.signup_window.geometry("600x350+710+290")
        self.signup_window.resizable(False, False)
        self.signup_window.iconbitmap("hotel.ico")
        self.rpassword = tk.StringVar()
        self.password = tk.StringVar()
        self.username = tk.StringVar()
        self.pNo = tk.StringVar()
        self.surname = tk.StringVar()
        self.name = tk.StringVar()
        self.create_widgets()

    def add_to_database(self):
        if self.name.get() == "" or not myVars.validation_check(self.name.get(),
                                                                "[a-zA-ZıİöçğşüÖÇĞŞÜ]{2,20}([ ]?[a-zA-ZıİöçğşüÖÇĞŞÜ]{2,20})?"):
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.name_error)
        elif self.surname.get() == "" or not myVars.validation_check(self.surname.get(),
                                                                     "[a-zA-ZıİöçğşüÖÇĞŞÜ]{2,20}([ ]?[a-zA-ZıİöçğşüÖÇĞŞÜ]{2,20})?"):
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.surname_error)
        elif self.pNo.get() == "" or not myVars.validation_check(self.pNo.get(), "[+]?[0-9]{9,20}"):
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.pNo_error)
        elif self.username.get() == "" or not myVars.validation_check(self.username.get(),
                                                                      "[a-zA-Z-_\.0-9ıİöçğşüÖÇĞŞÜ]{5,15}"):
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.username_error)
        elif self.password.get() == "" or not myVars.validation_check(self.password.get(),
                                                                      "(?=.*[a-zıİöçğşüÖÇĞŞÜ])(?=.*[A-ZıİöçğşüÖÇĞŞÜ)(?=.*[0-9])[\w\d.].{6,}"):
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.password_error)
        elif self.rpassword.get() != self.password.get():
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.password_mismatched)
        else:
            conn = sqlite3.connect("hotel.db")
            cur = conn.cursor()

            cur.execute("SELECT COUNT(username) FROM tblUser WHERE username=:username",
                        {"username": self.username.get()})
            row = cur.fetchone()
            if len(row) > 0 and int(row[0]) > 0:
                conn.close()
                msg.showerror(title=myVars.i18n.error, message=myVars.i18n.username_exist)
            else:
                cur.execute("INSERT INTO tblUser(name, surname, pNo, username, password) VALUES(:name, :surname, "
                            ":number, :username, :password)",
                            {"name": self.name.get(),
                             "surname": self.surname.get(),
                             "number": self.pNo.get(),
                             "username": self.username.get(),
                             "password": hashlib.md5(self.password.get().encode()).hexdigest()})
                conn.commit()
                conn.close()
                myVars.setUsername(self.username.get())
                self.signup_window.destroy()
                w4 = Win4()
                w4.homepage_window.focus_force()

    def return_welcome_page(self):
        self.signup_window.destroy()
        w1 = Win1()
        w1.welcome_win.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.signup_window.title(myVars.i18n.signup)
        self.name_label.configure(text=myVars.i18n.name)
        self.surname_label.configure(text=myVars.i18n.surname)
        self.pNo_label.configure(text=myVars.i18n.pno)
        self.username_label.configure(text=myVars.i18n.username)
        self.password_label.configure(text=myVars.i18n.password)
        self.rPassword_label.configure(text=myVars.i18n.rpassword)
        self.signup_button.configure(text=myVars.i18n.signup)
        self.back_button.configure(text=myVars.i18n.back)

    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.signup_window)
        main_frame.pack(expand=True)

        image = Image.open('signup.png')
        resized = image.resize((190, 280), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=2, row=0, rowspan=7, padx=5, pady=5)

        self.name_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.name)
        self.name_label.grid(column=0, row=0, padx=18, pady=10, sticky=tk.W)

        self.surname_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.surname)
        self.surname_label.grid(column=0, row=1, padx=18, pady=10, sticky=tk.W)

        self.pNo_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.pno)
        self.pNo_label.grid(column=0, row=2, padx=18, pady=10, sticky=tk.W)

        self.username_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.username)
        self.username_label.grid(column=0, row=3, padx=18, pady=10, sticky=tk.W)

        self.password_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.password)
        self.password_label.grid(column=0, row=4, padx=18, pady=10, sticky=tk.W)

        self.rPassword_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.rpassword)
        self.rPassword_label.grid(column=0, row=5, padx=18, pady=10, sticky=tk.W)

        self.name_entered = ttk.Entry(main_frame, textvariable=self.name, font=('OpenSans', 11))
        self.name_entered.grid(column=1, row=0, padx=18, pady=10)
        self.name_entered.focus()

        self.surname_entered = ttk.Entry(main_frame, textvariable=self.surname, font=('OpenSans', 11))
        self.surname_entered.grid(column=1, row=1, padx=18, pady=10)

        self.pNo_entered = ttk.Entry(main_frame, textvariable=self.pNo, font=('OpenSans', 11))
        self.pNo_entered.grid(column=1, row=2, padx=18, pady=10)

        self.username_entered = ttk.Entry(main_frame, textvariable=self.username, font=('OpenSans', 11))
        self.username_entered.grid(column=1, row=3, padx=18, pady=10)

        self.password_entered = ttk.Entry(main_frame, textvariable=self.password, font=('OpenSans', 11))
        self.password_entered.grid(column=1, row=4, padx=18, pady=10)
        self.password_entered.config(show="*")

        self.rpassword_entered = ttk.Entry(main_frame, textvariable=self.rpassword, font=('OpenSans', 11))
        self.rpassword_entered.grid(column=1, row=5, padx=18, pady=10)
        self.rpassword_entered.config(show="*")

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.signup_button = ttk.Button(main_frame, text=myVars.i18n.signup, style='my.TButton',
                                        command=self.add_to_database)
        self.signup_button.grid(column=1, row=6, padx=18, pady=10, sticky=tk.NSEW)

        self.back_button = ttk.Button(main_frame, text=myVars.i18n.back, style='my.TButton',
                                      command=self.return_welcome_page)
        self.back_button.grid(column=0, row=6, padx=18, pady=10, sticky=tk.NSEW)

        self.signup_window.bind("<Escape>", lambda e: self.return_welcome_page())
        self.signup_window.bind("<Return>", lambda e: self.add_to_database())
        self.signup_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.signup_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win4:

    def __init__(self):
        self.homepage_window = tk.Tk()
        self.homepage_window.title(myVars.i18n.homepage)
        self.homepage_window.geometry("930x790+610+150")
        self.homepage_window.resizable(False, False)
        self.homepage_window.iconbitmap("hotel.ico")
        self.create_widgets()

    def options_handler(self):
        self.homepage_window.destroy()
        w5 = Win5()
        w5.options_window.focus_force()

    def history_handler(self):
        self.homepage_window.destroy()
        w7 = Win7()
        w7.history_window.focus_force()

    def return_welcome_page(self):
        self.homepage_window.destroy()
        w1 = Win1()
        w1.welcome_win.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.homepage_window.title(myVars.i18n.homepage)
        self.menu_bar.entryconfigure(1, label=myVars.i18n.reservation)
        self.file_menu.entryconfigure(0, label=myVars.i18n.new_reservation)
        self.file_menu.entryconfigure(2, label=myVars.i18n.reservation_history)
        self.exit_button.configure(text=myVars.i18n.signout)
        self.hotel_label.configure(text=myVars.i18n.home_elipor)
        self.info_label1.configure(text=myVars.i18n.info1)
        self.info_label2.configure(text=myVars.i18n.info2)
        self.info_label3.configure(text=myVars.i18n.info3)

    def create_widgets(self):
        global photo

        main_frame = tk.LabelFrame(self.homepage_window)
        main_frame.pack(expand=True)

        self.menu_bar = Menu(main_frame)
        self.homepage_window.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=myVars.i18n.reservation, font=('FontAwesome', 10, "bold"), menu=self.file_menu)
        self.file_menu.add_command(label=myVars.i18n.new_reservation, font=('FontAwesome', 9, "bold"),
                                   command=self.options_handler)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=myVars.i18n.reservation_history, font=('FontAwesome', 9, "bold"),
                                   command=self.history_handler)

        self.hotel_label = tk.Label(main_frame, text=myVars.i18n.home_elipor, font=('Times', 17, "bold"))
        self.hotel_label.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        image = Image.open('home.png')
        resized = image.resize((650, 433), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized)

        image_label = tk.Label(main_frame, image=photo)
        image_label.grid(column=0, row=1, columnspan=2)

        self.info_label1 = tk.Label(main_frame, text=myVars.i18n.info1, font=('OpenSans', 13, "bold"))
        self.info_label1.grid(column=0, row=2, columnspan=2, padx=5, pady=5)

        self.info_label2 = tk.Label(main_frame, text=myVars.i18n.info2, font=('OpenSans', 12))
        self.info_label2.grid(column=0, row=3, columnspan=2, padx=5, pady=5)

        self.info_label3 = tk.Label(main_frame, text=myVars.i18n.info3, font=('FontAwesome', 9, "italic"))
        self.info_label3.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.exit_button = ttk.Button(main_frame, style='my.TButton', text=myVars.i18n.signout,
                                      command=self.return_welcome_page)
        self.exit_button.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)

        self.homepage_window.bind("<Escape>", lambda e: self.return_welcome_page())
        self.homepage_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.homepage_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win5:
    def __init__(self):
        self.options_window = tk.Tk()
        self.options_window.title(myVars.i18n.options_main)
        self.options_window.geometry("950x550+610+290")
        self.options_window.iconbitmap("hotel.ico")
        self.options_window.resizable(False, False)
        self.country = myVars.i18n.countryList
        self.number = (myVars.i18n.select, 1, 2, 3, 4, 5)
        self.rd1 = tk.StringVar()
        self.create_widgets()

    def complete_handler(self):
        if self.country_entered.current() < 1:
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.country_error)
        elif self.city_entered.current() < 1:
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.city_error)
        elif self.number_of_people_chosen.current() < 1:
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.no_of_people_error)
        elif self.number_of_room_chosen.current() < 1:
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.no_of_room_error)
        elif self.cal1.selection_get() == self.cal2.selection_get() or self.cal1.selection_get() > self.cal2.selection_get():
            msg.showerror(title=myVars.i18n.error, message=myVars.i18n.date_error)
        else:
            message = msg.askyesno(title=myVars.i18n.complete, message=myVars.i18n.are_you_sure_2)
            if message:
                conn = sqlite3.connect("hotel.db")
                cur = conn.cursor()

                cur.execute("INSERT INTO tblReservation(username, country, city, numberOfPeople, numberOfRoom, view, "
                            "breakfast, ac, rs, reservationDate, visitStartDate, visitFinishDate) VALUES(:username, "
                            ":country, :city, :numberOfPeople, :numberOfRoom, :view, :breakfast, :ac, :rs, "
                            ":reservationDate, :visitStartDate, :visitFinishDate)",
                            {"username": myVars.getUsername(),
                             "country": self.country_entered.get(),
                             "city": self.city_entered.get(),
                             "numberOfPeople": self.number_of_people_chosen.get(),
                             "numberOfRoom": self.number_of_room_chosen.get(),
                             "view": self.radiobutton_controller().get(),
                             "breakfast": (self.ch1s.get() and f"{myVars.i18n.yes}" or f"{myVars.i18n.no}"),
                             "ac": self.ch2s.get() and f"{myVars.i18n.yes}" or f"{myVars.i18n.no}",
                             "rs": self.ch3s.get() and f"{myVars.i18n.yes}" or f"{myVars.i18n.no}",
                             "reservationDate": str(date.today()),
                             "visitStartDate": self.cal1.selection_get(),
                             "visitFinishDate": self.cal2.selection_get()
                             })
                conn.commit()
                conn.close()

                w6 = Win6()
                w6.thanks_window.focus_force()
                w6.scr_text.insert(tk.INSERT, f"{myVars.i18n.country} {self.country_entered.get()}\n"
                                              f"{myVars.i18n.city} {self.city_entered.get()}"
                                              f"\n{myVars.i18n.people} {self.number_of_people_chosen.get()}"
                                              f"\n{myVars.i18n.room} {self.number_of_room_chosen.get()}"
                                              f"\n{myVars.i18n.selected_view} {self.radiobutton_controller().get()}"
                                              f"\n{myVars.i18n.selected_options} {self.checkbox_controller().get()}"
                                              f"\n{myVars.i18n.start_day} {self.cal1.selection_get()}"
                                              f"\n{myVars.i18n.finish_day} {self.cal2.selection_get()}")
                w6.scr_text.configure(state="disabled")
                w6.empty_label.configure(text=str(cur.lastrowid))
                self.options_window.destroy()

    def checkbox_controller(self):
        string_list = tk.StringVar()
        if self.ch1s.get():
            string_list.set(string_list.get() + f"\n{myVars.i18n.breakfast}")
        if self.ch2s.get():
            string_list.set(string_list.get() + f"\n{myVars.i18n.ac}")
        if self.ch3s.get():
            string_list.set(string_list.get() + f"\n{myVars.i18n.rs}")
        elif not self.ch1s.get() and not self.ch2s.get() and not self.ch3s.get():
            string_list.set(string_list.get() + f"\n{myVars.i18n.notspecified}")

        return string_list

    def radiobutton_controller(self):
        string_list = tk.StringVar()
        if self.rd1.get() == "City View":
            string_list.set(string_list.get() + f"{myVars.i18n.city_view}")
        if self.rd1.get() == "Sea View":
            string_list.set(string_list.get() + f"{myVars.i18n.sea_view}")
        if self.rd1.get() == "Nature View":
            string_list.set(string_list.get() + f"{myVars.i18n.nature_view}")
        if self.rd1.get() == "Not Specified":
            string_list.set(string_list.get() + f"{myVars.i18n.notspecified}")

        return string_list

    def homepage_handler(self):
        self.options_window.destroy()
        w4 = Win4()
        w4.homepage_window.focus_force()

    def getUpdateData(self, event):
        self.city_entered['values'] = self.country[self.country_entered.get()]
        self.city_entered.current(0)

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.country = myVars.i18n.countryList
        self.number = (myVars.i18n.select, 1, 2, 3, 4, 5)
        self.options_window.title(myVars.i18n.options_main)
        self.country_label.configure(text=myVars.i18n.country)
        self.city_label.configure(text=myVars.i18n.city)
        self.peopleNo_label.configure(text=myVars.i18n.people)
        self.roomNo_label.configure(text=myVars.i18n.room)
        self.room_type_label.configure(text=myVars.i18n.room_type)
        self.options_label.configure(text=myVars.i18n.options)
        self.rd1c.configure(text=myVars.i18n.city_view)
        self.rd2s.configure(text=myVars.i18n.sea_view)
        self.rd3n.configure(text=myVars.i18n.nature_view)
        self.rd4n.configure(text=myVars.i18n.notspecified)
        self.ch1.configure(text=myVars.i18n.breakfast)
        self.ch2.configure(text=myVars.i18n.ac)
        self.ch3.configure(text=myVars.i18n.rs)
        self.cal1_label.configure(text=myVars.i18n.start_day)
        self.cal2_label.configure(text=myVars.i18n.finish_day)
        self.back_button.configure(text=myVars.i18n.back)
        self.complete_reservation.configure(text=myVars.i18n.complete)
        self.country_entered.configure(values=list(myVars.i18n.countryList.keys()))
        self.country_entered.current(0)
        self.number_of_room_chosen.configure(values=self.number)
        self.number_of_room_chosen.current(0)
        self.number_of_people_chosen.configure(values=self.number)
        self.number_of_people_chosen.current(0)
        self.getUpdateData(None)
        self.price_label.configure(text=myVars.i18n.price_label)

    def create_widgets(self):
        main_frame = tk.LabelFrame(self.options_window)
        main_frame.pack(expand=True)

        self.country_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.country)
        self.country_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.country_entered = ttk.Combobox(main_frame, font=('OpenSans', 11), values=list(self.country.keys()),
                                            width=17, state="readonly")
        self.country_entered.bind('<<ComboboxSelected>>', self.getUpdateData)
        self.country_entered.grid(column=1, row=0, padx=5, pady=5, sticky=tk.E)
        self.country_entered.current(0)

        self.city_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.city)
        self.city_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.city_entered = ttk.Combobox(main_frame, font=('OpenSans', 11),
                                         values=self.country[self.country_entered.get()], width=17, state="readonly")
        self.city_entered.grid(column=1, row=1, padx=5, pady=5, sticky=tk.E)
        self.city_entered.current(0)

        self.peopleNo_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.people)
        self.peopleNo_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.number_of_people_chosen = ttk.Combobox(main_frame, font=('OpenSans', 11), width=17,
                                                    values=self.number, state="readonly")
        self.number_of_people_chosen.grid(column=1, row=2, padx=5, pady=5, sticky=tk.E)
        self.number_of_people_chosen.current(0)

        self.roomNo_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.room)
        self.roomNo_label.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.number_of_room_chosen = ttk.Combobox(main_frame, font=('OpenSans', 11), width=17, values=self.number,
                                                  state="readonly")
        self.number_of_room_chosen.grid(column=1, row=3, padx=5, pady=5, sticky=tk.E)
        self.number_of_room_chosen.current(0)

        self.room_type_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.room_type)
        self.room_type_label.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)

        self.rd1.set(value="Not Specified")
        self.rd1c = tk.Radiobutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.city_view, variable=self.rd1,
                                   value="City View")
        self.rd1c.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)

        self.rd2s = tk.Radiobutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.sea_view, variable=self.rd1,
                                   value="Sea View")
        self.rd2s.grid(column=2, row=4, padx=5, pady=5, sticky=tk.W)

        self.rd3n = tk.Radiobutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.nature_view,
                                   variable=self.rd1, value="Nature View")
        self.rd3n.grid(column=3, row=4, padx=5, pady=5, sticky=tk.W)

        self.rd4n = tk.Radiobutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.notspecified,
                                   variable=self.rd1, value="Not Specified")
        self.rd4n.grid(column=4, row=4, padx=5, pady=5, sticky=tk.W)

        self.options_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.options)
        self.options_label.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)

        self.ch1s = tk.IntVar()
        self.ch1 = tk.Checkbutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.breakfast, variable=self.ch1s)
        self.ch1.grid(column=1, row=5, padx=5, pady=5, sticky=tk.W)

        self.ch2s = tk.IntVar()
        self.ch2 = tk.Checkbutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.ac, variable=self.ch2s)
        self.ch2.grid(column=2, row=5, padx=5, pady=5, sticky=tk.W)

        self.ch3s = tk.IntVar()
        self.ch3 = tk.Checkbutton(main_frame, font=('OpenSans', 11), text=myVars.i18n.rs, variable=self.ch3s)
        self.ch3.grid(column=3, row=5, padx=5, pady=5, sticky=tk.W)

        self.cal1_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.start_day)
        self.cal1_label.grid(column=1, row=6, columnspan=3, padx=5, pady=5, sticky=tk.W)

        self.cal2_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.finish_day)
        self.cal2_label.grid(column=4, row=6, padx=5, pady=5, sticky=tk.NSEW)

        self.today = date.today()

        self.cal1 = Calendar(main_frame, font=('OpenSans', 11, "bold"), selectmode="day", year=self.today.year,
                             month=self.today.month, day=self.today.day)
        self.cal1.grid(column=0, row=7, columnspan=3, padx=30, pady=5, sticky=tk.W)

        self.cal2 = Calendar(main_frame, font=('OpenSans', 11, "bold"), selectmode="day", year=self.today.year,
                             month=self.today.month, day=self.today.day)
        self.cal2.grid(column=4, row=7, padx=20, pady=5)

        s = ttk.Style()
        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.complete_reservation = ttk.Button(main_frame, style='my.TButton', text=myVars.i18n.complete,
                                               command=self.complete_handler)
        self.complete_reservation.grid(column=4, row=9, padx=5, pady=5, sticky=tk.E)

        self.back_button = ttk.Button(main_frame, style='my.TButton', text=myVars.i18n.back,
                                      command=self.homepage_handler)
        self.back_button.grid(column=0, row=9, padx=5, pady=5, sticky=tk.W)

        self.price_label = ttk.Label(main_frame, font=('FontAwesome', 9, "italic"), text=myVars.i18n.price_label)
        self.price_label.grid(column=0, row=8, padx=5, pady=5, columnspan=5)

        self.options_window.bind("<Escape>", lambda e: self.homepage_handler())
        self.options_window.bind("<Return>", lambda e: self.complete_handler())
        self.options_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.options_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win6:
    def __init__(self):
        self.thanks_window = tk.Tk()
        self.thanks_window.title(myVars.i18n.thanks)
        self.thanks_window.geometry("385x350+710+290")
        self.thanks_window.iconbitmap("hotel.ico")
        self.thanks_window.resizable(False, False)
        self.create_widgets()

    def return_homepage(self):
        self.thanks_window.destroy()
        w4 = Win4()
        w4.homepage_window.focus_force()

    def return_welcome_page(self):
        self.thanks_window.destroy()
        w1 = Win1()
        w1.welcome_win.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.thanks_window.title(myVars.i18n.thanks)
        self.successful_label.configure(text=myVars.i18n.successful)
        self.information_label.configure(text=myVars.i18n.informations)
        self.resNo_label.configure(text=myVars.i18n.reservationid)
        self.exit_button.configure(text=myVars.i18n.signout)
        self.return_homepage_button.configure(text=myVars.i18n.return_homepage)

    def create_widgets(self):
        main_frame = tk.LabelFrame(self.thanks_window)
        main_frame.pack(expand=True)

        self.successful_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.successful)
        self.successful_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.information_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.informations)
        self.information_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.scr_text = scrolledtext.ScrolledText(main_frame, font=('OpenSans', 11), width=40, height=10, wrap=tk.WORD, state="normal")
        self.scr_text.grid(column=0, row=3, padx=5, pady=5)

        self.resNo_label = tk.Label(main_frame, font=('OpenSans', 11, "bold"), text=myVars.i18n.reservationid)
        self.resNo_label.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)

        self.empty_label = tk.Label(main_frame, text="")
        self.empty_label.grid(column=0, row=4)

        self.exit_button = tk.Button(main_frame, text=myVars.i18n.signout, font=('FontAwesome', 10, "bold"), foreground="black",
                                     command=self.return_welcome_page)
        self.exit_button.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)

        self.return_homepage_button = tk.Button(main_frame, text=myVars.i18n.return_homepage, foreground="black",
                                                font=('FontAwesome', 10, "bold"),
                                                command=self.return_homepage)
        self.return_homepage_button.grid(column=0, row=5, padx=5, pady=5, sticky=tk.E)

        self.thanks_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.thanks_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


class Win7:

    def __init__(self):
        self.history_window = tk.Tk()
        self.history_window.title(myVars.i18n.history)
        self.history_window.geometry("1430x330+350+290")
        self.history_window.iconbitmap("hotel.ico")
        self.create_widgets()
        self.show_history()
        self.history_window.resizable(False, False)

    def show_history(self):
        conn = sqlite3.connect("hotel.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM tblReservation WHERE username=:username",
                    {"username": myVars.getUsername()})

        for i in self.tv.get_children():
            self.tv.delete(i)

        rows = cur.fetchall()
        for g in rows:
            self.tv.insert(parent="", index="end", iid=g[0], values=(g[0], g[1], g[2], g[3], g[4], g[5], g[6],
                                                                     g[7], g[8], g[9], g[10], g[11], g[12]))
        conn.close()

    def delete_reservation(self, resid):
        message = msg.askyesno(title=myVars.i18n.delete_reservation, message=myVars.i18n.are_you_sure)
        if message:
            try:
                conn = sqlite3.connect("hotel.db")
                cur = conn.cursor()
                cur.execute(f"DELETE FROM tblReservation WHERE reservationID={resid}")
                conn.commit()
                conn.close()
            except Exception as exc:
                msg.showerror("Error", "Error: " + str(exc))
        self.show_history()

    def return_homepage(self):
        self.history_window.destroy()
        w4 = Win4()
        w4.homepage_window.focus_force()

    def reload_gui_text(self, language):
        myVars.i18n = I18N(language)
        self.tv.heading(0, text=myVars.i18n.reservationid_heading)
        self.tv.heading(1, text=myVars.i18n.username_heading)
        self.tv.heading(2, text=myVars.i18n.country_heading)
        self.tv.heading(3, text=myVars.i18n.city_heading)
        self.tv.heading(4, text=myVars.i18n.numberofpeople_heading)
        self.tv.heading(5, text=myVars.i18n.numberofroom_heading)
        self.tv.heading(6, text=myVars.i18n.view_heading)
        self.tv.heading(7, text=myVars.i18n.breakfast_heading)
        self.tv.heading(8, text=myVars.i18n.ac_heading)
        self.tv.heading(9, text=myVars.i18n.rs_heading)
        self.tv.heading(10, text=myVars.i18n.reservationdate_heading)
        self.tv.heading(11, text=myVars.i18n.start_day_heading)
        self.tv.heading(12, text=myVars.i18n.finish_day_heading)
        self.history_window.title(myVars.i18n.history)
        self.back_button.configure(text=myVars.i18n.return_homepage)
        self.delete.configure(text=myVars.i18n.delete)

    def delete_selected(self):
        selected_items = self.tv.selection()
        values = self.tv.item(selected_items)['values']
        rid = values[0]
        self.delete_reservation(rid)

    def create_widgets(self):
        self.container = tk.Frame(self.history_window)
        self.container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tv_frame = tk.Frame(self.container)
        self.tv_frame.pack()

        self.scr_bar = ttk.Scrollbar(self.tv_frame)
        self.scr_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tv = ttk.Treeview(self.tv_frame, yscrollcommand=self.scr_bar.set)
        self.tv.pack()

        self.scr_bar.configure(command=self.tv.yview)

        s = ttk.Style()
        s.configure("Treeview.Heading", font=('OpenSans', 9, "bold"))

        self.tv["columns"] = ("reservationID", "username", "country", "city", "numberOfPeople", "numberOfRoom", "view",
                              "breakfast", "ac", "rs", "reservationDate", "visitStartDate", "visitFinishDate")

        self.tv.column("#0", width=0, stretch=tk.NO)
        self.tv.column("reservationID", anchor=tk.CENTER, width=150)
        self.tv.column("username", anchor=tk.W, width=100)
        self.tv.column("country", anchor=tk.W, width=100)
        self.tv.column("city", anchor=tk.W, width=100)
        self.tv.column("numberOfPeople", anchor=tk.CENTER, width=110)
        self.tv.column("numberOfRoom", anchor=tk.CENTER, width=110)
        self.tv.column("view", anchor=tk.W, width=100)
        self.tv.column("breakfast", anchor=tk.W, width=100)
        self.tv.column("ac", anchor=tk.W, width=100)
        self.tv.column("rs", anchor=tk.W, width=100)
        self.tv.column("reservationDate", anchor=tk.CENTER, width=120)
        self.tv.column("visitStartDate", anchor=tk.CENTER, width=100)
        self.tv.column("visitFinishDate", anchor=tk.CENTER, width=100)

        self.tv.heading("#0", text="")
        self.tv.heading("reservationID", text=myVars.i18n.reservationid_heading, anchor=tk.CENTER)
        self.tv.heading("username", text=myVars.i18n.username_heading, anchor=tk.W)
        self.tv.heading("country", text=myVars.i18n.country_heading, anchor=tk.W)
        self.tv.heading("city", text=myVars.i18n.city_heading, anchor=tk.W)
        self.tv.heading("numberOfPeople", text=myVars.i18n.numberofpeople_heading, anchor=tk.CENTER)
        self.tv.heading("numberOfRoom", text=myVars.i18n.numberofroom_heading, anchor=tk.CENTER)
        self.tv.heading("view", text=myVars.i18n.view_heading, anchor=tk.W)
        self.tv.heading("breakfast", text=myVars.i18n.breakfast_heading, anchor=tk.W)
        self.tv.heading("ac", text=myVars.i18n.ac_heading, anchor=tk.W)
        self.tv.heading("rs", text=myVars.i18n.rs_heading, anchor=tk.W)
        self.tv.heading("reservationDate", text=myVars.i18n.reservationdate_heading, anchor=tk.CENTER)
        self.tv.heading("visitStartDate", text=myVars.i18n.start_day_heading, anchor=tk.CENTER)
        self.tv.heading("visitFinishDate", text=myVars.i18n.finish_day_heading, anchor=tk.CENTER)

        self.delete = ttk.Label(self.history_window, font=('FontAwesome', 9, "italic"), text=myVars.i18n.delete)
        self.delete.pack(pady=7, anchor=tk.SW)

        s.configure('my.TButton', foreground="black", background="black", font=('FontAwesome', 10, "bold"))

        self.back_button = ttk.Button(self.history_window, style='my.TButton', text=myVars.i18n.return_homepage,
                                      command=self.return_homepage)
        self.back_button.pack(pady=7, anchor=tk.CENTER)

        self.history_window.bind("<Escape>", lambda e: self.return_homepage())
        self.tv.bind("<Delete>", lambda e: self.delete_selected())
        self.history_window.bind("<F1>", lambda e: self.reload_gui_text("en"))
        self.history_window.bind("<F2>", lambda e: self.reload_gui_text("tr"))


if not os.path.exists("hotel.db"):
    print("We need to create DB")
    database.create_database()
    print("DB created")
else:
    print("Check DB if there is missing table")
    database.create_missing_table()
    print("DB is updated")

app = Win1()
app.welcome_win.mainloop()
