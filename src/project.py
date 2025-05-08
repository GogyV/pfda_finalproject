import tkinter as tk
from tkinter import messagebox
import json

class DungeonDelversCodex:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Delver's Codex")
        self.root.geometry("1000x700")
        tk.Label(root, text="Dungeon Delver's Codex", font=("Rage Italic", 80)).pack(pady=20)
        tk.Button(root, text="Create New Character", width=30, command=self.create_new_character).pack(pady=5)
        tk.Button(root, text="View Created Characters", width=30, command=self.view_characters).pack(pady=5)
        tk.Button(root, text="Exit", width=30, command=root.save_and_exit).pack(pady=20)

        self.characters = []
        self.load_from_file()


    def create_new_character(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Create New Character")
        fields = ["Name", "HP", "STR", "DEX", "CON", "INT", "WIS", "CHA"]
        name_entries = {}

        for field in fields:
            tk.Label(new_window, text=f"{field}:").pack()
            name_entry = tk.Entry(new_window)
            name_entry.pack()
            name_entries[field] = name_entry
        
        def save():
            try:
                name = name_entries["Name"].get().strip()
                if not name:
                    raise ValueError("Name is required.")
                
                hp = int(name_entries["HP"].get())
                stats = {key: int(name_entries[key].get()) for key in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]}

                self.characters.append({
                    "name": name,
                    "hp": hp,
                    "stats": stats,
                    "inventory": [],
                    "equipment": {}
                })
                messagebox.showinfo("Saved", f"Character '{name}' created!")
                new_window.destroy()
            except ValueError as e:
                messagebox.showwarning("Invalid Input", str(e))

        tk.Button(new_window, text="Save Character", command=save).pack(pady=10)

    def view_character(self):
         if not self.characters:
            messagebox.showinfo("No Characters", "No characters have been created yet.")
            return
        
    view_window = tk.Toplevel(self.root)
    view_window.title("Created Characters")
    
    for idx, char in enumerate(self.characters):
        tk.Button(view_window, text=f"{char['name']} - HP: {char['hp']}", command=lambda i=idx: self.open_character_sheet(i)).pack(pady=2)

    def open_character_sheet (self. index):
        character = self.characters[index]
        sheet = tk.Toplevel(self.root)
        sheet.title(f"{character['name']}'s Sheet")

        hp_label = tk.Label(sheet, text=f"HP: {character['hp']}")
        hp_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDelversCodex(root)
    root.mainloop()