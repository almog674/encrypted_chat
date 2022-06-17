from tkinter import *

form = Tk()
form.title('Test')
form.geometry('400x400')


def open_sing_up():
    sing_up_window = Tk()
    sing_up_window.title('Sing Up')
    sing_up_window.geometry('400x400')

    title_label = Label(sing_up_window, text = 'Welcome To The APP', font = ('poppins', 18)).grid(row = 0, column = 0, columnspan = 2, pady = 25, sticky = E)

    first_name_lable = Label(sing_up_window, text = 'First Name:').grid(row = 1, column = 0)
    first_name_entry = Entry(sing_up_window).grid(row = 1, column = 1, pady = 10)

    last_name_lable = Label(sing_up_window, text = 'Last Name:').grid(row = 2, column = 0)
    last_name_entry = Entry(sing_up_window).grid(row = 2, column = 1)

    submit_button = Button(button_section, text = 'Join For Free!')
    submit_button.grid(row = 0, column = 0, padx = 10, ipadx = 10, ipady = 5)

main_page = Frame(form, width = '600', height = '400')
title_label = Label(main_page, text = 'Welcome To The APP', font = ('poppins', 18)).grid(row = 0, column = 0, columnspan = 2, pady = 25)
button_section = Frame(main_page, width = '200', height = '100', bd = 1)
button_section.grid(row = 1, column = 0, pady = 200)

sing_up_btn = Button(button_section, text = 'Join For Free!')
sing_up_btn.grid(row = 0, column = 0, padx = 10, ipadx = 10, ipady = 5)
sing_in_btn = Button(button_section, text = 'Sing Up!', command = open_sing_up)
sing_in_btn.grid(row = 0, column = 1, padx = 10, ipadx = 10, ipady = 5)

sing_in_section = Frame(main_page, width = '300', height = 200)


main_page.pack()


form.mainloop()