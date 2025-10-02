import customtkinter
import random
import string
import pyperclip
import math


customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")  

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        
        self.title("🔐 Password Generator")
        self.geometry("500x550")
        self.resizable(False, False)

       
        self.frame = customtkinter.CTkFrame(self, corner_radius=20)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.grid_columnconfigure(0, weight=1)

        
        self.title_label = customtkinter.CTkLabel(
            self.frame, text="Password Generator",
            font=customtkinter.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color="#00ffcc"
        )
        self.title_label.grid(row=0, column=0, pady=(20, 5), sticky="n")

        self.subtitle = customtkinter.CTkLabel(
            self.frame, text="Designed for humans, feared by hackers.",
            font=customtkinter.CTkFont(size=14), text_color="#cccccc"
        )
        self.subtitle.grid(row=1, column=0, pady=(0, 20), sticky="n")

        
        length_frame = customtkinter.CTkFrame(self.frame, corner_radius=15)
        length_frame.grid(row=2, column=0, pady=10, padx=15, sticky="ew")
        length_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(length_frame, text="Length:", font=("Arial", 14)).grid(row=0, column=0, padx=(10, 0), pady=15, sticky="w")
        self.length_slider = customtkinter.CTkSlider(length_frame, from_=8, to=32, number_of_steps=24,
                                                     command=self.update_length_label, progress_color="#00ffcc")
        self.length_slider.set(16)
        self.length_slider.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        
        self.length_value_label = customtkinter.CTkLabel(length_frame, text="16", font=("Arial", 14, "bold"))
        self.length_value_label.grid(row=0, column=2, padx=(0, 10), pady=15, sticky="e")

        
        options_frame = customtkinter.CTkFrame(self.frame, corner_radius=15)
        options_frame.grid(row=3, column=0, pady=15, padx=15, sticky="ew")
        options_frame.grid_columnconfigure((0, 1), weight=1)

        self.uppercase_var = customtkinter.StringVar(value="on")
        self.lowercase_var = customtkinter.StringVar(value="on")
        self.digits_var = customtkinter.StringVar(value="on")
        self.symbols_var = customtkinter.StringVar(value="off")

        self.add_checkbox(options_frame, "Uppercase (A-Z)", self.uppercase_var, 0, 0)
        self.add_checkbox(options_frame, "Lowercase (a-z)", self.lowercase_var, 0, 1)
        self.add_checkbox(options_frame, "Numbers (0-9)", self.digits_var, 1, 0)
        self.add_checkbox(options_frame, "Symbols (!@#$)", self.symbols_var, 1, 1)

        
        self.strength_label = customtkinter.CTkLabel(self.frame, text="Password Strength", font=("Arial", 14, "bold"))
        self.strength_label.grid(row=4, column=0, pady=(15, 5), sticky="w", padx=15)
        
        self.strength_bar = customtkinter.CTkProgressBar(self.frame, height=12, corner_radius=8)
        self.strength_bar.grid(row=5, column=0, padx=15, sticky="ew")
        self.strength_bar.set(0)

        self.strength_text_label = customtkinter.CTkLabel(self.frame, text="Very Weak", font=("Arial", 12, "bold"))
        self.strength_text_label.grid(row=6, column=0, pady=(5, 15), padx=15, sticky="w")

        
        self.password_frame = customtkinter.CTkFrame(self.frame, corner_radius=15, fg_color="transparent")
        self.password_frame.grid(row=7, column=0, padx=15, sticky="ew")
        self.password_frame.grid_columnconfigure(0, weight=1)
        
        self.password_entry = customtkinter.CTkEntry(
            self.password_frame, placeholder_text="Click Generate to create a password",
            font=("Consolas", 14), corner_radius=15, justify="center", state="readonly"
        )
        self.password_entry.grid(row=0, column=0, sticky="ew")
        
        self.show_hide_button = customtkinter.CTkButton(
            self.password_frame, text="🙈", width=40, command=self.toggle_password_visibility,
            fg_color="#3399ff", hover_color="#2673b8", font=("Segoe UI", 16, "bold")
        )
        self.show_hide_button.grid(row=0, column=1, padx=(5, 0))
        self.is_password_visible = False

        
        button_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        button_frame.grid(row=8, column=0, pady=15, sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.generate_button = customtkinter.CTkButton(
            button_frame, text="🎲 Generate", command=self.generate_password,
            fg_color="#00cc99", hover_color="#009973", corner_radius=15
        )
        self.generate_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.copy_button = customtkinter.CTkButton(
            button_frame, text="📋 Copy", command=self.copy_password,
            fg_color="#3399ff", hover_color="#2673b8", corner_radius=15, state="disabled"
        )
        self.copy_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.update_strength()

    def add_checkbox(self, frame, text, var, row, col):
        checkbox = customtkinter.CTkCheckBox(frame, text=text, variable=var, onvalue="on", offvalue="off",
                                             font=("Arial", 12), command=self.update_strength)
        checkbox.grid(row=row, column=col, sticky="w", padx=15, pady=8)

    def update_length_label(self, value):
        self.length_value_label.configure(text=str(int(value)))
        self.update_strength()

    def update_strength(self):
        length = int(self.length_slider.get())
        
        pool_size = 0
        if self.uppercase_var.get() == "on": pool_size += 26
        if self.lowercase_var.get() == "on": pool_size += 26
        if self.digits_var.get() == "on": pool_size += 10
        if self.symbols_var.get() == "on": pool_size += 33 
        
        if pool_size == 0 or length == 0:
            entropy = 0
        else:
            entropy = length * math.log2(pool_size)
        
        
        if entropy < 40:
            strength_level = "Easy"
            score = entropy / 40 * 0.25
            color = "red"
        elif entropy < 60:
            strength_level = "Medium"
            score = 0.25 + (entropy - 40) / 20 * 0.25
            color = "orange"
        elif entropy < 80:
            strength_level = "Hard"
            score = 0.5 + (entropy - 60) / 20 * 0.25
            color = "green"
        else:
            strength_level = "Very Hard"
            score = 0.75 + (entropy - 80) / 20 * 0.25
            score = min(score, 1.0)
            color = "#00ff99"

        self.strength_bar.set(score)
        self.strength_bar.configure(progress_color=color)
        self.strength_text_label.configure(text=strength_level, text_color=color)

    def generate_password(self):
        self.is_password_visible = True
        self.show_hide_button.configure(text="🙈")
        
        length = int(self.length_slider.get())
        characters = ""
        if self.uppercase_var.get() == "on": characters += string.ascii_uppercase
        if self.lowercase_var.get() == "on": characters += string.ascii_lowercase
        if self.digits_var.get() == "on": characters += string.digits
        if self.symbols_var.get() == "on": characters += string.punctuation

        if not characters:
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, "Select at least one type!")
            self.password_entry.configure(state="readonly")
            self.copy_button.configure(state="disabled")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.configure(state="normal")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.password_entry.configure(state="readonly")
        self.copy_button.configure(state="normal")

    def toggle_password_visibility(self):
        self.is_password_visible = not self.is_password_visible
        if self.is_password_visible:
            self.show_hide_button.configure(text="")
            self.password_entry.configure(show="")
        else:
            self.show_hide_button.configure(text="👁️")
            self.password_entry.configure(show="*")

    def copy_password(self):
        password = self.password_entry.get()
        if password and password not in ["Select at least one type!", "Copied!"]:
            pyperclip.copy(password)
            self.password_entry.configure(state="normal")
            self.password_entry.delete(0, "end")
            self.password_entry.insert(0, "Copied!")
            self.password_entry.configure(state="readonly")
            self.after(1500, self.generate_password)

if __name__ == "__main__":
    app = App()
    app.mainloop()