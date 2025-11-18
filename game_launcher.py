import tkinter as tk
from tkinter import ttk
import ninja_adventure
import os

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ninja Adventure Launcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#1E1E2E')
        
        # Style moderne
        self.setup_style()
        
        # Interface principale
        title = tk.Label(self.root,
            text="NINJA ADVENTURE",
            font=('Helvetica', 36, 'bold'),
            fg='#89B4FA',
            bg='#1E1E2E'
        )
        title.pack(pady=50)
        
        # Boutons
        self.create_buttons()
        
        self.root.mainloop()
    
    def setup_style(self):
        style = ttk.Style()
        style.configure("Custom.TButton",
            font=('Helvetica', 14),
            padding=20,
            background='#89B4FA'
        )
    
    def create_buttons(self):
        buttons_frame = tk.Frame(self.root, bg='#1E1E2E')
        buttons_frame.pack(pady=20)
        
        # Bouton Play
        play_btn = tk.Button(buttons_frame,
            text="JOUER",
            font=('Helvetica', 16, 'bold'),
            bg='#89B4FA',
            fg='#1E1E2E',
            width=20,
            height=2,
            command=self.launch_game
        )
        play_btn.pack(pady=10)
        
        # Bouton Quitter
        quit_btn = tk.Button(buttons_frame,
            text="QUITTER",
            font=('Helvetica', 16),
            bg='#2D2D44',
            fg='#89B4FA',
            width=20,
            height=2,
            command=self.root.quit
        )
        quit_btn.pack(pady=10)
    
    def launch_game(self):
        self.root.withdraw()  # Cache la fenêtre du launcher
        game = ninja_adventure.GameInterface()
        game.root.protocol("WM_DELETE_WINDOW", self.on_game_close)
    
    def on_game_close(self):
        self.root.deiconify()  # Réaffiche le launcher

if __name__ == "__main__":
    launcher = GameLauncher()
