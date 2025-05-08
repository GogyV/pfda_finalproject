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

    def view_characters(self):
         if not self.characters:
            messagebox.showinfo("No Characters", "No characters have been created yet.")
            return
         view_window = tk.Toplevel(self.root)
         view_window.title("Existing Characters")

         for idx, char in enumerate(self.characters): tk.Button(view_window, text=f"{char['name']} - HP: {char['hp']}", command=lambda i=idx: self.open_character_sheet(i)).pack(pady=2)

    def open_character_sheet(self, index):
        character = self.characters[index]
        sheet = tk.Toplevel(self.root)
        sheet.title(f"{character['name']}'s Sheet")

        hp_label = tk.Label(sheet, text=f"HP: {character['hp']}")
        hp_label.pack()

        def change_hp(amount):
            character['hp'] += amount
            hp_label.config(text=f"HP: {character['hp']}")
            tk.Button(sheet, text="+1 HP", command=lambda: change_hp(1)).pack()
            tk.Button(sheet, text="-1 HP", command=lambda: change_hp(-1)).pack()

            stat_labels = {}
            tk.Label(sheet, text="Stats:").pack()
            for stat, value in character["stats"].items():
                frame = tk.Frame(sheet)
                frame.pack()
                label = tk.Label(frame, text=f"{stat}: {value}", width=20)
                label.pack(side=tk.LEFT)
                tk.Button(frame, text="+", command=lambda s=stat: self.adjust_stat(character, s, 1, label)).pack(side=tk.LEFT)
                tk.Button(frame, text="-", command=lambda s=stat: self.adjust_stat(character, s, -1, label)).pack(side=tk.LEFT)
                stat_labels[stat] = label
            
            tk.Label(sheet, text="Inventory:").pack()
            inv_box = tk.Listbox(sheet, height=5)
            inv_box.pack()
            for Item in character["Inventory"]:
                inv_box.pack()
            item_entry = tk.Entry(sheet)
            item_entry.pack()

            def add_item():
                item = item_entry.get().strip()
                if item:
                    character["inventory"].append(item)
                    inv_box.insert(tk.END, item)
                    item_entry.delete(0, tk.END)
            
            def remove_selected_item():
                selected = inv_box.curselection()
                if selected:
                    index = selected[0]
                    inv_box.delete(index)
                    del character["inventory"][index]

            tk.Button(sheet, text="Add Item", command=add_item).pack()
            tk.Button(sheet, text="Remove Selected", command=remove_selected_item).pack()
                
    def adjust_stat(self, character, stat, amount, label):
        character["stats"][stat] += amount
        label.config(text=f"{stat}: {character['stats'][stat]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDelversCodex(root)
    root.mainloop()