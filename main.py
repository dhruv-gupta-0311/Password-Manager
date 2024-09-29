from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project

def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(f"{password}")

    pass_entry.insert(0, password)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_pass():
    website = web_entry.get()
    try:
        with open("data.json") as datafile:
            data = json.load(datafile)
    except FileNotFoundError:
        messagebox.showerror(title="error", message="No datafile found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="error", message=f"No data for {website} found")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_data = web_entry.get()
    email_data = email_entry.get()
    password_data = pass_entry.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": password_data
        }
    }
    is_ok = bool
    if len(website_data) == 0 or len(email_data) == 0 or len(password_data) == 0:
        is_ok = False
        error = messagebox.showerror(title="Error", message="Necessary to fill all fields")

    if is_ok:
        is_ok = messagebox.askokcancel(title=website_data, message=f"These are details entered:\n Email:{email_data}\n"
                                                                   f"Password:{password_data}\nIs it ok to save?")

        try:
            with open("data.json", "r") as datafile:
                #reading old data
                data = json.load(datafile)

        except FileNotFoundError:
            with open("data.json", "w") as datafile:
                json.dump(new_data, datafile, indent=4)
                # updating with newdata
        else:
            data.update(new_data)

            with open("data.json", "w") as datafile:
                #writing updated data
                json.dump(data, datafile, indent=4)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)
#canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
#Labels
web_label = Label(text="Website:")
web_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
#entries input
web_entry = Entry(width=18)
web_entry.focus()
web_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
pass_entry = Entry(width=18)
pass_entry.grid(row=3, column=1, sticky="EW")
#buttons
pass_gen = Button(text="Generate Password", width=10, padx=20, command=password_gen)
pass_gen.grid(row=3, column=2, sticky="EW")
add = Button(text="Add", width=36, command=save)
add.grid(row=4, column=1, columnspan=2, sticky="EW")
search_data = Button(text="Search", width=10, padx=20, command=find_pass)
search_data.grid(row=1, column=2, sticky="EW")
window.mainloop()
