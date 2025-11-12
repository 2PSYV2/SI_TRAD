import requests # model requests
import tkinter as tk # GUI lib
from tkinter import ttk, messagebox, filedialog
import json
import os, time, ctypes
from dotenv import load_dotenv # enviorment params extracor


# Version + author
VERSION = "V-0.1.1"
AUTHOR = "Yevhenii Edelshteyn Kylymnyk"
# load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Global paths
CONFIG_PATH = "config.json"

default_config = {
    "models": ["deepseek/deepseek-r1-0528:free"],
    "languages": ["Spanish"]
}

# Available default models
MODELS = [
    "deepseek/deepseek-r1-0528:free"
]

SYSTEM_ROLE = [
    "You are a translation assistant. Provide exclusively the translation of the requested text"
]

# API requesst URL
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load or create config
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(default_config,f,indent=4)
        return default_config

def save_config():
    cfg = {"models":MODELS, "languages": LANGUAGES}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)

# Call model by promt and model
def call_model(prompt, model):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages":[
            {"role": "system", "content": SYSTEM_ROLE[0]},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(API_URL, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        elif r.status_code == 402:
            return "[ERROR] Insufficient credits. Try a free model or add funds."
        elif r.status_code == 429:
            return "[ERROR] Request limit reached, try again later."
        else:
            return f"[ERROR] {r.status_code}: {r.text}"
    except Exception as e:
        return f"[ERROR] {e}"

def translate():
    prompt = input_text.get("1.0", tk.END).strip()
    model = model_var.get()
    target_lang = lang_var.get()
    if not prompt:
        messagebox.showwarning("Warning","Introduce some text first.")
        return
    log_text.insert(tk.END, f"Using model: {model}\n")
    log_text.insert(tk.END, f"Target language: {target_lang}\n")
    log_text.insert(tk.END, "Processing; please wait...\n")
    root.update_idletasks()

    full_prompt = f"Translade the following text to {target_lang}:\n\n{prompt}"
    start = time.time()
    result = call_model(prompt=full_prompt, model=model)
    finish = time.time()

    output_text.delete("1.0",tk.END)
    output_text.insert(tk.END, result+"\n")
    log_text.insert(tk.END,f"Task completed in {finish-start:.2f}s\n\n")

def add_new_model():
    win = tk.Toplevel(root)
    win.title("Add new model")
    win.geometry("400x150")
    win.resizable(False, False)
    win.grab_set()
    tk.Label(win, text="Enter new model link:").pack(pady=10)
    entry=tk.Entry(win, width=50)
    entry.pack(pady=5)

    def save():
        new = entry.get().strip()
        if new and new not in MODELS:
            MODELS.append(new)
            save_config()
            refresh_menus()
            model_var.set(new)
        win.destroy()
    tk.Button(win,text="Add", command=save).pack(pady=10)

def add_new_lang():
    win = tk.Toplevel(root)
    win.title("Add new language")
    win.geometry("400x150")
    win.resizable(False, False)
    win.grab_set()
    tk.Label(win, text="Enter new language name:").pack(pady=10)
    entry = tk.Entry(win,width=50)
    entry.pack(pady=5)
    def save():
        new = entry.get().strip()
        if new and new not in LANGUAGES:
            LANGUAGES.append(new)
            save_config()
            refresh_menus()
            lang_var.set(new)
        win.destroy()
    tk.Button(win, text="Add", command=save).pack(pady=10)

def on_model_select(event):
    if model_var.get() == "+ Add new...":
        add_new_model()
def on_lang_select(event):
    if lang_var.get() == "+ Add new...":
        add_new_lang()

def refresh_menus():
    model_menu["values"] = MODELS + ["+ Add new..."]
    lang_menu["values"] = LANGUAGES + ["+ Add new..."]

def save_result():
    content = output_text.get("1.0",tk.END).strip()
    if not content:
        messagebox.showwarning("Warning","No output to save.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt")])
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        log_text.insert(tk.END,f"Output saved at {path}\n")

def open_results():
    paths = filedialog.askopenfilenames(filetypes=[("Text Files","*.txt")])
    if not paths:
        return
    new = tk.Toplevel(root)
    new.title("Output Comparator")
    text = tk.Text(new, wrap="word", height=30, width=100)
    text.pack(padx=10,pady=10)
    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            text.insert(tk.END, f"--- {os.path.basename(path)} ---\n")
            text.insert(tk.END, f.read()+"\n\n")

