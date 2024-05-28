import tkinter as tk
from tkinter import messagebox
from tkinter import *
import sqlite3
import re

def connect():
    conn = sqlite3.connect("Contact_book.db")
    return conn

def create_table():
    conn = connect()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS 
              contact_book(id INTEGER PRIMARY KEY, Name TEXT,Phone_number TEXT, Email TEXT, Address TEXT)''')
    conn.commit()
    conn.close()
    
create_table()

def add_contact(Name, Phone_number, Email, Address):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO contact_book(Name, Phone_number, Email, Address) VALUES(?,?,?,?)",(Name, Phone_number, Email, Address))
    conn.commit()
    conn.close()

def view():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM contact_book")
    contacts = c.fetchall()
    conn.close()
    return contacts

def search(query):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM contact_book WHERE Name LIKE ? OR Phone_number LIKE ?", (f'%{query}%',f'%{query}%'))
    contacts = c.fetchall()
    conn.close()
    return contacts

def update(id, Name, Phone_number, Email, Address):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE contact_book SET Name = ?, Phone_number = ?, Email = ?, Address = ? WHERE id = ?", (Name, Phone_number, Email, Address, id))
    conn.commit()
    conn.close()
    
def delete(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM contact_book WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def is_valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def show_add_screen():
    clear_screen()
    global name_entry, phone_entry, email_entry, address_entry
    add_frame = tk.Frame(root)
    add_frame.pack(pady=20)

    tk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(add_frame, text="Phone Number:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(add_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(add_frame, text="Address:").grid(row=3, column=0, padx=10, pady=5)

    name_entry = tk.Entry(add_frame)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    phone_entry = tk.Entry(add_frame)
    phone_entry.grid(row=1, column=1, padx=10, pady=5)
    email_entry = tk.Entry(add_frame)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    address_entry = tk.Entry(add_frame)
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    save_button = tk.Button(add_frame, text="Save", command=save_contact)
    save_button.grid(row=4, column=1, pady=10)
    
    back_button = tk.Button(add_frame, text="Back", command=show_main_screen)
    back_button.grid(row=4, column=0, pady=10)

def save_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    if not name or not phone or not email or not address:
        messagebox.showerror("Error", "All fields are required")
    elif not is_valid_phone(phone):
        messagebox.showerror("Error", "Phone number must be 10 digits")
    elif not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
    else:
        add_contact(name, phone, email, address)
        messagebox.showinfo("Success", "Contact added successfully")
        clear_screen()
        show_main_screen()

def show_view_screen():
    clear_screen()
    global contacts_listbox
    view_frame = tk.Frame(root)
    view_frame.pack(pady=10)

    contacts = view()
    contacts_listbox = tk.Listbox(view_frame, width=50, height=10)
    contacts_listbox.grid(row=0, column=0, columnspan=2, pady=10)

    for contact in contacts:
        contacts_listbox.insert(tk.END, f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}, Address: {contact[4]}")

    update_button = tk.Button(view_frame, text="Update", command=update_contact)
    update_button.grid(row=1, column=0, pady=2)

    delete_button = tk.Button(view_frame, text="Delete", command=delete_contact)
    delete_button.grid(row=1, column=1, pady=2)
    
    back_button = tk.Button(view_frame, text="Back", command=show_main_screen)
    back_button.grid(row=1, column=2, pady=2)


def update_contact():
    selected_contact = contacts_listbox.get(tk.ANCHOR)
    if selected_contact:
        contact_id = int(selected_contact.split(",")[0].split(":")[1].strip())
        show_update_screen(contact_id)

def show_update_screen(contact_id):
    clear_screen()
    global update_name_entry, update_phone_entry, update_email_entry, update_address_entry
    update_frame = tk.Frame(root)
    update_frame.pack(pady=20)

    contact = search(str(contact_id))[0]

    tk.Label(update_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(update_frame, text="Phone Number:").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(update_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(update_frame, text="Address:").grid(row=3, column=0, padx=10, pady=5)

    update_name_entry = tk.Entry(update_frame)
    update_name_entry.grid(row=0, column=1, padx=10, pady=5)
    update_name_entry.insert(0, contact[1])
    update_phone_entry = tk.Entry(update_frame)
    update_phone_entry.grid(row=1, column=1, padx=10, pady=5)
    update_phone_entry.insert(0, contact[2])
    update_email_entry = tk.Entry(update_frame)
    update_email_entry.grid(row=2, column=1, padx=10, pady=5)
    update_email_entry.insert(0, contact[3])
    update_address_entry = tk.Entry(update_frame)
    update_address_entry.grid(row=3, column=1, padx=10, pady=5)
    update_address_entry.insert(0, contact[4])

    update_save_button = tk.Button(update_frame, text="Save", command=lambda: save_updated_contact(contact_id))
    update_save_button.grid(row=4, column=1, pady=10)
    
    back_button = tk.Button(update_frame, text="Back", command=show_main_screen)
    back_button.grid(row=4, column=0, pady=10)


def save_updated_contact(contact_id):
    name = update_name_entry.get()
    phone = update_phone_entry.get()
    email = update_email_entry.get()
    address = update_address_entry.get()
    if not name or not phone or not email or not address:
        messagebox.showerror("Error", "All fields are required")
    elif not is_valid_phone(phone):
        messagebox.showerror("Error", "Phone number must be 10 digits")
    elif not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
    else:
        update(contact_id, name, phone, email, address)
        messagebox.showinfo("Success", "Contact updated successfully")
        clear_screen()
        show_main_screen()


def delete_contact():
    selected_contact = contacts_listbox.get(tk.ANCHOR)
    if selected_contact:
        contact_id = int(selected_contact.split(",")[0].split(":")[1].strip())
        delete(contact_id)
        messagebox.showinfo("Success", "Contact deleted successfully")
        clear_screen()
        show_main_screen()

def show_search_screen():
    clear_screen()
    global search_entry
    search_frame = tk.Frame(root)
    search_frame.pack(pady=20)

    tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=10, pady=5)

    search_entry = tk.Entry(search_frame)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = tk.Button(search_frame, text="Search", command=search_contact)
    search_button.grid(row=0, column=2, padx=10, pady=5)
    
    back_button = tk.Button(search_frame, text="Back", command=show_main_screen)
    back_button.grid(row=4, column=0, pady=10)
    
def search_contact():
    query = search_entry.get()
    if query:
        results = search(query)
        if results:
            show_search_results(results)
        else:
            messagebox.showinfo("No Results", "No contacts found matching the search query")
    else:
        messagebox.showerror("Error", "Search field cannot be empty")

def show_search_results(results):
    clear_screen()
    results_frame = tk.Frame(root)
    results_frame.pack(pady=20)

    results_listbox = tk.Listbox(results_frame, width=50, height=10)
    results_listbox.grid(row=0, column=0, columnspan=2, pady=10)

    for result in results:
        results_listbox.insert(tk.END, f"ID: {result[0]}, Name: {result[1]}, Phone: {result[2]}, Email: {result[3]}, Address: {result[4]}")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_main_screen():
    clear_screen()
    main_frame = tk.Frame(root)
    main_frame.pack(pady=20)
    
    head_label = tk.Label(main_frame, text="Contacts Manager", font=("Helvetica", 14, "bold"))
    head_label.grid(row=0, column=0, columnspan= 5, pady=15)

    add_button = tk.Button(main_frame, text="Add Contact", command=show_add_screen)
    add_button.grid(row=1, column=0, padx=10)

    view_button = tk.Button(main_frame, text="View Contacts", command=show_view_screen)
    view_button.grid(row=1, column=1, padx=10)

    search_button = tk.Button(main_frame, text="Search Contact", command=show_search_screen)
    search_button.grid(row=1, column=2, padx=10)

root = tk.Tk()
root.title("Contact Book")
root.geometry("400x500")
show_main_screen()
root.mainloop()
