#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ModernUI:
    # Modern color palette
    PRIMARY = "#3498db"       # Main brand color (blue)
    SECONDARY = "#2ecc71"     # Success/confirmation color (green)
    DANGER = "#e74c3c"        # Destructive/warning color (red)
    DARK = "#34495e"          # Dark text/elements
    LIGHT = "#ecf0f1"         # Light background
    WHITE = "#ffffff"         # Pure white
    GRAY = "#95a5a6"          # Neutral/disabled color
    
    # Font settings
    FONT_FAMILY = "Helvetica"
    
    # Button styles
    BTN_PADDING_X = 15
    BTN_PADDING_Y = 8
    
    # Rounded corners for buttons (using flat relief and specific backgrounds)
    BTN_RELIEF = tk.FLAT

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("550x600")
        self.root.minsize(500, 500)
        
        # Set theme colors
        self.ui = ModernUI()
        self.root.configure(bg=self.ui.LIGHT)
        
        # Set app icon (if available)
        try:
            # Attempt to set an icon - this is optional and platform-dependent
            self.root.iconbitmap("todo_icon.ico")  # You would need to create this icon file
        except:
            pass
        
        # Data storage
        self.todo_file = "todos.json"
        self.todos = self.load_todos()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        container = tk.Frame(self.root, bg=self.ui.LIGHT)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # App header with shadow effect
        header_frame = tk.Frame(container, bg=self.ui.LIGHT)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # App logo/title
        title_label = tk.Label(
            header_frame, 
            text="✓ My Tasks",
            font=(self.ui.FONT_FAMILY, 22, "bold"), 
            fg=self.ui.DARK,
            bg=self.ui.LIGHT
        )
        title_label.pack(side=tk.LEFT)
        
        # Current date display
        date_str = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(
            header_frame,
            text=date_str,
            font=(self.ui.FONT_FAMILY, 12),
            fg=self.ui.GRAY,
            bg=self.ui.LIGHT
        )
        date_label.pack(side=tk.RIGHT, pady=10)
        
        # Search and add container
        input_container = tk.Frame(container, bg=self.ui.LIGHT)
        input_container.pack(fill=tk.X, pady=(0, 15))
        
        # Stylish input with border and rounded corners
        input_frame = tk.Frame(
            input_container, 
            bg=self.ui.WHITE,
            highlightbackground=self.ui.GRAY,
            highlightthickness=1,
            bd=0
        )
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Input icon
        task_icon = tk.Label(
            input_frame, 
            text="➕", 
            font=(self.ui.FONT_FAMILY, 12),
            bg=self.ui.WHITE,
            fg=self.ui.GRAY
        )
        task_icon.pack(side=tk.LEFT, padx=10)
        
        # Todo input
        self.todo_entry = tk.Entry(
            input_frame, 
            font=(self.ui.FONT_FAMILY, 12),
            bd=0,
            highlightthickness=0,
            bg=self.ui.WHITE
        )
        self.todo_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10)
        self.todo_entry.bind("<Return>", lambda event: self.add_todo())
        self.todo_entry.insert(0, "Add a new task...")
        self.todo_entry.config(fg=self.ui.GRAY)
        
        # Clear placeholder on focus
        def on_entry_focus_in(event):
            if self.todo_entry.get() == "Add a new task...":
                self.todo_entry.delete(0, tk.END)
                self.todo_entry.config(fg=self.ui.DARK)
                
        # Restore placeholder on focus out if empty
        def on_entry_focus_out(event):
            if not self.todo_entry.get():
                self.todo_entry.insert(0, "Add a new task...")
                self.todo_entry.config(fg=self.ui.GRAY)
                
        self.todo_entry.bind("<FocusIn>", on_entry_focus_in)
        self.todo_entry.bind("<FocusOut>", on_entry_focus_out)
        
        # Add button
        add_button = tk.Button(
            input_container,
            text="Add Task",
            command=self.add_todo,
            bg=self.ui.PRIMARY,
            fg=self.ui.WHITE,
            font=(self.ui.FONT_FAMILY, 10, "bold"),
            relief=self.ui.BTN_RELIEF,
            padx=self.ui.BTN_PADDING_X,
            pady=self.ui.BTN_PADDING_Y,
            cursor="hand2"
        )
        add_button.pack(side=tk.RIGHT)
        
        # Task counts
        stats_frame = tk.Frame(container, bg=self.ui.LIGHT)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Todo count label (updated in refresh_todo_list)
        self.count_label = tk.Label(
            stats_frame,
            text="",  # Will be set in refresh_todo_list
            font=(self.ui.FONT_FAMILY, 10),
            fg=self.ui.GRAY,
            bg=self.ui.LIGHT
        )
        self.count_label.pack(side=tk.LEFT)
        
        # Task list frame with white background and border
        list_container = tk.Frame(
            container, 
            bg=self.ui.WHITE,
            highlightbackground=self.ui.GRAY,
            highlightthickness=1,
            bd=0
        )
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Inner padding for list
        list_frame = tk.Frame(list_container, bg=self.ui.WHITE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar and Treeview for todo list
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Define Treeview style
        style = ttk.Style()
        style.theme_use('default')  # Reset theme for consistency
        style.configure(
            "Treeview", 
            background=self.ui.WHITE,
            foreground=self.ui.DARK,
            rowheight=40,
            fieldbackground=self.ui.WHITE,
            borderwidth=0,
            font=(self.ui.FONT_FAMILY, 11)
        )
        style.map(
            'Treeview', 
            background=[('selected', self.ui.LIGHT)],
            foreground=[('selected', self.ui.DARK)]
        )
        
        # Remove borders
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        # Header style
        style.configure(
            "Treeview.Heading",
            background=self.ui.LIGHT,
            foreground=self.ui.DARK,
            font=(self.ui.FONT_FAMILY, 10, 'bold')
        )
        
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
        self.todo_tree.heading("Status", text="")
        self.todo_tree.heading("Task", text="Task")
        self.todo_tree.heading("Actions", text="")
        
        self.todo_tree.column("Status", width=40, anchor="center")
        self.todo_tree.column("Task", width=400)
        self.todo_tree.column("Actions", width=60, anchor="center")
        
        self.todo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.todo_tree.yview)
        
        # Add some tag configurations for visual variety
        self.todo_tree.tag_configure('completed', foreground=self.ui.GRAY)
        self.todo_tree.tag_configure('odd_row', background=self.ui.LIGHT)
        
        # Action buttons frame
        action_frame = tk.Frame(container, bg=self.ui.LIGHT)
        action_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Complete button
        complete_button = tk.Button(
            action_frame,
            text="✓ Complete",
            command=self.toggle_complete,
            bg=self.ui.SECONDARY,
            fg=self.ui.WHITE,
            font=(self.ui.FONT_FAMILY, 10, "bold"),
            relief=self.ui.BTN_RELIEF,
            padx=self.ui.BTN_PADDING_X,
            pady=self.ui.BTN_PADDING_Y,
            cursor="hand2"
        )
        complete_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Edit button
        edit_button = tk.Button(
            action_frame,
            text="✎ Edit",
            command=self.edit_todo,
            bg=self.ui.PRIMARY,
            fg=self.ui.WHITE,
            font=(self.ui.FONT_FAMILY, 10, "bold"),
            relief=self.ui.BTN_RELIEF,
            padx=self.ui.BTN_PADDING_X,
            pady=self.ui.BTN_PADDING_Y,
            cursor="hand2"
        )
        edit_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Delete button
        delete_button = tk.Button(
            action_frame,
            text="🗑 Delete",
            command=self.delete_todo,
            bg=self.ui.DANGER,
            fg=self.ui.WHITE,
            font=(self.ui.FONT_FAMILY, 10, "bold"),
            relief=self.ui.BTN_RELIEF,
            padx=self.ui.BTN_PADDING_X,
            pady=self.ui.BTN_PADDING_Y,
            cursor="hand2"
        )
        delete_button.pack(side=tk.LEFT)
        
        # Button hover effects (for all buttons)
        for button in (add_button, complete_button, edit_button, delete_button):
            self.setup_button_hover(button)
        
        # Double click to edit - FIXED to check for selection first
        def on_double_click(event):
            if self.todo_tree.selection():  # Only proceed if an item is selected
                self.edit_todo()
                
        self.todo_tree.bind("<Double-1>", on_double_click)
        
        # Right-click context menu
        self.create_context_menu()
        
        # Refresh todo list
        self.refresh_todo_list()
        
        # Ensure clean exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_button_hover(self, button):
        """Add hover effect to buttons"""
        original_bg = button['background']
        
        # Slightly darker on hover
        def on_enter(e):
            # Create slightly darker color for hover effect
            r, g, b = button.winfo_rgb(original_bg)
            darker = f'#{int(r/256*0.9):02x}{int(g/256*0.9):02x}{int(b/256*0.9):02x}'
            button['background'] = darker
            
        def on_leave(e):
            button['background'] = original_bg
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_context_menu(self):
        """Create right-click context menu"""
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.ui.WHITE, fg=self.ui.DARK)
        self.context_menu.add_command(label="Complete/Incomplete", command=self.toggle_complete)
        self.context_menu.add_command(label="Edit Task", command=self.edit_todo)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete Task", command=self.delete_todo)
        
        def show_context_menu(event):
            # Only show if there's a selection
            if self.todo_tree.selection():
                self.context_menu.post(event.x_root, event.y_root)
                
        self.todo_tree.bind("<Button-3>", show_context_menu)
    
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
        completed_count = 0
        for i, todo in enumerate(self.todos):
            # Determine status icon and tags
            completed = todo.get("completed", False)
            if completed:
                completed_count += 1
                status = "✓"
                tags = ('completed',)
            else:
                status = "○"
                tags = ()
                
            # Add alternating row background
            if i % 2 == 1:
                tags = tags + ('odd_row',)
                
            self.todo_tree.insert("", "end", iid=str(i), values=(status, todo["text"], ""), tags=tags)
        
        # Update count label
        total = len(self.todos)
        self.count_label.config(text=f"{completed_count} completed, {total-completed_count} remaining")
    
    def add_todo(self):
        """Add a new todo"""
        todo_text = self.todo_entry.get().strip()
        
        # Don't add if it's the placeholder text
        if todo_text == "Add a new task...":
            return
            
        if todo_text:
            self.todos.append({"text": todo_text, "completed": False})
            self.save_todos()
            self.refresh_todo_list()
            self.todo_entry.delete(0, tk.END)
            
            # Reset focus to input for quick multiple entries
            self.todo_entry.focus_set()
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
            edit_window.title("Edit Task")
            edit_window.geometry("450x150")
            edit_window.configure(bg=self.ui.LIGHT)
            edit_window.resizable(False, False)
            
            # Add padding container
            edit_container = tk.Frame(edit_window, bg=self.ui.LIGHT, padx=20, pady=20)
            edit_container.pack(fill=tk.BOTH, expand=True)
            
            # Add editing widgets
            tk.Label(
                edit_container, 
                text="Edit Task", 
                bg=self.ui.LIGHT, 
                fg=self.ui.DARK,
                font=(self.ui.FONT_FAMILY, 14, "bold")
            ).pack(anchor="w", pady=(0, 10))
            
            # Create styled input field with border
            input_frame = tk.Frame(
                edit_container, 
                bg=self.ui.WHITE,
                highlightbackground=self.ui.GRAY,
                highlightthickness=1,
                bd=0
            )
            input_frame.pack(fill=tk.X, pady=(0, 15))
            
            edit_entry = tk.Entry(
                input_frame, 
                font=(self.ui.FONT_FAMILY, 12),
                bd=0,
                highlightthickness=0,
                bg=self.ui.WHITE
            )
            edit_entry.pack(fill=tk.X, ipady=10, padx=10)
            edit_entry.insert(0, self.todos[index]["text"])
            edit_entry.select_range(0, tk.END)
            
            # Buttons container
            button_frame = tk.Frame(edit_container, bg=self.ui.LIGHT)
            button_frame.pack(fill=tk.X)
            
            def save_edit():
                new_text = edit_entry.get().strip()
                if new_text:
                    self.todos[index]["text"] = new_text
                    self.save_todos()
                    self.refresh_todo_list()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Task cannot be empty!")
            
            # Cancel button
            cancel_button = tk.Button(
                button_frame,
                text="Cancel",
                command=edit_window.destroy,
                bg=self.ui.LIGHT,
                fg=self.ui.DARK,
                font=(self.ui.FONT_FAMILY, 10),
                relief=self.ui.BTN_RELIEF,
                padx=self.ui.BTN_PADDING_X,
                pady=self.ui.BTN_PADDING_Y,
                cursor="hand2"
            )
            cancel_button.pack(side=tk.LEFT, padx=(0, 10))
            
            # Save button
            save_button = tk.Button(
                button_frame,
                text="Save",
                command=save_edit,
                bg=self.ui.PRIMARY,
                fg=self.ui.WHITE,
                font=(self.ui.FONT_FAMILY, 10, "bold"),
                relief=self.ui.BTN_RELIEF,
                padx=self.ui.BTN_PADDING_X,
                pady=self.ui.BTN_PADDING_Y,
                cursor="hand2"
            )
            save_button.pack(side=tk.LEFT)
            
            # Add hover effects
            self.setup_button_hover(cancel_button)
            self.setup_button_hover(save_button)
            
            # Bind Enter key to save
            edit_entry.bind("<Return>", lambda event: save_edit())
            
            # Make dialog modal AFTER it's fully created
            edit_window.update()  # Force update of the window
            
            # Make the window transient for the main window
            edit_window.transient(self.root)
            
            # Set grab only after window is updated/visible
            edit_window.focus_set()  # Set focus to the window
            edit_window.grab_set()   # Make it modal
            
            # Center the dialog window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
            y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
            edit_window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Set focus to the entry field after window is fully configured
            edit_entry.focus_set()
    
    def delete_todo(self):
        """Delete the selected todo"""
        index = self.get_selected_todo_index()
        if index is not None:
            # Create confirmation dialog
            confirm_window = tk.Toplevel(self.root)
            confirm_window.title("Confirm Deletion")
            confirm_window.geometry("400x150")
            confirm_window.configure(bg=self.ui.LIGHT)
            confirm_window.resizable(False, False)
            
            # Add padding container
            confirm_container = tk.Frame(confirm_window, bg=self.ui.LIGHT, padx=20, pady=20)
            confirm_container.pack(fill=tk.BOTH, expand=True)
            
            # Warning icon and message
            message_frame = tk.Frame(confirm_container, bg=self.ui.LIGHT)
            message_frame.pack(fill=tk.X, pady=(0, 15))
            
            warning_icon = tk.Label(
                message_frame,
                text="⚠️",
                font=(self.ui.FONT_FAMILY, 24),
                bg=self.ui.LIGHT,
                fg=self.ui.DANGER
            )
            warning_icon.pack(side=tk.LEFT, padx=(0, 15))
            
            message_text = tk.Label(
                message_frame,
                text="Are you sure you want to delete this task?",
                font=(self.ui.FONT_FAMILY, 12),
                bg=self.ui.LIGHT,
                fg=self.ui.DARK,
                wraplength=280,
                justify=tk.LEFT
            )
            message_text.pack(side=tk.LEFT, fill=tk.BOTH)
            
            # Buttons container
            button_frame = tk.Frame(confirm_container, bg=self.ui.LIGHT)
            button_frame.pack(fill=tk.X)
            
            # Cancel button
            cancel_button = tk.Button(
                button_frame,
                text="Cancel",
                command=confirm_window.destroy,
                bg=self.ui.LIGHT,
                fg=self.ui.DARK,
                font=(self.ui.FONT_FAMILY, 10),
                relief=self.ui.BTN_RELIEF,
                padx=self.ui.BTN_PADDING_X,
                pady=self.ui.BTN_PADDING_Y,
                cursor="hand2"
            )
            cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
            
            # Delete button
            def confirm_delete():
                del self.todos[index]
                self.save_todos()
                self.refresh_todo_list()
                confirm_window.destroy()
                
            delete_button = tk.Button(
                button_frame,
                text="Delete",
                command=confirm_delete,
                bg=self.ui.DANGER,
                fg=self.ui.WHITE,
                font=(self.ui.FONT_FAMILY, 10, "bold"),
                relief=self.ui.BTN_RELIEF,
                padx=self.ui.BTN_PADDING_X,
                pady=self.ui.BTN_PADDING_Y,
                cursor="hand2"
            )
            delete_button.pack(side=tk.RIGHT)
            
            # Add hover effects
            self.setup_button_hover(cancel_button)
            self.setup_button_hover(delete_button)
            
            # Make dialog modal AFTER it's fully created
            confirm_window.update()  # Force update of the window
            
            # Make the window transient for the main window
            confirm_window.transient(self.root)
            
            # Set grab only after window is updated/visible
            confirm_window.focus_set()  # Set focus to the window
            confirm_window.grab_set()   # Make it modal
            
            # Center the dialog window
            confirm_window.update_idletasks()
            width = confirm_window.winfo_width()
            height = confirm_window.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
            y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
            confirm_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_closing(self):
        """Handle window closing event"""
        self.save_todos()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()