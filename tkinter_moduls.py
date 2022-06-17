from tkinter import *
from PIL import ImageTk
from PIL import Image
import sqlite3
from tkinter import messagebox




class Start:
    def __init__(self):
        self.root = Tk()
        sing_up_button = Button(self.root, text = 'Sing Up', command = self.open_sing_up)
        sing_up_button.grid(row = 0, column = 0)
        sing_in_button = Button(self.root, text = 'Sing In', command = self.open_sing_in)
        sing_in_button.grid(row = 0, column = 1)

        self.root.mainloop()
    
    
    def open_sing_up(self):
        self.root.destroy()
        self.choose = 'sing_up'

    def open_sing_in(self):
        self.root.destroy()
        self.choose = 'sing_ip'


class Sing_In:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('500x500')

        heading = Label(self.root, text = 'Welcome To The App', bg = 'grey', fg = 'black', width = 500, height = 2, font = ('poppins', 18))
        heading.pack()
        
        username_label = Label(self.root, text = 'First name')
        password_label = Label(self.root, text = 'Password')
        username_label.place(x = 15, y = 70)
        password_label.place(x = 15, y = 140)


        self.username_entry = Entry(self.root, width = 30)
        self.password_entry = Entry(self.root, width = 30)
        self.username_entry.place(x = 15, y = 100)
        self.password_entry.place(x = 15, y = 170)


        finish = Button(self.root, text = 'Submit', width = '30', height = "2", command = self.Submit, bg = 'grey')
        finish.place(x = 0, y = 250)


        self.root.mainloop()


    def Submit(self):
        self.username, self.password = self.get_data()
        self.root.destroy()

    def get_data(self):
        username_data = self.username_entry.get()
        password_data = self.password_entry.get()
        return (username_data, password_data)

    # def send_data(self, client, username, password):
    #     message  = f'[SINGUP]/{username}/{password}'
    #     client.send(message.encode())

    # def get_result(self, client):
    #     code = client.recv(1024).decode()
    #     return code

        

class Sing_Up:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('500x500')

        heading = Label(self.root, text = 'Welcome To The App', bg = 'grey', fg = 'black', width = 500, height = 2, font = ('poppins', 18))
        heading.pack()
        
        username_label = Label(self.root, text = 'First name')
        password_label = Label(self.root, text = 'Password')
        username_label.place(x = 15, y = 70)
        password_label.place(x = 15, y = 140)
        validate_password_label = Label(self.root, text = 'Validate Password')
        validate_password_label.place(x = 15, y = 210)

        self.username_entry = Entry(self.root, width = 30)
        self.password_entry = Entry(self.root, width = 30)
        self.validate_password_entry = Entry(self.root, width = 30)
        self.username_entry.place(x = 15, y = 100)
        self.password_entry.place(x = 15, y = 170)
        self.validate_password_entry.place(x = 15, y = 240)



        finish = Button(self.root, text = 'Submit', width = '30', height = "2", command = self.Submit, bg = 'grey')
        finish.place(x = 0, y = 300)

        self.root.mainloop()

    def Submit(self):
        self.username, self.password, validate_password = self.get_data()
        if self.password != validate_password:
            respons = messagebox.showerror('Error', "The passwords Don't match")
        elif self.password == self.username:
            respons = messagebox.showerror('Error', "The password can't be same as the username")
        elif len(self.password) < 8:
            respons = messagebox.showerror('Error', "The Password is too short, it needs tobe at least8 characters")
        else:
            self.root.destroy()           

    def get_data(self):
        username_data = self.username_entry.get()
        password_data = self.password_entry.get()
        validate_password_data = self.validate_password_entry.get()
        return (username_data, password_data, validate_password_data)

    # def send_data(self, client, username, password):
    #     message  = f'[SINGUP]/{username}/{password}'
    #     client.send(message.encode())

    # def get_result(self, client):
    #     code = client.recv(1024).decode()
    #     return code




        





# def Submit():
#     username_info = username_entry.get()
#     password_info = password_entry.get()
#     connect = sqlite3.connect('form.db')

#     c = connect.cursor()

#     # c.execute('''CREATE TABLE users (
#     #     username text,
#     #     password text
#     # )''')


#     c.execute("INSERT INTO users VALUES (:username, :password)",
#         {
#             'username': username_info,
#             'password': password_info,
#         })

#     c.execute("SELECT *, oid FROM users")
#     information = c.fetchall()

#     print_records = ''
#     for record in information:
#        print(record)



#     connect.commit()
#     connect.close()
