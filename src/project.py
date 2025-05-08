import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import json
import os

class DungeonDelversCodex:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Delver's Codex")
        self.root.geometry("1000x700")

        self.characters = []
        self.load_from_file()
        self.load_characters()
        self.main_menu

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(root, text="Dungeon Delver's Codex", font=("Rage Italic", 80)).pack(pady=20)
        tk.Button(root, text="Create New Character", width=30, command=self.create_new_character).pack(pady=5)
        tk.Button(root, text="View Created Characters", width=30, command=self.view_characters).pack(pady=5)
        tk.Button(root, text="Exit", width=30, command=self.save_and_exit).pack(pady=20)

    def create_new_character(self):
        popup = tk.Toplevel(self.root)
        popup.title("New Character")

        tk.Label(popup, text="Name:").pack()
        name_entries = tk.Entry(popup)
        name_entries.pack()

        tk.Label(popup, text="HP:").pack()
        hp_entry = tk.Entry(popup)
        hp_entry.pack()

        stat = {}
        stat_labels = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        stat_entries = {}
        for stat in stat_labels:
            tk.Label(popup, text=f"{stat}:").pack()
            entry = tk.Entry(popup)
            entry.pack()
            stat_entries[stat] = entry
        
        # Species
        tk.Label(popup, text="Species:").pack()
        species_var = tk.StringVar()
        species_options = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome", "Half-Orc", "Tiefling", "Aasimar", "Tabaxi", "Kitsune", "Yuan-ti", "Shifter", "Harpy"]
        ttk.Combobox(popup, textvariable=species_var, values=species_options, state="readonly").pack()

        # Alignment
        tk.Label(popup, text="Alignment:").pack()
        alignment_var = tk.StringVar()
        alignment_options = [
            "Lawful Good", "Neutral Good", "Chaotic Good",
            "Lawful Neutral", "True Neutral", "Chaotic Neutral",
            "Lawful Evil", "Neutral Evil", "Chaotic Evil"
        ]
        ttk.Combobox(popup, textvariable=alignment_var, values=alignment_options, state="readonly").pack()

        # Class, Subclass, Level
        tk.Label(popup, text="Class:").pack()
        class_var = tk.StringVar()
        class_options = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard", "Artificer"]
        ttk.Combobox(popup, textvariable=class_var, values=class_options, state="readonly").pack()

        tk.Label(popup, text="Subclass:").pack()
        subclass_entry = tk.Entry(popup)
        subclass_entry.pack()

        tk.Label(popup, text="Level:").pack()
        level_entry = tk.Entry(popup)
        level_entry.pack()

        is_multiclass = tk.BooleanVar()
        tk.Checkbutton(popup, text="Multiclass?", variable=is_multiclass).pack()

        tk.Label(popup, text="Second Class:").pack()
        second_class_var = tk.StringVar()
        ttk.Combobox(popup, textvariable=second_class_var, values=class_options, state="readonly").pack()

        tk.Label(popup, text="Second Subclass:").pack()
        second_subclass_entry = tk.Entry(popup)
        second_subclass_entry.pack()

        tk.Label(popup, text="Second Level:").pack()
        second_level_entry = tk.Entry(popup)
        second_level_entry.pack()

        def save():
            stats = {stat: int(stat_entries[stat].get()) for stat in stat_labels}
            character = {
                "name": name_entries.get(),
                "hp": int(hp_entry.get()),
                "stats": stats,
                "inventory": [],
                "equipment": {},
                "image": None,
                "species": species_var.get(),
                "alignment": alignment_var.get(),
                "class": class_var.get(),
                "subclass": subclass_entry.get(),
                "level": level_entry.get(),
                "multiclass": is_multiclass.get(),
                "second_class": second_class_var.get() if is_multiclass.get() else None,
                "second_subclass": second_subclass_entry.get() if is_multiclass.get() else None,
                "second_level": second_level_entry.get() if is_multiclass.get() else None
            }
            self.characters.append(character)
            popup.destroy()

        tk.Button(popup, text="Save Character", command=save).pack(pady=10)

    def view_characters(self):
         view_window = tk.Toplevel(self.root)
         view_window.title("Existing Characters")

         for i, char in enumerate(self.characters): tk.Button(view_window, text= char['name'], command=lambda i=i: self.open_character_sheet(i)).pack(pady=2)

    def open_character_sheet(self, index):
        character = self.characters[index]
        sheet = tk.Toplevel(self.root)
        sheet.title(f"{character['name']}'s Sheet")


        info_text = f"""
Species: {character.get('species', 'N/A')}
Alignment: {character.get('alignment', 'N/A')}
Class: {character.get('class', 'N/A')} (Lvl {character.get('level', '?')}) - {character.get('subclass', '')}
"""
        if character.get("multiclass"):
            info_text += f"Multiclass: {character.get('second_class', 'N/A')} (Lvl {character.get('second_level', '?')}) - {character.get('second_subclass', '')}"
        tk.Label(sheet, text=info_text.strip(), justify="left").pack(pady=(5, 10))

        hp_frame = tk.Frame(sheet)
        hp_frame.pack()
        hp_label = tk.Label(hp_frame, text=f"HP: {character['hp']}", font=("Rage Italic", 40))
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
        image_label = tk.Label(img_frame)
        image_label.pack()

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