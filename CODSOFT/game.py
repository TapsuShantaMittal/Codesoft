import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont, UnidentifiedImageError
import random, os

BASE_PATH = r"C:\Users\Sitaram\OneDrive\Desktop\CODEING\CODSOFT"
IMG_SIZE = (120, 120)

choices = ['rock', 'paper', 'scissors']
score_user = 0
score_com = 0


def create_placeholder(text, size=IMG_SIZE, bg=(180, 200, 230, 255)):
    """Create a simple placeholder image with centered text."""
    img = Image.new("RGBA", size, bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=(0, 0, 0), font=font)
    return img

def load_image_safe(base, name, size=IMG_SIZE):
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(base, name + ext)
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except (UnidentifiedImageError, OSError) as e:
                print(f"[WARN] Could not open {path}: {e}")
    print(f"[INFO] Using placeholder for {name}")
    return ImageTk.PhotoImage(create_placeholder(name.capitalize(), size=size))


def determine_winner(user_choice):
    global score_user, score_com
    com_choice = random.choice(choices)

    if user_choice == com_choice:
        result = f"Tie! Both chose {user_choice}."
        color = "#ffcc00"
    elif (user_choice == 'rock' and com_choice == 'scissors') or \
         (user_choice == 'scissors' and com_choice == 'paper') or \
         (user_choice == 'paper' and com_choice == 'rock'):
        result = f"You Win! {user_choice.capitalize()} beats {com_choice.capitalize()}."
        color = "#4CAF50"
        score_user += 1
    else:
        result = f"Computer Wins! {com_choice.capitalize()} beats {user_choice.capitalize()}."
        color = "#e74c3c"
        score_com += 1

    animate_result(result, color)
    user_score_label.config(text=str(score_user))
    com_score_label.config(text=str(score_com))

def animate_result(text, color):
    """Animate result text with color flash."""
    result_label.config(text=text, fg="white", bg=color)
    result_label.after(800, lambda: result_label.config(bg="white", fg="black"))


root = tk.Tk()
root.title("Rock Paper Scissors ✊ ✋ ✌️")
root.geometry("650x550")
root.configure(bg="#dfe9f3")


title = tk.Label(root, text="✨ Rock Paper Scissors Game ✨", font=("Verdana", 20, "bold"), bg="#4682B4", fg="white", pady=10)
title.pack(fill="x")


rock_img = load_image_safe(BASE_PATH, "rock")
paper_img = load_image_safe(BASE_PATH, "paper")
scissors_img = load_image_safe(BASE_PATH, "scissors")


btn_frame = tk.Frame(root, bg="#dfe9f3")
btn_frame.pack(pady=20)

def hover_effect(widget, enter_bg, leave_bg):
    widget.bind("<Enter>", lambda e: widget.config(bg=enter_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=leave_bg))

b1 = tk.Button(btn_frame, image=rock_img, command=lambda: determine_winner('rock'), bg="#ffffff", relief="flat", bd=3)
b1.grid(row=0, column=0, padx=25)
hover_effect(b1, "#cce7ff", "#ffffff")

b2 = tk.Button(btn_frame, image=paper_img, command=lambda: determine_winner('paper'), bg="#ffffff", relief="flat", bd=3)
b2.grid(row=0, column=1, padx=25)
hover_effect(b2, "#cce7ff", "#ffffff")

b3 = tk.Button(btn_frame, image=scissors_img, command=lambda: determine_winner('scissors'), bg="#ffffff", relief="flat", bd=3)
b3.grid(row=0, column=2, padx=25)
hover_effect(b3, "#cce7ff", "#ffffff")


result_label = tk.Label(root, text="Make your move!", font=("Arial", 16, "bold"), bg="white", width=55, height=2, relief="groove")
result_label.pack(pady=20)


score_frame = tk.LabelFrame(root, text="🏆 Scoreboard", font=("Arial", 14, "bold"), bg="#f0f8ff", padx=20, pady=10, bd=3, relief="ridge")
score_frame.pack(pady=10)

tk.Label(score_frame, text="You", font=("Arial", 14, "bold"), bg="#f0f8ff").grid(row=0, column=0, padx=30)
user_score_label = tk.Label(score_frame, text="0", font=("Arial", 18, "bold"), bg="white", fg="#2e8b57", width=5, relief="ridge")
user_score_label.grid(row=1, column=0)

tk.Label(score_frame, text="Computer", font=("Arial", 14, "bold"), bg="#f0f8ff").grid(row=0, column=1, padx=30)
com_score_label = tk.Label(score_frame, text="0", font=("Arial", 18, "bold"), bg="white", fg="#b22222", width=5, relief="ridge")
com_score_label.grid(row=1, column=1)


exit_btn = tk.Button(root, text="Exit Game", font=("Arial", 14, "bold"), bg="#e74c3c", fg="white", width=20, relief="raised", command=root.destroy)
exit_btn.pack(side=tk.BOTTOM, pady=20)
hover_effect(exit_btn, "#ff6b6b", "#e74c3c")

root.mainloop()