def open_preferences():
    pref = tk.Toplevel(root)
    pref.title("Preferences")
    pref.geometry("400x250")
    pref.minsize(350,200)
    pref.resizable(False, False)
    pref.grab_set()
    
    pref.update_idletasks()
    x = root.winfo_x()+(root.winfo_width() // 2 - pref.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2 - pref.winfo_height() // 2)
    pref.geometry(f"+{x}+{y}")

    tk.Label(pref, text="Theme", font=("Segoe UI", 11, "bold")).pack(pady=(20,10))
    theme_var = tk.StringVar(value="Light")

    def apply_theme(event=None):
        selected = theme_var.get()
        if selected == "Dark":
            root.config(bg="#1e1e1e")
            root.config()
            for w in [input_text, output_text, log_text]:
                w.config(bg="#2d2d2d", fg="white", insertbackground="white")
        else:
            root.config(bg="SystemButtonFace")
            for w in [input_text, output_text, log_text]:
                w.config(bg="white", fg="black", insertbackground="black")
    theme_box = ttk.Combobox(pref, textvariable=theme_var, values=["Light", "Dark"], width=20, state="readonly")
    theme_box.pack(pady=5)
    theme_box.bind("<<ComboboxSelected>>", apply_theme)
    
    tk.Button(pref, text="Close", command=pref.destroy).pack(pady=20)


def open_about():
    about = tk.Toplevel(root)
    about.title("About SI_LANG")
    about.geometry("500x400")
    about.minsize(400,300)
    about.resizable(False, False)
    about.grab_set()

    about.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2 - about.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2 - about.winfo_height() // 2)
    about.geometry(f"+{x}+{y}")

    info_text = (
        f"SI_LANG - LLM Translation Tool\n"
        f"Version: {VERSION}\n\n"
        f"Developed by {AUTHOR}\n"
        "University of Alicante\n\n"
        "contact: \n"
        "- Email: yevheniiedelshteyn17@gmail.com\n\n"
        "- GitHub: https://github.com/2PSYV2\n\n"
        "Licensed under the MIT License\n"
        "© 2025 Yevhenii Edelshteyn Kylymnyk"
    )

    tk.Label(about, text=info_text, justify="left", font=("Segoe UI", 10)).pack(padx=20, pady=20)


# Fix for blurry screens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

config =load_config()
MODELS = config["models"]
LANGUAGES = config["languages"]

root = tk.Tk()
root.title(f"SI_LANG - LLM Translation tool")
root.geometry("1280x800")

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar,tearoff=0)
file_menu.add_command(label="Preferences", command=open_preferences)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=open_about)
menubar.add_cascade(label="Help", menu=help_menu)


# Upper secction
top_frame = tk.Frame(root)
top_frame.pack(fill="x", pady=5)

tk.Label(top_frame, text="Model:").pack(side="left", padx=5)
model_var = tk.StringVar(value=MODELS[0])
model_menu = ttk.Combobox(top_frame, textvariable=model_var, values=MODELS + ["+ Add new..."], width=40, state="readonly")
model_menu.pack(side="left", padx=5)
model_menu.bind("<<ComboboxSelected>>", on_model_select)

# languages
tk.Label(top_frame, text="Target Language:").pack(side="left", padx=(20,5))
lang_var = tk.StringVar(value=LANGUAGES[0])
lang_menu = ttk.Combobox(top_frame, textvariable=lang_var, values=LANGUAGES + ["+ Add new..."], width=20, state="readonly")
lang_menu.pack(side="left")
lang_menu.bind("<<ComboboxSelected>>", on_lang_select)

# ==== MAIN CONTAINER ====
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

# --- Upper area (Input / Output side-by-side) ---
io_frame = tk.Frame(content_frame)
io_frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

io_frame.columnconfigure(0, weight=1)
io_frame.columnconfigure(1, weight=1)
io_frame.rowconfigure(0, weight=1)

# Input (left)
left_frame = tk.Frame(io_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
tk.Label(left_frame, text="Input:").pack(anchor="w")
input_text = tk.Text(left_frame, wrap="word", font=("Segoe UI", 11), height=18)
input_text.pack(fill="both", expand=True)

# Output (right)
right_frame = tk.Frame(io_frame, bg="#f5f5f5")
right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
tk.Label(right_frame, text="Output:", bg="#f5f5f5").pack(anchor="w")
output_text = tk.Text(right_frame, wrap="word", bg="#f5f5f5", font=("Segoe UI", 11), height=18)
output_text.pack(fill="both", expand=True)

# --- Buttons ---
button_frame = tk.Frame(content_frame)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Translate", command=translate).pack(side="left", padx=5)
tk.Button(button_frame, text="Save Output", command=save_result).pack(side="left", padx=5)
tk.Button(button_frame, text="Compare Outputs", command=open_results).pack(side="left", padx=5)

# --- Log section (bottom, full width) ---
log_frame = tk.Frame(content_frame)
log_frame.pack(fill="both", expand=False, padx=10, pady=(0, 10))
tk.Label(log_frame, text="Log:").pack(anchor="w")
log_text = tk.Text(log_frame, height=8, wrap="word", bg="#e6e6e6", font=("Consolas", 10))
log_text.pack(fill="both", expand=True)

root.mainloop()



