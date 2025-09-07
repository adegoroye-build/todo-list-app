import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# File path in user home directory
file_path = os.path.join(os.path.expanduser("~"), "tasks.json")

# Save tasks to file
def save_tasks():
    tasks = []
    for i in range(task_listbox.size()):
        task_text = task_listbox.get(i)
        tasks.append(task_text)
    with open(file_path, "w") as f:
        json.dump(tasks, f)

# Load tasks from file
def load_tasks():
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            tasks = json.load(f)
            for task in tasks:
                task_listbox.insert(tk.END, task)

# Add task
def add_task(event=None):
    task = task_entry.get().strip()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task!")

# Delete task with confirmation
def delete_task(event=None):
    try:
        selected = task_listbox.curselection()[0]
        task_text = task_listbox.get(selected)
        confirm = messagebox.askyesno("Confirm Delete", f"Delete task: {task_text}?")
        if confirm:
            task_listbox.delete(selected)
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

# Edit task
def edit_task():
    try:
        selected = task_listbox.curselection()[0]
        new_task = task_entry.get().strip()
        if new_task:
            task_listbox.delete(selected)
            task_listbox.insert(selected, new_task)
            task_entry.delete(0, tk.END)
            save_tasks()
        else:
            messagebox.showwarning("Warning", "Enter new text to edit!")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to edit!")

# Mark task as done / undone
def mark_done():
    try:
        selected = task_listbox.curselection()[0]
        task_text = task_listbox.get(selected)
        if not task_text.startswith("[Done] "):
            task_listbox.delete(selected)
            task_listbox.insert(selected, "[Done] " + task_text)
        else:
            task_listbox.delete(selected)
            task_listbox.insert(selected, task_text.replace("[Done] ", "", 1))
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark as done!")

# Main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("500x500")
root.resizable(False, False)

# Modern theme
style = ttk.Style(root)
style.theme_use("clam")

# Input field
task_entry = ttk.Entry(root, width=40)
task_entry.pack(pady=10)

# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

add_button = ttk.Button(button_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=0, padx=5)

edit_button = ttk.Button(button_frame, text="Edit Task", command=edit_task)
edit_button.grid(row=0, column=1, padx=5)

done_button = ttk.Button(button_frame, text="Mark Done", command=mark_done)
done_button.grid(row=0, column=2, padx=5)

delete_button = ttk.Button(button_frame, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=3, padx=5)

# Task list with scrollbar
frame = ttk.Frame(root)
frame.pack(pady=10)

scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox = tk.Listbox(
    frame,
    width=60,
    height=15,
    yscrollcommand=scrollbar.set,
    font=("Arial", 12)
)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=task_listbox.yview)

# Load saved tasks
load_tasks()

# Keyboard shortcuts
root.bind("<Return>", add_task)      # Press Enter to add task
root.bind("<Delete>", delete_task)   # Press Delete key to remove task

# Run app
root.mainloop()
