import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Calculator")
app.geometry("400x580")  
app.resizable(False, False)
app.configure(fg_color="#1E1E1E")  

user_input = ctk.StringVar()

entry = ctk.CTkEntry(
    app,
    textvariable=user_input,
    font=("Helvetica", 36, "bold"),  
    justify="right",
    corner_radius=20,
    fg_color="#0A0A0A",  
    border_color="#3A3A3A",  
    border_width=3,
    height=80
)
entry.pack(padx=20, pady=25, fill="x")


def add_to_input(value):
    current = user_input.get()
    if current == "Error":
        user_input.set(value)
    else:
        user_input.set(current + value)

def clear_input():
    user_input.set("")

def calculate_result():
    expression = user_input.get()
    try:
        
        result = eval(expression, {"__builtins__": {}})
        user_input.set(str(result))
    except ZeroDivisionError:
        user_input.set("Error")
    except Exception:
        user_input.set("Error")


def create_button(parent, text, color, hover_color, command, is_operator=False):
    if is_operator:
      
        return ctk.CTkButton(
            parent,
            text=text,
            font=("Helvetica", 28),
            fg_color=color,
            hover_color=hover_color,
            border_color=color,
            border_width=1,
            corner_radius=25,
            height=80,
            command=command
        )
    else:
      
        return ctk.CTkButton(
            parent,
            text=text,
            font=("Helvetica", 28, "bold"),
            fg_color=color,
            hover_color=hover_color,
            border_color="#4A4A4A",
            border_width=1,
            corner_radius=25,
            height=80,
            command=command
        )


frame = ctk.CTkFrame(app, fg_color="transparent")
frame.pack(expand=True, fill="both", padx=15, pady=15)

number_color = "#383838"  
number_hover_color = "#454545"  
operator_color = "#FF9500"  
operator_hover_color = "#E08600"   
clear_color = "#D95750"
clear_hover_color = "#B54640" 
equals_color = "#5AC8FA"  
equals_hover_color = "#4AB8E0"  

buttons = [
    ("7", number_color, number_hover_color, lambda: add_to_input("7")),
    ("8", number_color, number_hover_color, lambda: add_to_input("8")),
    ("9", number_color, number_hover_color, lambda: add_to_input("9")),
    ("÷", operator_color, operator_hover_color, lambda: add_to_input("/"), True),
    ("4", number_color, number_hover_color, lambda: add_to_input("4")),
    ("5", number_color, number_hover_color, lambda: add_to_input("5")),
    ("6", number_color, number_hover_color, lambda: add_to_input("6")),
    ("×", operator_color, operator_hover_color, lambda: add_to_input("*"), True),
    ("1", number_color, number_hover_color, lambda: add_to_input("1")),
    ("2", number_color, number_hover_color, lambda: add_to_input("2")),
    ("3", number_color, number_hover_color, lambda: add_to_input("3")),
    ("-", operator_color, operator_hover_color, lambda: add_to_input("-"), True),
    ("0", number_color, number_hover_color, lambda: add_to_input("0")),
    ("C", clear_color, clear_hover_color, clear_input),
    ("+", operator_color, operator_hover_color, lambda: add_to_input("+"), True),
    ("=", equals_color, equals_hover_color, calculate_result),
]


for i, item in enumerate(buttons):
    text, color, hover_color, cmd = item[:4]
    is_operator = item[4] if len(item) > 4 else False
    btn = create_button(frame, text, color, hover_color, cmd, is_operator)
    btn.grid(row=i//4, column=i%4, padx=10, pady=10, sticky="nsew")

for i in range(4):
    frame.columnconfigure(i, weight=1)
    frame.rowconfigure(i, weight=1)

app.mainloop()