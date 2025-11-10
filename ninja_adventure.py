import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import random
import os

class GameInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ninja Adventure - Lionel")
        self.root.geometry("1280x720")
        self.root.configure(bg='#1E1E2E')

        # Création du système d'onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Style des onglets
        style = ttk.Style()
        style.configure("Custom.TNotebook",
            background='#1E1E2E',
            foreground='#89B4FA',
            padding=5
        )
        style.configure("Custom.TNotebook.Tab",
            background='#2D2D44',
            foreground='#89B4FA',
            padding=[20, 10],
            font=('Helvetica', 12, 'bold')
        )
        self.notebook.configure(style="Custom.TNotebook")

        # Création des onglets
        self.game_tab = ttk.Frame(self.notebook)
        self.scores_tab = ttk.Frame(self.notebook)
        self.options_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.game_tab, text="🎮 Jeu")
        self.notebook.add(self.scores_tab, text="🏆 Scores")
        self.notebook.add(self.options_tab, text="⚙️ Options")

        # Configuration des onglets
        self.setup_game_tab()
        self.setup_scores_tab()
        self.setup_options_tab()

    def setup_game_tab(self):
        # Frame du jeu
        game_frame = ttk.Frame(self.game_tab)
        game_frame.pack(expand=True, fill='both')

        # Lancement du jeu dans le frame
        self.game = NinjaAdventure(game_frame)

    def setup_scores_tab(self):
        scores_frame = ttk.Frame(self.scores_tab)
        scores_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Label(scores_frame,
            text="Meilleurs Scores",
            font=('Helvetica', 24, 'bold')
        ).pack(pady=20)

        # Liste des scores
        self.scores_list = tk.Listbox(scores_frame,
            font=('Helvetica', 14),
            height=10,
            width=40,
            bg='#2D2D44',
            fg='#89B4FA'
        )
        self.scores_list.pack(pady=10)

    def setup_options_tab(self):
        options_frame = ttk.Frame(self.options_tab)
        options_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Contrôles audio
        ttk.Label(options_frame,
            text="Volume",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=10)

        # Slider pour la musique
        ttk.Scale(options_frame,
            from_=0,
            to=100,
            orient='horizontal'
        ).pack(fill='x', padx=50, pady=10)

