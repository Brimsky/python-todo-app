#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("500x500")
        self.root.minsize(400, 400)
        
        # Set theme colors that work well across platforms
        self.bg_color = "#f5f5f5"
        self.highlight_color = "#4a90e2"
        self.root.configure(bg=self.bg_color)
        
        # Data storage
        self.todo_file = "todos.json"
        self.todos = self.load_todos()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # App title
        title_label = tk.Label(
            main_frame, 
            text="Todo App", 
            font=("Helvetica", 16, "bold"), 
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 10))
        
        # Input frame for new todos
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Todo input
        self.todo_entry = tk.Entry(input_frame, font=("Helvetica", 12))
        self.todo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.todo_entry.bind("<Return>", lambda event: self.add_todo())
        
        # Add button
        add_button = tk.Button(
            input_frame,
            text="Add",
            command=self.add_todo,
            bg=self.highlight_color,
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=10
        )
        add_button.pack(side=tk.RIGHT)
        
        # Todo list frame
        list_frame = tk.Frame(main_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar and Treeview for todo list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Define Treeview style
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#ffffff",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ffffff")
        style.map('Treeview', 
                background=[('selected', self.highlight_color)])
        
        # Create Treeview
        columns = ("Status", "Task", "Actions")
        self.todo_tree = ttk.Treeview(
            list_frame, 
            columns=columns,
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set
        )
        
        # Configure columns
        self.todo_tree.heading("Status", text="Status")
        self.todo_tree.heading("Task", text="Task")
        self.todo_tree.heading("Actions", text="Actions")
        
        self.todo_tree.column("Status", width=50, anchor="center")
        self.todo_tree.column("Task", width=300)
        self.todo_tree.column("Actions", width=100, anchor="center")
        
        self.todo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.todo_tree.yview)
        
        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg=self.bg_color)
        action_frame.pack(fill=tk.X, pady=5)
        
        # Complete button
        complete_button = tk.Button(
            action_frame,
            text="Toggle Complete",
            command=self.toggle_complete,
            bg=self.highlight_color,
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=10
        )
        complete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Edit button
        edit_button = tk.Button(
            action_frame,
            text="Edit",
            command=self.edit_todo,
            bg=self.highlight_color,
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=10
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        delete_button = tk.Button(
            action_frame,
            text="Delete",
            command=self.delete_todo,
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            padx=10
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Refresh todo list
        self.refresh_todo_list()
        
        # Ensure clean exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.todo_file):
            try:
                with open(self.todo_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.todo_file, "w") as f:
            json.dump(self.todos, f)
    
    def refresh_todo_list(self):
        """Refresh the todo list display"""
        # Clear current items
        for item in self.todo_tree.get_children():
            self.todo_tree.delete(item)
        
        # Add todos to the treeview
        for i, todo in enumerate(self.todos):
            status = "✓" if todo.get("completed", False) else "○"
            self.todo_tree.insert("", "end", iid=str(i), values=(status, todo["text"], ""))
    
    def add_todo(self):
        """Add a new todo"""
        todo_text = self.todo_entry.get().strip()
        if todo_text:
            self.todos.append({"text": todo_text, "completed": False})
            self.save_todos()
            self.refresh_todo_list()
            self.todo_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Todo cannot be empty!")
    
    def get_selected_todo_index(self):
        """Get the index of the selected todo"""
        selection = self.todo_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a todo first!")
            return None
        return int(selection[0])
    
    def toggle_complete(self):
        """Toggle the completion status of the selected todo"""
        index = self.get_selected_todo_index()
        if index is not None:
            self.todos[index]["completed"] = not self.todos[index].get("completed", False)
            self.save_todos()
            self.refresh_todo_list()
    
    def edit_todo(self):
        """Edit the selected todo"""
        index = self.get_selected_todo_index()
        if index is not None:
            # Create a dialog for editing
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Todo")
            edit_window.geometry("400x100")
            edit_window.configure(bg=self.bg_color)
            edit_window.resizable(False, False)
            
            # Make dialog modal
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            # Add editing widgets
            tk.Label(edit_window, text="Edit Todo:", bg=self.bg_color, font=("Helvetica", 12)).pack(pady=(10, 5))
            
            edit_entry = tk.Entry(edit_window, font=("Helvetica", 12), width=40)
            edit_entry.pack(pady=5, padx=10)
            edit_entry.insert(0, self.todos[index]["text"])
            edit_entry.select_range(0, tk.END)
            edit_entry.focus_set()
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.todos[index]["text"] = new_text
                    self.save_todos()
                    self.refresh_todo_list()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Todo cannot be empty!")
            
            # Save button
            save_button = tk.Button(
                edit_window,
                text="Save",
                command=save_edit,
                bg=self.highlight_color,
                fg="white",
                font=("Helvetica", 10),
                relief=tk.FLAT,
                padx=10
            )
            save_button.pack(pady=5)
            
            # Bind Enter key to save
            edit_entry.bind("<Return>", lambda event: save_edit())
            
            # Center the dialog window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
            y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
            edit_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def delete_todo(self):
        """Delete the selected todo"""
        index = self.get_selected_todo_index()
        if index is not None:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this todo?")
            if confirm:
                del self.todos[index]
                self.save_todos()
                self.refresh_todo_list()
    
    def on_closing(self):
        """Handle window closing event"""
        self.save_todos()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()