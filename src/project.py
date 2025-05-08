import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import json

class DungeonDelversCodex:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Delver's Codex")
        self.root.geometry("1000x700")
        tk.Label(root, text="Dungeon Delver's Codex", font=("Rage Italic", 80)).pack(pady=20)
        tk.Button(root, text="Create New Character", width=30, command=self.create_new_character).pack(pady=5)
        tk.Button(root, text="View Created Characters", width=30, command=self.view_characters).pack(pady=5)
        tk.Button(root, text="Exit", width=30, command=self.save_and_exit).pack(pady=20)

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
                    "equipment": {},
                    "image": None
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

        tk.Label(sheet, text=f"{character['name']}'s Character Sheet", font=("Helvetica", 14, "bold")).pack(pady=(5, 10))
        hp_frame = tk.Frame(sheet)
        hp_frame.pack()
        hp_label = tk.Label(hp_frame, text=f"HP: {character['hp']}", font=("Helvetica", 12))
        hp_label.pack(side=tk.LEFT, padx=10)
        tk.Button(hp_frame, text="+1", command=lambda: self.change_hp(character, 1, hp_label)).pack(side=tk.LEFT)
        tk.Button(hp_frame, text="-1", command=lambda: self.change_hp(character, -1, hp_label)).pack(side=tk.LEFT)

        tk.Label(sheet, text="Stats:", font=("Rage Italic", 50, "underline")).pack(pady=(10, 5))
        for stat, value in character["stats"].items():
            stat_frame = tk.Frame(sheet)
            stat_frame.pack(pady=2)
            label = tk.Label(stat_frame, text=f"{stat}: {value}", width=20)
            label.pack(side=tk.LEFT)
            tk.Button(stat_frame, text="+", command=lambda s=stat, l=label: self.adjust_stat(character, s, 1, l)).pack(side=tk.LEFT)
            tk.Button(stat_frame, text="-", command=lambda s=stat, l=label: self.adjust_stat(character, s, -1, l)).pack(side=tk.LEFT)

        tk.Label(sheet, text="Inventory:", font=("Rage Italic", 50, "underline")).pack(pady=(10, 5))
        inv_box = tk.Listbox(sheet, height=10, width=30)
        inv_box.pack()

        for item in character["inventory"]:
            inv_box.insert(tk.END, item)
        
        item_entry = tk.Entry(sheet)
        item_entry.pack(pady=5)

        img_frame = tk.Frame(sheet)
        img_frame.pack(pady=10)

        def load_profile_image(path):
            img = Image.open(path)
            img = img.resize((300, 300))
            return ImageTk.PhotoImage(img)
        image_label = tk.Label(img_frame)
        image_label.pack()

        if character.get("image"):
            try:
                photo = load_profile_image(character["image"])
                image_label.config(image=photo)
                image_label.image = photo
            except:
                image_label.config(text="Image not found")
        
        def upload_image():
            filepath = filedialog.askopenfilename(
                title="Select Profile Picture",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
            )
            if filepath:
                character["image"] = filepath
                photo = load_profile_image(filepath)
                image_label.config(image=photo)
                image_label.image = photo
        tk.Button(img_frame, text="Upload Profile Picture", command=upload_image).pack()


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

    def change_hp(self, character, amount, label):
            character["hp"] += amount
            label.config(text=f"HP: {character['hp']}")

    def adjust_stat(self, character, stat, amount, label):
        character["stats"][stat] += amount
        label.config(text=f"{stat}: {character['stats'][stat]}")

    def save_and_exit(self):
        self.save_to_file()
        self.root.quit()

    def save_to_file(self):
        with open("characters.json", "w") as f:
            json.dump(self.characters, f, indent=2)
    
    def load_from_file(self):
        try:
            with open("characters.json", "r") as f:
                self.characters = json.load(f)
        except FileNotFoundError:
            self.characters = []

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDelversCodex(root)
    root.mainloop()