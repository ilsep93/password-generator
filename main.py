import json
import os
import random
import string
import tkinter as tk
from json import JSONDecodeError
from tkinter import messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project

letters = list(string.ascii_lowercase + string.ascii_uppercase)
numbers = list(range(0, 10))
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
        '''
        Generates a random password by combining letters, numbers, and symbols.
        '''
        letter_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
        symbol_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]
        num_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]
        
        password_list = letter_list + symbol_list + num_list
        random.shuffle(password_list)

        password = "".join(letter_list)
        password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def overwrite_password():
        """Returns True if user wishes to overwrite password.
        Returns false if password should be not be overwritten from data file.
        If previous password is not found, returns None.

        Returns:
            
        """
        website = website_entry.get()
        try:
                with open("data.json", "r") as data_file:
                        data = json.load(data_file)
                        if website in data and data is not None:
                                return messagebox.askyesno(title="Password exists", message=f"Password for {website} already exists. Overwrite?")
        except JSONDecodeError:
                pass
        except FileNotFoundError:
                pass
                


def export_password():
        '''
        1. Ensures entry is not empty of website or password
        2. Formats entry as dictionary
        3. Checks to see user needs to overwrite password
        4. Updates file with new entry and creates one if none exists.
        '''
        
        website = website_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if len(website)==0 or len(password)==0:
                messagebox.showinfo(title="Invalid", message="Please do not leave fields empty!")      

        else:
                new_entry = {
                website: {
                "email": email,
                "password": password,
                },
                }

                overwrite = overwrite_password()
                try:
                        with open("data.json", "r") as data_file:
                                data = json.load(data_file)
                                if overwrite is True:
                                        data[f"{website}"] = new_entry
                                if overwrite is False:
                                        website_entry.delete(0,'end')
                                        password_entry.delete(0, 'end')
                                if overwrite is None:
                                        data.update(new_entry)
                except FileNotFoundError:
                                with open("data.json", "w") as data_file:
                                        json.dump(new_entry, data_file, indent=4)
                except JSONDecodeError:
                        os.remove("data.json")
                        with open("data.json", "w") as data_file:
                                json.dump(new_entry, data_file, indent=4)

                else:
                        if overwrite is True or overwrite is None:
                                with open("data.json", "w") as data_file:
                                        json.dump(data, data_file, indent=4)

 
# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
        '''
        Searches for existing passwords in data file and returns
        value in message box.
        '''
        #Gather inputs from website field
        website = website_entry.get()
        #Open existing data file
        try:
                with open("data.json") as data_file:
                        data = json.load(data_file)
                        result = data[website]
        except FileNotFoundError as no_file:
                messagebox.showinfo(title="No Info", message="There are no saved passwords to search.")        
        except KeyError:
                messagebox.showinfo(title="No Info", message="No results found")
        else:
                messagebox.showinfo(title="Your Info", message=f"Email: {result['email']} Password: {result['password']}"                         )
        
               
#  ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white")

# Image: row=1, column=2

pass_img = tk.PhotoImage(file="logo.png")
canvas = tk.Canvas(
        width=200,
        height=200,
        bg="white",
        highlightthickness=0
        )
lock = canvas.create_image(100, 100,image=pass_img)
canvas.grid(row=0, column=1)

# Text 
website_text = tk.Label(
        text="Website:",
        fg = "black",
        bg="white",
        highlightthickness=0)
website_text.grid(row=2, column=0)

email_text = tk.Label(
        text="Email/Username:",
        fg = "black",
        bg="white",
        highlightthickness=0
        )
email_text.grid(row=3, column=0)

password_text = tk.Label(
        text="Password:",
        fg = "black",
        bg="white",
        highlightthickness=0
        )
password_text.grid(row=4, column=0)

# Entry
website_entry = tk.Entry(
        width=35,
        fg = "black",
        bg="white",
        highlightthickness=0)
website_entry.focus()
website_entry.grid(row=2, column=1)

email_entry = tk.Entry(
        width=35,
        fg = "black",
        bg="white",
        highlightthickness=0
        )
email_entry.insert(0, "ilsep@umich.edu")
email_entry.grid(row=3, column=1, columnspan=2, sticky="EW")


password_entry = tk.Entry(
        width=21,
        fg = "black",
        bg="white",
        highlightbackground="white",
        show="*"
        )
password_entry.grid(row=4, column=1, sticky="EW")

# Buttons
password_button = tk.Button(
        text="Generate Password",
        fg = "black",
        bg="white",
        highlightbackground="white",
        command=generate_password
        )
password_button.grid(row=4, column=2)

add_button = tk.Button(
        text="Add",
        width=36,
        fg = "black",
        bg="white",
        highlightbackground="white",
        command=export_password
        )
add_button.grid(row=5, column=1, columnspan=2)

search_button = tk.Button(
        text="Search",
        fg = "black",
        bg="white",
        highlightbackground="white",
        width=15,
        command=search_password
        )
search_button.grid(row=2, column=2)

window.mainloop()