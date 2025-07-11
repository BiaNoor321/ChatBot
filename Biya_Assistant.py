from threading import Thread
import tkinter as tk
from tkinter import ttk, messagebox
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ========== Constants ==========

APP_TITLE = "🤖Assistant Developed by Bia Noor"
WINDOW_SIZE = "900x750"

# ========== Themes ==========

THEMES = {
    "dark": {
        "bg": "#121212",
        "input_bg": "#1E1E1E",
        "text": "#E0E0E0",
        "btn": "#2979FF",
        "btn_hover": "#5393FF",
        "log_bg": "#1A1A1A",
    },
    "light": {
        "bg": "#FFFFFF",
        "input_bg": "#F0F0F0",
        "text": "#000000",
        "btn": "#0066CC",
        "btn_hover": "#3385FF",
        "log_bg": "#E6E6E6",
    }
}
current_theme = "dark"

theme = THEMES[current_theme]
BG_COLOR = theme["bg"]
INPUT_BG = theme["input_bg"]
TEXT_COLOR = theme["text"]
BTN_COLOR = theme["btn"]
BTN_HOVER = theme["btn_hover"]
LOG_BG = theme["log_bg"]

# Fonts
FONT_BIA = ("Arial", 24, "bold")
FONT_SUB = ("Segoe UI", 18, "bold")
FONT_MAIN = ("Segoe UI", 14)
FONT_LOG = ("Courier New", 12, "bold")

# Valid student IDs (001 to 092)
VALID_IDS = [f"{i:03}" for i in range(1, 93)]

# ========== Functions ==========
def on_enter(e):
    generate_btn.config(bg=BTN_HOVER)

def on_leave(e):
    generate_btn.config(bg=BTN_COLOR)

def validate_student_id(sid):
    return sid in VALID_IDS

def log_message(message):
    log_output.config(state=tk.NORMAL)
    log_output.insert(tk.END, message + "\n")
    log_output.see(tk.END)
    log_output.config(state=tk.DISABLED)

def call_gemini_api(student_id, question):
    try:
        prompt = f"Student ID: {student_id}. Question: {question}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"
    
def threaded_response(student_id, question):
    log_message("⏳ Please wait... generating response...\n")
    response = call_gemini_api(student_id, question)
    log_message(f"✅ Response:\n{response}")

def generate_script():
    student_id = student_id_entry.get().strip()
    question = question_input.get("1.0", tk.END).strip()

    if not validate_student_id(student_id):
        messagebox.showerror("Invalid ID", "Student ID must be between 0001 and 0092.")
        return

    if not question:
        messagebox.showerror("Missing Question", "Please enter your question.")
        return

    log_message(f"🎓 Asking for student ID {student_id}...\n {question}")
    Thread(target=threaded_response, args=(student_id, question)).start()


def export_log():
    log = log_output.get("1.0", tk.END).strip()
    if log:
        with open("conversation_log.txt", "w", encoding="utf-8") as f:
            f.write(log)
        messagebox.showinfo("Exported", "Conversation log saved as 'conversation_log.txt'.")
    else:
        messagebox.showinfo("Empty", "No conversation to export.")

def toggle_theme():
    global current_theme, BG_COLOR, INPUT_BG, TEXT_COLOR, BTN_COLOR, BTN_HOVER, LOG_BG

    # Switch theme
    current_theme = "light" if current_theme == "dark" else "dark"
    theme = THEMES[current_theme]

    # Update theme variables
    BG_COLOR = theme["bg"]
    INPUT_BG = theme["input_bg"]
    TEXT_COLOR = theme["text"]
    BTN_COLOR = theme["btn"]
    BTN_HOVER = theme["btn_hover"]
    LOG_BG = theme["log_bg"]

    # Update backgrounds
    app.configure(bg=BG_COLOR)
    main_frame.configure(bg=BG_COLOR)
    title_frame.configure(bg=BG_COLOR)

    # Update title labels
    title_text.configure(bg=BG_COLOR, fg=TEXT_COLOR)
    name_label.configure(bg=BG_COLOR, fg="#2979FF")

    # Update all main_frame widgets
    for widget in main_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=BG_COLOR, fg=TEXT_COLOR)
        elif isinstance(widget, (tk.Entry, tk.Text)):
            widget.configure(bg=INPUT_BG, fg=TEXT_COLOR)

    log_output.configure(bg=LOG_BG, fg=TEXT_COLOR)

    # Update button styles
    style.configure("Rounded.TButton",
                    foreground="white",
                    background=BTN_COLOR,
                    borderwidth=0,
                    padding=10)
    style.map("Rounded.TButton",
              background=[("active", BTN_HOVER)])


# ========== GUI Setup ==========
app = tk.Tk()
app.title(APP_TITLE)
app.geometry(WINDOW_SIZE)
app.configure(bg=BG_COLOR)
style = ttk.Style()
style.theme_use("clam")
# Title section
title_frame = tk.Frame(app, bg=BG_COLOR)
title_frame.pack(pady=(10, 0))

title_text = tk.Label(title_frame, text="🤖 Assistant developed by ", font=FONT_BIA, fg=TEXT_COLOR, bg=BG_COLOR)
title_text.pack(side=tk.LEFT)

name_label = tk.Label(title_frame, text="Bia Noor", font=FONT_BIA, fg="#2979FF", bg=BG_COLOR)
name_label.pack(side=tk.LEFT)

# --- Main Frame ---
main_frame = tk.Frame(app, bg=BG_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True)

# --- ID input ---
tk.Label(main_frame, text="🆔Enter Student ID (001 to 0092): ", font=FONT_MAIN, bg=BG_COLOR).pack(anchor="w")
student_id_entry = tk.Entry(main_frame, font=FONT_MAIN, bg=INPUT_BG, fg=TEXT_COLOR)
student_id_entry.pack(anchor="w")

# --- Question input ---
tk.Label(main_frame, text="🔍 Ask or Enter your question:", font=FONT_MAIN, bg=BG_COLOR).pack(anchor="w", padx=40)
question_input = tk.Text(main_frame, height=6, font=FONT_MAIN, bg=INPUT_BG, fg=TEXT_COLOR)
question_input.pack(fill=tk.X, padx=40, pady=(0, 20))

# --- Send button ---
style.configure("Rounded.TButton",
                foreground="white",
                background=BTN_COLOR,
                borderwidth=0,
                padding=10)
style.map("Rounded.TButton",
          background=[("active", BTN_HOVER)])

generate_btn = ttk.Button(main_frame, text="🚀Send", style="Rounded.TButton", command=generate_script)
generate_btn.pack(pady=(0, 20))

toggle_btn = ttk.Button(main_frame, text="🌓 Toggle Theme", style="Rounded.TButton", command=toggle_theme)
toggle_btn.pack(pady=(0, 10))


# --- Export button ---
export_btn = ttk.Button(main_frame, text="📤Export Log", style="Rounded.TButton", command=export_log)
export_btn.pack(pady=(0, 10))

# --- Log section ---
tk.Label(main_frame, text="💬Conversation Log:", font=("Comic Sans MS", 14, "bold"),
         bg=BG_COLOR).pack(anchor="w", padx=40)
log_output = tk.Text(main_frame, height=12, font=FONT_LOG,
                     bg=LOG_BG, fg=TEXT_COLOR,
                     state=tk.DISABLED, wrap=tk.WORD)
log_output.pack(fill=tk.BOTH, padx=40, pady=(5, 20),expand=True)

app.mainloop()