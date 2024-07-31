from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_letters + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    entry_password.delete(0,END)
    entry_password.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website:{
            "email":email,
            "password":password,
        }
    }

    if len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: "
                                                              f"\nEmail:{email} "
                                                              f"\nPassword:{password} \n Is it ok to save?")
    if is_ok:
        try:
            with open(file="data.json", mode = 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
                data.update(new_data)

                with open(file="data.json", mode='w') as data_file:
                    json.dump(data,data_file, indent=4)
        finally:
            entry_website.delete(0,END)
            entry_password.delete(0,END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = entry_website.get()
    try:
        with open(file="data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}\n")
        else:
            messagebox.showinfo(title="Error", message=f"No details exist for {website}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.minsize(width = 200, height = 200)
window.title("Password Manager")
window.config(padx = 20 , pady = 20)

logo = PhotoImage(file = "logo.png")
canvas = Canvas(width=200,height = 200)
canvas.create_image(100,100, image = logo)
canvas.grid(column = 1, row = 0)

#LABELS
label_text = Label(text = "Website:", font=("Arial",10))
label_text.grid(column = 0, row = 1)

label_email = Label(text = "Email/Username:", font=("Arial",10))
label_email.grid(column = 0, row = 2)

label_password = Label(text = "Password:", font=("Arial",10))
label_password.grid(column = 0, row = 3)

#ENTRY
entry_website = Entry(width=35)
entry_website.grid(column = 1, row = 1)
entry_website.focus()

entry_email = Entry(width=35)
entry_email.grid(column = 1, row = 2, columnspan = 2, sticky = "EW")
entry_email.insert(0, "email@gmail.com")

entry_password = Entry(width=35)
entry_password.grid(column = 1, row = 3)

#BUTTONS
generate_pass = Button(text="Generate Password", command=generate_password,width=15)
generate_pass.grid(column = 2, row = 3)

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column = 1, row = 4, columnspan = 2, sticky = "EW")

search_button = Button(text="Search", command=find_password, width=15)
search_button.grid(column = 2, row = 1)

window.mainloop()