#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Šeit tiek izveidota klase ar mūsdienīgu dizainu
class ModernUI:
    # Krāsu palete - lai programma izskatītos smuki
    PRIMARY = "#3498db"       # Zila krāsa pogām
    SECONDARY = "#2ecc71"     # Zaļa krāsa pabeigšanas pogai
    DANGER = "#e74c3c"        # Sarkana krāsa dzēšanas pogai
    DARK = "#34495e"          # Tumša krāsa tekstam
    LIGHT = "#ecf0f1"         # Gaiša krāsa fonam
    WHITE = "#ffffff"         # Balta krāsa
    GRAY = "#95a5a6"          # Pelēka krāsa mazāk svarīgām lietām
    PINK = "#f4d3d7"          # Pelēka krāsa mazāk svarīgām lietām

    # Fontu iestatījumi - izmanto Helvetica, jo tas izskatās moderni
    FONT_FAMILY = "Helvetica"

    # Pogu stils - tās izskatās labāk ar aizpildījumu
    BTN_PADDING_X = 15
    BTN_PADDING_Y = 8

    # Pogām ir plakans izskats - tā ir modernāk
    BTN_RELIEF = tk.FLAT

# Galvenā klase, kas veido visu lietotni
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo App")
        self.root.geometry("550x600")
        self.root.minsize(500, 500)

        # Izmanto modernās krāsas no ModernUI klases
        self.ui = ModernUI()
        self.root.configure(bg=self.ui.LIGHT)

        # Mēģina iestatīt ikonu, ja tāda ir
        try:
            self.root.iconbitmap("todo_icon.ico")
        except:
            pass

        # Kur glabāt uzdevumus - saglabā JSON failā
        self.todo_file = "todos.json"
        self.todos = self.load_todos()

        # Izveido visus logrīkus
        self.create_widgets()

    def create_widgets(self):
        # Galvenais konteiners ar aizpildījumu malās
        container = tk.Frame(self.root, bg=self.ui.LIGHT)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Aplikācijas augšdaļa ar nosaukumu
        header_frame = tk.Frame(container, bg=self.ui.LIGHT)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Aplikācijas nosaukums ar ķeksīša ikonu
        title_label = tk.Label(
            header_frame,
            text="✓ Mani Uzdevumi",
            font=(self.ui.FONT_FAMILY, 22, "bold"),
            fg=self.ui.DARK,
            bg=self.ui.LIGHT
        )
        title_label.pack(side=tk.LEFT)

        # Šodienas datums labajā pusē
        date_str = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(
            header_frame,
            text=date_str,
            font=(self.ui.FONT_FAMILY, 12),
            fg=self.ui.GRAY,
            bg=self.ui.LIGHT
        )
        date_label.pack(side=tk.RIGHT, pady=10)

        # Ievades lauks un poga uzdevumu pievienošanai
        input_container = tk.Frame(container, bg=self.ui.LIGHT)
        input_container.pack(fill=tk.X, pady=(0, 15))

        # Skaists ievades lauks ar apmali
        input_frame = tk.Frame(
            input_container,
            bg=self.ui.WHITE,
            highlightbackground=self.ui.GRAY,
            highlightthickness=1,
            bd=0
        )
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Ikona pie ievades lauka
        task_icon = tk.Label(
            input_frame,
            text="➕",
            font=(self.ui.FONT_FAMILY, 12),
            bg=self.ui.WHITE,
            fg=self.ui.GRAY
        )
        task_icon.pack(side=tk.LEFT, padx=10)

        # Ievades lauks jauniem uzdevumiem
        self.todo_entry = tk.Entry(
            input_frame,
            font=(self.ui.FONT_FAMILY, 12),
            bd=0,
            highlightthickness=0,
            bg=self.ui.WHITE
        )
        self.todo_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10)
        self.todo_entry.bind("<Return>", lambda event: self.add_todo())
        self.todo_entry.insert(0, "Pievienot jaunu uzdevumu...")
        self.todo_entry.config(fg=self.ui.GRAY)

        # Notīra tekstu, kad uzklikšķina uz lauka
        def on_entry_focus_in(event):
            if self.todo_entry.get() == "Pievienot jaunu uzdevumu...":
                self.todo_entry.delete(0, tk.END)
                self.todo_entry.config(fg=self.ui.DARK)

        # Atjauno tekstu, ja lauks ir tukšs un vairs nav fokusā
        def on_entry_focus_out(event):
            if not self.todo_entry.get():
                self.todo_entry.insert(0, "Pievienot jaunu uzdevumu...")
                self.todo_entry.config(fg=self.ui.GRAY)

        self.todo_entry.bind("<FocusIn>", on_entry_focus_in)
        self.todo_entry.bind("<FocusOut>", on_entry_focus_out)

        # Poga uzdevumu pievienošanai
        add_button = tk.Button(
            input_container,
            text="Pievienot",
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

        # Uzdevumu skaitītājs - cik pabeigti, cik vēl jāizpilda
        stats_frame = tk.Frame(container, bg=self.ui.LIGHT)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Skaitītāja teksts (tiks atjaunots vēlāk)
        self.count_label = tk.Label(
            stats_frame,
            text="",  # Tiks iestatīts refresh_todo_list funkcijā
            font=(self.ui.FONT_FAMILY, 10),
            fg=self.ui.GRAY,
            bg=self.ui.LIGHT
        )
        self.count_label.pack(side=tk.LEFT)

        # Uzdevumu saraksta rāmis ar baltu fonu un apmali
        list_container = tk.Frame(
            container,
            bg=self.ui.WHITE,
            highlightbackground=self.ui.GRAY,
            highlightthickness=1,
            bd=0
        )
        list_container.pack(fill=tk.BOTH, expand=True)

        # Iekšējā aizpildījums sarakstam
        list_frame = tk.Frame(list_container, bg=self.ui.WHITE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Ritjosla un saraksts uzdevumiem
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Saraksta stila iestatījumi
        style = ttk.Style()
        style.theme_use('default')  # Atiestatīt tēmu, lai būtu vienādi
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
            background=[('selected', self.ui.PINK)],
            foreground=[('selected', self.ui.DARK)]
        )

        # Noņem apmales, lai izskatītos modernāk
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])

        # Galvenes stils
        style.configure(
            "Treeview.Heading",
            background=self.ui.LIGHT,
            foreground=self.ui.DARK,
            font=(self.ui.FONT_FAMILY, 10, 'bold')
        )

        # Izveido sarakstu ar kolonnām
        columns = ("Status", "Task", "Actions")
        self.todo_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set
        )

        # Konfigurē kolonnas
        self.todo_tree.heading("Status", text="")
        self.todo_tree.heading("Task", text="Uzdevums")
        self.todo_tree.heading("Actions", text="")

        self.todo_tree.column("Status", width=40, anchor="center")
        self.todo_tree.column("Task", width=400)
        self.todo_tree.column("Actions", width=60, anchor="center")

        self.todo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.todo_tree.yview)

        # Pievieno atzīmes, lai pabeigti uzdevumi būtu pelēki
        self.todo_tree.tag_configure('completed', foreground=self.ui.GRAY)
        self.todo_tree.tag_configure('odd_row', background=self.ui.LIGHT)

        # Pogu rāmis darbībām ar uzdevumiem
        action_frame = tk.Frame(container, bg=self.ui.LIGHT)
        action_frame.pack(fill=tk.X, pady=(15, 0))

        # Pabeigšanas poga ar ķeksīti
        complete_button = tk.Button(
            action_frame,
            text="✓ Pabeigt",
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

        # Rediģēšanas poga ar zīmuļa ikonu
        edit_button = tk.Button(
            action_frame,
            text="✎ Rediģēt",
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

        # Dzēšanas poga ar miskastes ikonu
        delete_button = tk.Button(
            action_frame,
            text="🗑 Dzēst",
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

        # Pievieno pogu efektus, kad peles kursors ir virs tām
        for button in (add_button, complete_button, edit_button, delete_button):
            self.setup_button_hover(button)

        # Dubultklikšķis, lai rediģētu - vispirms pārbauda, vai ir atlasīts elements
        def on_double_click(event):
            if self.todo_tree.selection():  # Turpina tikai, ja ir atlasīts uzdevums
                self.edit_todo()

        self.todo_tree.bind("<Double-1>", on_double_click)

        # Labā klikšķa izvēlne
        self.create_context_menu()

        # Atjauno uzdevumu sarakstu
        self.refresh_todo_list()

        # Pareiza aizvēršana, lai saglabātu uzdevumus
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_button_hover(self, button):
        """Pievieno pogām efektu, kad peles kursors ir virs tām"""
        original_bg = button['background']

        # Nedaudz tumšāka krāsa, kad kursors ir virs pogas
        def on_enter(e):
            r, g, b = button.winfo_rgb(original_bg)
            darker = f'#{int(r/256*0.9):02x}{int(g/256*0.9):02x}{int(b/256*0.9):02x}'
            button['background'] = darker

        def on_leave(e):
            button['background'] = original_bg

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def create_context_menu(self):
        """Izveido labā klikšķa izvēlni"""
        self.context_menu = tk.Menu(self.root, tearoff=0, bg=self.ui.WHITE, fg=self.ui.DARK)
        self.context_menu.add_command(label="Pabeigt/Atsākt", command=self.toggle_complete)
        self.context_menu.add_command(label="Rediģēt", command=self.edit_todo)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Dzēst", command=self.delete_todo)

        def show_context_menu(event):
            # Parāda tikai, ja ir atlasīts uzdevums
            if self.todo_tree.selection():
                self.context_menu.post(event.x_root, event.y_root)

        self.todo_tree.bind("<Button-3>", show_context_menu)

    def load_todos(self):
        """Ielādē uzdevumus no JSON faila"""
        if os.path.exists(self.todo_file):
            try:
                with open(self.todo_file, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_todos(self):
        """Saglabā uzdevumus JSON failā"""
        with open(self.todo_file, "w") as f:
            json.dump(self.todos, f)

    def refresh_todo_list(self):
        """Atjauno uzdevumu sarakstu"""
        # Notīra visus tagadējos ierakstus
        for item in self.todo_tree.get_children():
            self.todo_tree.delete(item)

        # Pievieno uzdevumus sarakstam
        completed_count = 0
        for i, todo in enumerate(self.todos):
            # Nosaka statusu un atzīmes
            completed = todo.get("completed", False)
            if completed:
                completed_count += 1
                status = "✓"
                tags = ('completed',)
            else:
                status = "○"
                tags = ()

            # Pievieno mainīgo fonu katrai otrajai rindai
            if i % 2 == 1:
                tags = tags + ('odd_row',)

            self.todo_tree.insert("", "end", iid=str(i), values=(status, todo["text"], ""), tags=tags)

        # Atjauno skaitītāja tekstu
        total = len(self.todos)
        self.count_label.config(text=f"{completed_count} pabeigti, {total-completed_count} aktīvi")

    def add_todo(self):
        """Pievieno jaunu uzdevumu"""
        todo_text = self.todo_entry.get().strip()

        # Nepievieno, ja tas ir noklusējuma teksts
        if todo_text == "Pievienot jaunu uzdevumu...":
            return

        if todo_text:
            self.todos.append({"text": todo_text, "completed": False})
            self.save_todos()
            self.refresh_todo_list()
            self.todo_entry.delete(0, tk.END)

            # Atjauno fokusu uz ievades lauku, lai varētu ātri pievienot vairākus
            self.todo_entry.focus_set()
        else:
            messagebox.showwarning("Brīdinājums", "Uzdevums nevar būt tukšs!")

    def get_selected_todo_index(self):
        """Iegūst atlasītā uzdevuma indeksu"""
        selection = self.todo_tree.selection()
        if not selection:
            messagebox.showwarning("Brīdinājums", "Lūdzu, atlasiet uzdevumu!")
            return None
        return int(selection[0])

    def toggle_complete(self):
        """Pārslēdz uzdevuma pabeigšanas statusu"""
        index = self.get_selected_todo_index()
        if index is not None:
            self.todos[index]["completed"] = not self.todos[index].get("completed", False)
            self.save_todos()
            self.refresh_todo_list()

    def edit_todo(self):
        """Rediģē atlasīto uzdevumu"""
        index = self.get_selected_todo_index()
        if index is not None:
            # Izveido dialoglogu rediģēšanai
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Rediģēt uzdevumu")
            edit_window.geometry("450x150")
            edit_window.configure(bg=self.ui.LIGHT)
            edit_window.resizable(False, False)

            # Pievieno aizpildījuma konteineru
            edit_container = tk.Frame(edit_window, bg=self.ui.LIGHT, padx=20, pady=20)
            edit_container.pack(fill=tk.BOTH, expand=True)

            # Pievieno rediģēšanas logrīkus
            tk.Label(
                edit_container,
                text="Rediģēt uzdevumu",
                bg=self.ui.LIGHT,
                fg=self.ui.DARK,
                font=(self.ui.FONT_FAMILY, 14, "bold")
            ).pack(anchor="w", pady=(0, 10))

            # Izveido stilizētu ievades lauku ar apmali
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

            # Pogu konteiners
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
                    messagebox.showwarning("Brīdinājums", "Uzdevums nevar būt tukšs!")

            # Atcelšanas poga
            cancel_button = tk.Button(
                button_frame,
                text="Atcelt",
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

            # Saglabāšanas poga
            save_button = tk.Button(
                button_frame,
                text="Saglabāt",
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

            # Pievieno pogu efektus
            self.setup_button_hover(cancel_button)
            self.setup_button_hover(save_button)

            # Enter taustiņš, lai saglabātu
            edit_entry.bind("<Return>", lambda event: save_edit())

            # Padara dialoglogu modālu PĒC tā izveidošanas
            edit_window.update()  # Atjauno logu

            # Padara logu atkarīgu no galvenā loga
            edit_window.transient(self.root)

            # Iestata saķeršanu tikai pēc loga atjaunošanas
            edit_window.focus_set()  # Iestata fokusu uz logu
            edit_window.grab_set()   # Padara to modālu

            # Centrē dialoglogu
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
            y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
            edit_window.geometry(f"{width}x{height}+{x}+{y}")

            # Iestata fokusu uz ievades lauku
            edit_entry.focus_set()

    def delete_todo(self):
        """Dzēš atlasīto uzdevumu"""
        index = self.get_selected_todo_index()
        if index is not None:
            # Izveido apstiprinājuma dialoglogu
            confirm_window = tk.Toplevel(self.root)
            confirm_window.title("Apstiprināt dzēšanu")
            confirm_window.geometry("400x150")
            confirm_window.configure(bg=self.ui.LIGHT)
            confirm_window.resizable(False, False)

            # Pievieno aizpildījuma konteineru
            confirm_container = tk.Frame(confirm_window, bg=self.ui.LIGHT, padx=20, pady=20)
            confirm_container.pack(fill=tk.BOTH, expand=True)

            # Brīdinājuma ikona un ziņojums
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
                text="Vai tiešām vēlaties dzēst šo uzdevumu?",
                font=(self.ui.FONT_FAMILY, 12),
                bg=self.ui.LIGHT,
                fg=self.ui.DARK,
                wraplength=280,
                justify=tk.LEFT
            )
            message_text.pack(side=tk.LEFT, fill=tk.BOTH)

            # Pogu konteiners
            button_frame = tk.Frame(confirm_container, bg=self.ui.LIGHT)
            button_frame.pack(fill=tk.X)

            # Atcelšanas poga
            cancel_button = tk.Button(
                button_frame,
                text="Atcelt",
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

            # Dzēšanas poga
            def confirm_delete():
                del self.todos[index]
                self.save_todos()
                self.refresh_todo_list()
                confirm_window.destroy()

            delete_button = tk.Button(
                button_frame,
                text="Dzēst",
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

            # Pievieno pogu efektus
            self.setup_button_hover(cancel_button)
            self.setup_button_hover(delete_button)

            # Padara dialoglogu modālu PĒC tā izveidošanas
            confirm_window.update()  # Atjauno logu

            # Padara logu atkarīgu no galvenā loga
            confirm_window.transient(self.root)

            # Iestata saķeršanu tikai pēc loga atjaunošanas
            confirm_window.focus_set()  # Iestata fokusu uz logu
            confirm_window.grab_set()   # Padara to modālu

            # Centrē dialoglogu
            confirm_window.update_idletasks()
            width = confirm_window.winfo_width()
            height = confirm_window.winfo_height()
            x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
            y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
            confirm_window.geometry(f"{width}x{height}+{x}+{y}")

    def on_closing(self):
        """Apstrādā loga aizvēršanas notikumu"""
        self.save_todos()
        self.root.destroy()

# Programmas palaišana
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
