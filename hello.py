import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class GameHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Center")
        self.root.geometry("1024x768")
        self.root.configure(bg='#1a1a2e')
        
        # Création du notebook (système d'onglets)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Style personnalisé pour les onglets
        style = ttk.Style()
        style.configure("Custom.TNotebook", background='#1a1a2e', padding=5)
        style.configure("Custom.TNotebook.Tab", background='#16213e', foreground='#00fff5', padding=[20, 10])
        style.map("Custom.TNotebook.Tab",
                 background=[("selected", "#0f3460")],
                 foreground=[("selected", "#ffffff")])
        self.notebook.configure(style="Custom.TNotebook")
        
        # Création des différents onglets
        self.quiz_frame = ttk.Frame(self.notebook)
        self.game_frame = ttk.Frame(self.notebook)
        self.options_frame = ttk.Frame(self.notebook)
        
        # Ajout des onglets au notebook
        self.notebook.add(self.quiz_frame, text="📝 Quiz Game", padding=10)
        self.notebook.add(self.game_frame, text="🎮 Course Game", padding=10)
        self.notebook.add(self.options_frame, text="⚙️ Options", padding=10)
        
        # Ajouter un style moderne
        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TNotebook": {
                "configure": {"background": "#1E1E2E", "tabmargins": [2, 5, 2, 0]}
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [20, 10],
                    "background": "#2D2D44",
                    "foreground": "#89B4FA"
                },
                "map": {
                    "background": [("selected", "#89B4FA")],
                    "foreground": [("selected", "#1E1E2E")]
                }
            }
        })
        style.theme_use("modern")
        
        # Configuration des onglets
        self.setup_quiz_tab()
        self.setup_game_tab()
        self.setup_options_tab()

    def setup_quiz_tab(self):
        quiz_content = tk.Frame(self.quiz_frame, bg='#1a1a2e')
        quiz_content.pack(fill='both', expand=True)
        
        # Titre du Quiz
        tk.Label(quiz_content,
            text="QUIZ MASTER",
            font=('Helvetica', 36, 'bold'),
            bg='#1a1a2e',
            fg='#00fff5'
        ).pack(pady=20)
        
        # Bouton pour lancer le quiz
        tk.Button(quiz_content,
            text="Commencer le Quiz",
            font=('Helvetica', 18),
            bg='#16213e',
            fg='#00fff5',
            command=self.start_quiz,
            width=20,
            height=2
        ).pack(pady=30)

    def setup_game_tab(self):
        game_content = tk.Frame(self.game_frame, bg='#1E1E2E')
        game_content.pack(fill='both', expand=True)
        
        # Logo du jeu
        logo_label = tk.Label(game_content,
            text="🏃 NINJA RUN",
            font=('Helvetica', 48, 'bold'),
            bg='#1E1E2E',
            fg='#89B4FA'
        )
        logo_label.pack(pady=30)
        
        # Conteneur pour les boutons
        buttons_frame = tk.Frame(game_content, bg='#1E1E2E')
        buttons_frame.pack(pady=20)
        
        # Boutons avec effets hover
        buttons = [
            ("Nouvelle Partie", self.start_game),
            ("Meilleurs Scores", lambda: self.show_scores()),
            ("Tutoriel", lambda: self.show_tutorial())
        ]
        
        for text, command in buttons:
            btn = tk.Button(buttons_frame,
                text=text,
                font=('Helvetica', 16),
                bg='#2D2D44',
                fg='#89B4FA',
                activebackground='#89B4FA',
                activeforeground='#1E1E2E',
                width=20,
                height=2,
                command=command,
                relief='flat',
                bd=0
            )
            btn.pack(pady=10)
            self.add_hover_effect(btn)

    def setup_options_tab(self):
        options_content = tk.Frame(self.options_frame, bg='#1a1a2e')
        options_content.pack(fill='both', expand=True)
        
        # Options du jeu
        tk.Label(options_content,
            text="OPTIONS",
            font=('Helvetica', 36, 'bold'),
            bg='#1a1a2e',
            fg='#00fff5'
        ).pack(pady=20)
        
        # Contrôles audio
        audio_frame = tk.LabelFrame(options_content, 
            text="Audio",
            font=('Helvetica', 16),
            bg='#1a1a2e',
            fg='#00fff5'
        )
        audio_frame.pack(pady=20, padx=20, fill='x')
        
        # Volume de la musique
        tk.Label(audio_frame,
            text="Volume Musique",
            bg='#1a1a2e',
            fg='#00fff5'
        ).pack(pady=5)
        
        music_slider = ttk.Scale(audio_frame,
            from_=0, to=100,
            orient='horizontal',
            command=lambda v: self.update_music_volume(float(v)/100)
        )
        music_slider.set(50)
        music_slider.pack(pady=5, padx=20, fill='x')
        
        # Volume des effets
        tk.Label(audio_frame,
            text="Volume Effets",
            bg='#1a1a2e',
            fg='#00fff5'
        ).pack(pady=5)
        
        effects_slider = ttk.Scale(audio_frame,
            from_=0, to=100,
            orient='horizontal',
            command=lambda v: self.update_effects_volume(float(v)/100)
        )
        effects_slider.set(40)
        effects_slider.pack(pady=5, padx=20, fill='x')

    def add_hover_effect(self, button):
        def on_enter(e):
            button['background'] = '#89B4FA'
            button['foreground'] = '#1E1E2E'
        def on_leave(e):
            button['background'] = '#2D2D44'
            button['foreground'] = '#89B4FA'
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def show_scores(self):
        scores_window = tk.Toplevel(self.root)
        scores_window.title("Meilleurs Scores")
        scores_window.geometry("400x500")
        scores_window.configure(bg='#1E1E2E')
        # ...rest of scores display code...

    def show_tutorial(self):
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Comment Jouer")
        tutorial_window.geometry("600x400")
        tutorial_window.configure(bg='#1E1E2E')
        # ...rest of tutorial code...

    def start_quiz(self):
        # Lancer le quiz existant
        QuizGameDeluxe(tk.Toplevel(self.root))

    def start_game(self):
        # Créer une nouvelle fenêtre pour le jeu
        game_window = tk.Toplevel(self.root)
        game_window.geometry("1024x600")
        game_window.title("Ninja Run")
        import course_game
        course_game.RealisticGame(game_window)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = GameHub(root)
    root.mainloop()