class NinjaAdventure:
    def __init__(self, parent):
        self.parent = parent
        # Création du canvas de jeu
        self.canvas = tk.Canvas(
            parent,
            width=1280,
            height=600,
            bg='#1E1E2E',
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill='both')

        # Configuration de la fenêtre principale
        self.root = tk.Toplevel()
        self.root.title("Ninja Adventure")
        self.root.geometry("1280x720")
        
        # Initialisation audio
        pygame.mixer.init()
        self.load_audio()
        
        # Chargement des ressources
        self.load_resources()
        
        # Configuration du jeu
        self.game_speed = 5
        self.score = 0
        self.distance = 0
        self.is_jumping = False
        self.is_attacking = False
        self.has_shield = False
        
        # Configuration des personnages disponibles
        self.characters = {
            "ninja": {
                "sprites": self.ninja_sprites,
                "speed": 8,
                "jump_power": -20,
                "attack_power": 10
            },
            "samurai": {
                "sprites": self.samurai_sprites,
                "speed": 6,
                "jump_power": -18,
                "attack_power": 15
            },
            "monk": {
                "sprites": self.monk_sprites,
                "speed": 7,
                "jump_power": -22,
                "attack_power": 8
            }
        }
        
        # Monstres et obstacles
        self.monsters = []
        self.monster_types = [
            {"name": "oni", "speed": 3, "damage": 20, "health": 30},
            {"name": "ghost", "speed": 5, "damage": 10, "health": 15},
            {"name": "demon", "speed": 4, "damage": 15, "health": 25}
        ]
        
        # Effets visuels
        self.particles = []
        self.effects = []
        
        # Configuration des animations du ninja Lionel
        self.ninja_animations = {
            "idle": {
                "frames": ["lionel_idle1.png", "lionel_idle2.png", "lionel_idle3.png"],
                "speed": 0.15
            },
            "run": {
                "frames": ["lionel_run1.png", "lionel_run2.png", "lionel_run3.png", "lionel_run4.png"],
                "speed": 0.12
            },
            "jump": {
                "frames": ["lionel_jump1.png", "lionel_jump2.png", "lionel_jump3.png"],
                "speed": 0.2
            },
            "attack": {
                "frames": ["lionel_attack1.png", "lionel_attack2.png", "lionel_attack3.png"],
                "speed": 0.1
            },
            "slide": {
                "frames": ["lionel_slide1.png", "lionel_slide2.png"],
                "speed": 0.15
            },
            "dash": {
                "frames": ["lionel_dash1.png", "lionel_dash2.png", "lionel_dash3.png"],
                "speed": 0.08
            },
            "special": {
                "frames": ["lionel_special1.png", "lionel_special2.png", "lionel_special3.png"],
                "speed": 0.1
            }
        }
        
        # État actuel de l'animation
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Capacités spéciales de Lionel
        self.special_moves = {
            "dragon_dash": {
                "cooldown": 5000,
                "damage": 25,
                "effect": self.create_dragon_effect
            },
            "shadow_clone": {
                "cooldown": 8000,
                "duration": 3000,
                "effect": self.create_clone_effect
            }
        }
        
        # Démarrage du jeu
        self.show_character_select()
        self.root.mainloop()

    def load_audio(self):
        # Musique de fond
        pygame.mixer.music.load("assets/music/theme.mp3")
        pygame.mixer.music.set_volume(0.5)
        
        # Effets sonores
        self.sounds = {
            "jump": pygame.mixer.Sound("assets/sounds/jump.wav"),
            "attack": pygame.mixer.Sound("assets/sounds/attack.wav"),
            "hit": pygame.mixer.Sound("assets/sounds/hit.wav"),
            "powerup": pygame.mixer.Sound("assets/sounds/powerup.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav")
        }

    def load_resources(self):
        # Chargement des images pour chaque personnage
        self.ninja_sprites = self.load_character_sprites("ninja")
        self.samurai_sprites = self.load_character_sprites("samurai")
        self.monk_sprites = self.load_character_sprites("monk")
        
        # Chargement des monstres
        self.monster_sprites = self.load_monster_sprites()
        
        # Chargement des décors parallax
        self.backgrounds = self.load_background_layers()
        
        # Chargement des effets visuels
        self.effect_sprites = self.load_effect_sprites()

    def create_particle_effect(self, x, y, color, count=10):
        for _ in range(count):
            particle = {
                "x": x,
                "y": y,
                "dx": random.uniform(-3, 3),
                "dy": random.uniform(-8, 0),
                "life": random.randint(10, 30),
                "color": color,
                "alpha": 1.0
            }
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["dy"] += 0.5  # Gravité
            particle["life"] -= 1
            particle["alpha"] -= 0.03
            
            if particle["life"] <= 0:
                self.particles.remove(particle)

    def spawn_monster(self):
        monster_type = random.choice(self.monster_types)
        monster = {
            "type": monster_type,
            "x": 1280,
            "y": 500,
            "health": monster_type["health"],
            "state": "running",
            "frame": 0
        }
        self.monsters.append(monster)

    def update_animation(self):
        # Met à jour l'animation courante
        animation = self.ninja_animations[self.current_animation]
        self.animation_timer += 1
        
        if self.animation_timer >= animation["speed"] * 60:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(animation["frames"])
            
            # Mise à jour du sprite
            current_frame = animation["frames"][self.animation_frame]
            self.player_sprite = self.load_image(f"assets/sprites/lionel/{current_frame}")
            
            # Effets spéciaux selon l'animation
            if self.current_animation == "dash":
                self.create_dash_trail()
            elif self.current_animation == "special":
                self.create_special_effect()

    def create_dash_trail(self):
        # Effet de traînée pour le dash
        x, y = self.player_pos
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
        
        for i in range(3):
            self.create_particle_effect(
                x - i * 20,
                y,
                random.choice(colors),
                count=5
            )

    def create_dragon_effect(self):
        # Animation de l'attaque dragon
        x, y = self.player_pos
        dragon_frames = self.load_effect_sprites("dragon")
        
        def animate_dragon(frame=0):
            if frame < len(dragon_frames):
                self.canvas.create_image(x + 50, y, image=dragon_frames[frame])
                self.root.after(50, lambda: animate_dragon(frame + 1))
        
        animate_dragon()

    def create_clone_effect(self):
        # Création de clones d'ombre
        x, y = self.player_pos
        clone_pos = [(x - 30, y), (x + 30, y)]
        
        for cx, cy in clone_pos:
            clone = {
                "x": cx,
                "y": cy,
                "alpha": 0.7,
                "life": 60
            }
            self.effects.append(clone)

    def update_game(self):
        # Mise à jour du parallax
        self.update_background()
        
        # Mise à jour des monstres
        self.update_monsters()
        
        # Mise à jour des particules
        self.update_particles()
        
        # Mise à jour du score
        self.distance += self.game_speed
        self.score = self.distance // 100
        
        # Augmentation progressive de la difficulté
        if self.score % 100 == 0:
            self.game_speed += 0.5
        
        # Spawn de nouveaux monstres
        if random.random() < 0.02:
            self.spawn_monster()
        
        # Mise à jour des animations
        self.update_animation()
        
        # Mise à jour des effets spéciaux
        self.update_effects()
        
        self.canvas.after(16, self.update_game)

    def handle_collision(self, monster):
        if not self.has_shield:
            self.play_sound("hit")
            self.create_particle_effect(monster["x"], monster["y"], "red", 20)
            self.game_over()
        else:
            self.has_shield = False
            self.monsters.remove(monster)

    def game_over(self):
        self.play_sound("death")
        # Affichage du score et menu de redémarrage
        # ...existing game over code...

# Point d'entrée
if __name__ == "__main__":
    app = GameInterface()
    app.root.mainloop()
