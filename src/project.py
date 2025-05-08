import tkinter as tk
from tkinter import messagebox

class DungeonDelversCodex:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Delver's Codex")
        self.root.geometry("500x400")
        self.title_label = tk.Label(root, text="Dungeon Delver's Codex", font=("Helvetica", 18))
        self.title_label.pack(pady=20)
        self.new_char_button = tk.Button(root, text="Create New Character", width=30, command=self.create_new_character)
        self.new_char_button.pack(pady=5)
        self.view_chars_button = tk.Button(root, text="View Created Characters", width=30, command=self.view_characters)
        self.view_chars_button.pack(pady=5)
        self.exit_button = tk.Button(root, text="Exit", width=30, command=root.quit)
        self.exit_button.pack(pady=20)

        self.characters = []

    def create_new_character(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Create New Character")
        tk.Label(new_window, text="Character Name:").pack()
        name_entry = tk.Entry(new_window)
        name_entry.pack()
        tk.Button(new_window, text="Save", command=lambda: self.save_character(name_entry.get())).pack()

    def save_character(self, name):
        if name:
            self.characters.append({
                "name": name,
                "hp": 10,
                "stats": {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10},
                "inventory": [],
                "equipment": {}
            })
            messagebox.showinfo("Saved", f"Character '{name}' created!")
        else:
            messagebox.showwarning("Missing Name", "Please enter a name for your character.")


    def view_characters(self):
        if not self.characters:
            messagebox.showinfo("No Characters", "No characters have been created yet.")
            return
        
        view_window = tk.Toplevel(self.root)
        view_window.title("Existing Characters")
        for char in self.characters:
            tk.Label(view_window, text=f"{char['name']} - HP: {char['hp']}").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDelversCodex(root)
    root.mainloop()