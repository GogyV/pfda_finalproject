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

    
    def save_character(self, name):


    def view_characters(self):
        

if __name__ == "__main__":
    root = tk.Tk()
    app = DungeonDelversCodex(root)
    root.mainloop()