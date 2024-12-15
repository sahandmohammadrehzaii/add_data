# in the name of god

import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime

# Connect to the database
def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Create a table in the database
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ghadaamghadaamquestion (
            id INTEGER PRIMARY KEY,
            ghadaamquestion TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()

# Add ghadaamquestion and answers to the database
def add_ghadaamghadaamquestion(conn, ghadaamquestion, answer):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ghadaamghadaamquestion (ghadaamquestion, answer) VALUES (?, ?)', (ghadaamquestion, answer))
    conn.commit()

# Function to add ghadaamquestion and answers
def submit():
    ghadaamquestion = ghadaamquestion_entry.get()
    answer = answer_entry.get()

    if ghadaamquestion and answer:
        add_ghadaamghadaamquestion(conn, ghadaamquestion, answer)
        add_message_to_mat_db(ghadaamquestion, answer)
        messagebox.showinfo("Success", "ghadaamquestion and answer added successfully.")
        ghadaamquestion_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please fill in both fields.")

# Function to add message to saveddatainfo.db database
def add_message_to_mat_db(ghadaamquestion, answer):
    mat_conn = connect_db('../database/operations/savedatainfo.db')
    cursor = mat_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            ghadaamquestion TEXT NOT NULL,
            answer TEXT NOT NULL,
            datetime TEXT NOT NULL
        )
    ''')
    mat_conn.commit()
    cursor.execute('INSERT INTO messages (ghadaamquestion, answer, datetime) VALUES (?, ?, ?)',
                   (ghadaamquestion, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mat_conn.commit()
    mat_conn.close()

# Function to delete ghadaamquestion and answers
def delete_ghadaamghadaamquestion():
    delete_text = delete_entry.get()
    if delete_text:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ghadaamghadaamquestion WHERE ghadaamquestion=? OR answer=?', (delete_text, delete_text))
        conn.commit()
        messagebox.showinfo("Success", "ghadaamquestion and answer successfully deleted.")
        delete_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please fill in the deletion field.")

# تابع برای ویرایش سوال و پاسخ
def edit_ghadaamghadaamquestion():
    edit_text = edit_entry.get()
    new_ghadaamquestion = new_ghadaamquestion_entry.get()
    new_answer = new_answer_entry.get()
    if edit_text and new_ghadaamquestion and new_answer:
        cursor = conn.cursor()
        cursor.execute('UPDATE ghadaamghadaamquestion SET ghadaamquestion = ?, answer = ? WHERE ghadaamquestion = ? OR answer = ?', (new_ghadaamquestion, new_answer, edit_text, edit_text))
        conn.commit()
        messagebox.showinfo("Success", "ghadaamquestion and answer edited successfully.")
        edit_entry.delete(0, tk.END)
        new_ghadaamquestion_entry.delete(0, tk.END)
        new_answer_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

# Function to display information
def show_info():
    info_window = tk.Toplevel(window)
    info_window.title("Display Information")
    info_label = tk.Label(info_window, text="Enter ghadaamquestion:")
    info_label.pack(padx=10, pady=5)
    info_entry = tk.Entry(info_window, width=50)
    info_entry.pack(padx=10, pady=5)
    info_text = scrolledtext.ScrolledText(info_window, width=50, height=10)
    info_text.pack(padx=10, pady=5)
    def search_info():
        ghadaamquestion = info_entry.get()
        if ghadaamquestion:
            cursor = conn.cursor()
            cursor.execute('SELECT id, ghadaamquestion, answer FROM ghadaamghadaamquestion WHERE ghadaamquestion=?', (ghadaamquestion,))
            result = cursor.fetchone()
            if result:
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, f"ID number: {result[0]}\n ghadaamquestion: {result[1]}\n answer: {result[2]}")
            else:
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, "ghadaamquestion not found.")
        else:
            messagebox.showwarning("Error", "Please fill in the field.")
    search_button = tk.Button(info_window, text="Search", command=search_info)
    search_button.pack(pady=10)

# Initial settings
db_name = '../database/question/question.db'
conn = connect_db(db_name)
create_table(conn)

# Create Tkinter window
window = tk.Tk()
window.title("Add ghadaamquestion and answers")
window.iconphoto(False, tk.PhotoImage(file='../assets/icon.png'))  # add icon to the window  


# ghadaamquestion input field
ghadaamquestion_label = tk.Label(window, text="ghadaamquestion:")
ghadaamquestion_label.pack(padx=10, pady=5)
ghadaamquestion_entry = tk.Entry(window, width=50)
ghadaamquestion_entry.pack(padx=10, pady=5)

# Response input field
answer_label = tk.Label(window, text="answer:")
answer_label.pack(padx=10, pady=5)
answer_entry = tk.Entry(window, width=50)
answer_entry.pack(padx=10, pady=5)

# Add button
add_button = tk.Button(window, text="add", command=submit)
add_button.pack(pady=10)

# Input field to delete ghadaamquestion or answer
delete_label = tk.Label(window, text="Delete ghadaamquestion or answer:")
delete_label.pack(padx=10, pady=5)
delete_entry = tk.Entry(window, width=50)
delete_entry.pack(padx=10, pady=5)

# Delete button
delete_button = tk.Button(window, text="delete", command=delete_ghadaamghadaamquestion)
delete_button.pack(pady=10)

# Input field to edit the ghadaamquestion or answer
edit_label = tk.Label(window, text="Edit ghadaamquestion or answer:")
edit_label.pack(padx=10, pady=5)
edit_entry = tk.Entry(window, width=50)
edit_entry.pack(padx=10, pady=5)

# Input field for new ghadaamquestion
new_ghadaamquestion_label = tk.Label(window, text="New ghadaamquestion:")
new_ghadaamquestion_label.pack(padx=10, pady=5)
new_ghadaamquestion_entry = tk.Entry(window, width=50)
new_ghadaamquestion_entry.pack(padx=10, pady=5)

# Input field for new response
new_answer_label = tk.Label(window, text="New answer:")
new_answer_label.pack(padx=10, pady=5)
new_answer_entry = tk.Entry(window, width=50)
new_answer_entry.pack(padx=10, pady=5)

# Edit button
edit_button = tk.Button(window, text="Edit", command=edit_ghadaamghadaamquestion)
edit_button.pack(pady=10)

# Information display button
info_button = tk.Button(window, text="display information", command=show_info)
info_button.pack(pady=10)

# Help button
def show_guide():
    guide_window = tk.Toplevel(window)
    guide_window.title("guide")
    guide_label = tk.Label(guide_window, text="Greetings, don't get tired of the data storage and support team. This part of the project belongs to data storage and their management.")
    guide_label.pack(padx=10, pady=10)

guide_button = tk.Button(window, text="guide", command=show_guide)
guide_button.pack(pady=10, side=tk.RIGHT)

# Run the main loop
window.mainloop()

conn.close()
