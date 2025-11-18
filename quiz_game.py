import time
import random
import tkinter as tk
from PIL import Image, ImageTk
import os

questions = [
    {"question": "Quelle est la capitale de la France?", "choix": ["Londres", "Paris", "Berlin", "Madrid"], "reponse": "Paris"},
    {"question": "Combien font 2 + 2?", "choix": ["3", "4", "5", "6"], "reponse": "4"},
    {"question": "Quelle est la couleur du ciel?", "choix": ["vert", "bleu", "rouge", "jaune"], "reponse": "bleu"},
    {"question": "Quel est le plus grand océan?", "choix": ["Atlantique", "Indien", "Pacifique", "Arctique"], "reponse": "Pacifique"}
]

def jouer_quiz():
    score = 0
    print("=== JEU DE QUIZ CHRONOMETRE (terminal) ===")
    print("Vous avez 10s par question.")
    for q in random.sample(questions, len(questions)):
        print("\nQuestion:", q["question"])
        debut = time.time()
        try:
            reponse = input("Votre réponse: ").strip().lower()
        except EOFError:
            reponse = ""
        temps = time.time() - debut
        if temps > 10:
            print("Temps écoulé!")
        elif reponse == q["reponse"].lower():
            print("Correct!")
            score += 1
        else:
            print("Incorrect. Réponse:", q["reponse"])
    print(f"\nScore final: {score}/{len(questions)}")

# GUI quiz tab usable inside un Notebook tab or tout Frame parent
class QuizTab:
    def __init__(self, parent, time_per_question=10, banner_image=None):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.time_per_question = time_per_question
        self.questions = random.sample(questions, len(questions))
        self.index = 0
        self.score = 0
        self.timer_id = None
        self.time_left = 0

        # Banner image (optional)
        self.banner_photo = None
        if banner_image and os.path.exists(banner_image):
            try:
                img = Image.open(banner_image)
                # resize to fit (max width 760)
                w, h = img.size
                max_w = 760
                if w > max_w:
                    img = img.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
                self.banner_photo = ImageTk.PhotoImage(img)
                self.banner_label = tk.Label(self.frame, image=self.banner_photo, bg=self.frame.cget("bg"))
                self.banner_label.pack(pady=6)
            except Exception:
                # fail silently and continue without banner
                pass

        # UI
        self.title = tk.Label(self.frame, text="QUIZ CHRONO", font=("Helvetica", 18, "bold"))
        self.title.pack(pady=8)
        self.timer_label = tk.Label(self.frame, text="")
        self.timer_label.pack()
        self.question_label = tk.Label(self.frame, text="", wraplength=600, font=("Helvetica", 14))
        self.question_label.pack(pady=10)
        self.buttons_frame = tk.Frame(self.frame)
        self.buttons_frame.pack(pady=10)
        self.choice_buttons = [tk.Button(self.buttons_frame, text="", width=30, command=lambda i=i: self.select_choice(i)) for i in range(4)]
        for btn in self.choice_buttons:
            btn.pack(pady=4)
        self.status_label = tk.Label(self.frame, text="Score: 0")
        self.status_label.pack(pady=8)
        self.control_frame = tk.Frame(self.frame)
        self.control_frame.pack(pady=6)
        self.start_btn = tk.Button(self.control_frame, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=5)
        self.restart_btn = tk.Button(self.control_frame, text="Restart", command=self.restart)
        self.restart_btn.pack(side="left", padx=5)

        # initially disabled until Start
        self.set_buttons_state("disabled")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)

    def start(self):
        self.start_btn.config(state="disabled")
        self.index = 0
        self.score = 0
        self.status_label.config(text=f"Score: {self.score}")
        self.questions = random.sample(questions, len(questions))
        self.next_question()

    def restart(self):
        if self.timer_id:
            self.frame.after_cancel(self.timer_id)
            self.timer_id = None
        self.start_btn.config(state="normal")
        self.set_buttons_state("disabled")
        self.question_label.config(text="")
        self.timer_label.config(text="")
        self.status_label.config(text="Score: 0")

    def next_question(self):
        if self.index >= len(self.questions):
            self.finish()
            return
        q = self.questions[self.index]
        self.question_label.config(text=q["question"])
        # shuffle choices
        choices = q["choix"].copy()
        random.shuffle(choices)
        self.current_answer = q["reponse"]
        for i, btn in enumerate(self.choice_buttons):
            btn.config(text=choices[i], state="normal")
        self.time_left = self.time_per_question
        self.update_timer()

    def set_buttons_state(self, state):
        for btn in self.choice_buttons:
            btn.config(state=state)

    def update_timer(self):
        self.timer_label.config(text=f"Temps restant: {self.time_left} s")
        if self.time_left <= 0:
            self.set_buttons_state("disabled")
            self.index += 1
            self.frame.after(500, self.next_question)
            return
        self.time_left -= 1
        self.timer_id = self.frame.after(1000, self.update_timer)

    def select_choice(self, idx):
        if self.timer_id:
            self.frame.after_cancel(self.timer_id)
            self.timer_id = None
        choice_text = self.choice_buttons[idx].cget("text")
        if choice_text.lower() == self.current_answer.lower():
            self.score += 1
        # disable buttons, show next after short delay
        self.set_buttons_state("disabled")
        self.status_label.config(text=f"Score: {self.score}")
        self.index += 1
        self.frame.after(500, self.next_question)

    def finish(self):
        self.question_label.config(text=f"Quiz terminé ! Score final: {self.score}/{len(self.questions)}")
        self.timer_label.config(text="")
        self.set_buttons_state("disabled")
        self.start_btn.config(state="normal")

# helper: create a tab/frame inside a Notebook or parent Frame
def create_quiz_tab(parent, time_per_question=10, banner_image=None):
    tab = QuizTab(parent, time_per_question=time_per_question, banner_image=banner_image)
    return tab

if __name__ == "__main__":
    # standalone GUI test
    root = tk.Tk()
    root.title("Quiz - Test GUI")
    # Example: pass path to banner image if available
    banner_path = "assets/images/quiz_banner.png"
    tab = create_quiz_tab(root, banner_image=banner_path if os.path.exists(banner_path) else None)
    tab.pack(fill="both", expand=True, padx=20, pady=20)
    root.mainloop()
