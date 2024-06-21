import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import json
import os

class Task:
    def __init__(self, description, priority='low', due_date=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(data):
        task = Task(data['description'], data['priority'], data['due_date'])
        task.completed = data['completed']
        return task

class ToDoList:
    def __init__(self, file_path='tasks.json'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task) for task in tasks_data]
        return []

    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, description, priority='low', due_date=None):
        task = Task(description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_as_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_as_completed()
            self.save_tasks()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x400")
        self.todo_list = ToDoList()
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.task_description = tk.StringVar()
        self.task_priority = tk.StringVar(value='low')
        self.task_due_date = tk.StringVar()

        ttk.Label(self.frame, text="Task Description:").grid(column=1, row=1, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.task_description, width=50).grid(column=2, row=1, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(self.frame, text="Priority:").grid(column=1, row=2, sticky=tk.W)
        ttk.Combobox(self.frame, textvariable=self.task_priority, values=['high', 'medium', 'low']).grid(column=2, row=2, sticky=tk.W)

        ttk.Label(self.frame, text="Due Date (YYYY-MM-DD):").grid(column=1, row=3, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.task_due_date).grid(column=2, row=3, sticky=tk.W)

        ttk.Button(self.frame, text="Add Task", command=self.add_task).grid(column=3, row=2, rowspan=2, sticky=(tk.W, tk.E))

        self.task_listbox = tk.Listbox(self.frame, height=10, width=70)
        self.task_listbox.grid(column=1, row=4, columnspan=3, sticky=(tk.W, tk.E))

        ttk.Button(self.frame, text="Mark as Completed", command=self.mark_task_as_completed).grid(column=1, row=5, sticky=tk.W)
        ttk.Button(self.frame, text="Remove Task", command=self.remove_task).grid(column=3, row=5, sticky=tk.E)

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.todo_list.tasks):
            status = "Completed" if task.completed else "Pending"
            due_date = task.due_date if task.due_date else "No due date"
            self.task_listbox.insert(tk.END, f"{index}: {task.description} [{task.priority}] - {due_date} - {status}")

    def add_task(self):
        description = self.task_description.get()
        priority = self.task_priority.get()
        due_date = self.task_due_date.get()
        if description:
            self.todo_list.add_task(description, priority, due_date)
            self.refresh_task_list()
            self.task_description.set("")
            self.task_priority.set("low")
            self.task_due_date.set("")
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")

    def mark_task_as_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.todo_list.mark_task_as_completed(index)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "No task selected.")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.todo_list.remove_task(index)
            self.refresh_task_list()
        else:
            messagebox.showwarning("Selection Error", "No task selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
