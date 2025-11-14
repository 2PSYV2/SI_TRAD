# Auto install missing packages
import importlib.util, subprocess, sys, os
from pathlib import Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REQ_FILE = os.path.join(DATA_DIR, "requirements.txt")

MODULE_NAME_MAP = {
    "python-dotenv": "dotenv",
}

def ensure_requirements():

    if os.environ.get("DEPS_CHECKED") == "1":
        return

    if not os.path.exists(REQ_FILE):
        print("[!] requirements.txt not found - skipping dependency check, ensure you have all the required libs manually.")
        return
    
    with open(REQ_FILE, "r", encoding="utf-8") as f:
        pkgs = [line.strip().split("==")[0] for line in f if line.strip() and not line.startswith("#")]

    missing = []
    for pkg in pkgs:
        module_name =MODULE_NAME_MAP.get(pkg, pkg)
        try:
            if importlib.util.find_spec(module_name) is None:
                missing.append(pkg)
        except Exception:
            missing.append(pkg)
    if missing:
        print(f"[!] Missing packages: {'| '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQ_FILE])
            os.environ["DEPS_CHECKED"] = "1"
            print("[+] Dependencies installed.")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            print(f"[x] Failed to install dependencies: {e}")
            time.sleep(3)

ensure_requirements()

################### Main segment ###################

import json, time, ctypes, requests
import tkinter as tk # GUI lib
from tkinter import ttk, messagebox, filedialog, PhotoImage, simpledialog
from dotenv import load_dotenv, set_key # enviorment params extracor

#TODO
# Export output into csv or json

# Version + author
VERSION = "V-1.0-Knorozov"
AUTHOR = "Eugene Edelshteyn Kylymnyk"

# Global paths
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
DEFAULT_CONFIG_PATH = os.path.join(DATA_DIR, "defaults.json")
ENV_PATH = os.path.join(DATA_DIR, ".env")

ICO_PATH = os.path.join(DATA_DIR, "icon.ico")
PNG_PATH = os.path.join(DATA_DIR, "icon.png")

def get_api_key():
    try:
        load_dotenv(dotenv_path=ENV_PATH)
        key = os.getenv("OPENROUTER_API_KEY")
        if not key or key.strip() == "":
            raise ValueError("Missing API key")
        return key.strip()
    except Exception:
        return None

# Available default models
MODELS = [
    "deepseek/deepseek-r1-0528:free"
]

SYSTEM_ROLES = [
    "You are a translation assistant. Provide exclusively the translation of the requested text"
]

# API requesst URL
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def reset_to_default():
    global DEFAULT_CONFIG
    if len(DEFAULT_CONFIG)==0:
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
            DEFAULT_CONFIG = json.load(f)
    global MODELS, LANGUAGES
    MODELS = DEFAULT_CONFIG["models"].copy()
    LANGUAGES = DEFAULT_CONFIG["languages"].copy()

    save_config()
    refresh_menus()
    messagebox.showinfo("Reset", "Configuration was restored to default settings")

def open_api_key_window(parent=None):
    win = tk.Toplevel(parent)
    win.title("Set OpenRouter API key")
    win.geometry("600x180")
    win.resizable(False, False)
    win.grab_set()

    tk.Label(win, text="Enter your OpenRouter API key:", font=("Segoe UI", 10, "bold")).pack(pady=(15,5))

    show_var = tk.BooleanVar(value=False)

    entry = tk.Entry(win, width=80, show="*")
    entry.pack(pady=(0,5),padx=10)

    current_key = os.getenv("OPENROUTER_API_KEY")

    if current_key:
        entry.insert(0, current_key)

    def toggle_show():
        show_var.set(not show_var.get())
        entry.config(show="" if show_var.get() else "*")
        show_btn.config(text="Hide" if show_var.get() else "Show")

    show_btn = tk.Button(win,text="Show",width=10,command=toggle_show)
    show_btn.pack(pady=(0,10))

    def save_key():
        new_key = entry.get().strip()
        if not new_key:
            messagebox.showerror("Error","API key can not be empty.\nRefer to readme.md for instructions.")
            return
        env_path = Path(ENV_PATH)

        if not env_path.exists():
            env_path.parent.mkdir(parents=True, exist_ok=True)
            env_path.touch()

        set_key(env_path, "OPENROUTER_API_KEY", new_key)
        load_dotenv(dotenv_path=env_path, override=True)
        global OPENROUTER_API_KEY
        OPENROUTER_API_KEY = new_key
        messagebox.showinfo("Saved","API key updated succesfully.")
        win.destroy()
    buttons = tk.Frame(win)
    buttons.pack(pady=(5,10))
    tk.Button(buttons, text="Save", command=save_key).pack(side="left", padx=10)
    tk.Button(buttons, text="Close", command=win.destroy).pack(side="left", padx=10)

# Load or create config
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG,f,indent=4)
        return DEFAULT_CONFIG

def save_config():
    cfg = {"models":MODELS, "languages": LANGUAGES, "api": API_URL, "system_roles": SYSTEM_ROLES}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)

def bulk_translate_json():
    sets_dir = Path("sets")
    input_dir = sets_dir / "input"
    output_dir = sets_dir / "output"

    path = filedialog.askopenfilename(initialdir=input_dir,filetypes=[("JSON files", "*.json")])
    input_path = Path(path)
    input_name = input_path.stem

    if not path:
        return
    try:
        with open(path,"r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed toload JSON:{e}")

    if "pairs" not in data or "source_language" not in data or "target_language" not in data:
        messagebox.showerror("Error", "Invalid JSON structure.\nRefer to readme.md for details.")
        return
    src_lang = data["source_language"]
    tgt_lang = data["target_language"]
    pairs = data["pairs"]
    if not pairs:
        messagebox.showwarning("Warning", "No pairs were found in JSON, check the format.")
        return
    


    if tgt_lang in LANGUAGES:
        lang_var.set(tgt_lang)
    else:
        messagebox.showwarning("Warning", "Target language was not on the list of languages.\nWe will add it for you.")
        LANGUAGES.append(tgt_lang)
        save_config()
        lang_var.set(tgt_lang)


    numbered_text = "\n".join(f"{p['id']}. {p['original']}" for p in pairs)
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, numbered_text)
    output_text.delete("1.0", tk.END)

    model = model_var.get()

    prompt = (
        f"you are a professional translation ssytem.\n"
        f"Trasnlate the folowing sentences from {src_lang} to {tgt_lang}.\n"
        f"Return ONLY a valid JSON array of objects with fields 'id' and 'translation'.\n\n"
        f"{numbered_text}"
    )

    log_text.insert(tk.END, f"Sending bulk translation request with {len(pairs)} sentences...\n")
    root.update_idletasks()
    start = time.time()
    # May return a simple string if the format is invalid
    result = call_model(prompt=prompt, model=model)
    finish = time.time()

    try:
        llm_output = json.loads(result)
    except Exception:
        import re
        match = re.search(r"\[[\s\S]*\]", result)
        if match:
            try:
                llm_output = json.loads(match.group(0))
            except Exception:
                llm_output = []
        else:
            llm_output = []
    if not llm_output:
        messagebox.showerror("Error", f"Something went wrong, the model output is not a valid JSON:\n{result}")
        return        

    merged = []
    translations_by_id = {int(r.get("id",0)): r.get("translation","") for r in llm_output}
    for p in pairs:
        merged.append({
            "id": p["id"],
            "original": p["original"],
            "reference": p.get("reference",""),
            "llm_translation": translations_by_id.get(p["id"],"")
        })
    output_data = {
        "model": model,
        "source_language": src_lang,
        "target_language": tgt_lang,
        "results": merged,
        "processing_time_sec": round(finish-start, 2)
    }

    safe_model_name = model.replace("/","_").replace(":","_")
    otput_filename = f"{input_name}_{safe_model_name}.json"

    out_path = filedialog.asksaveasfilename(initialdir=output_dir, initialfile=otput_filename, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    out_pairs = output_data["results"]
    numbered_output = "\n".join(f"{p['id']}. {p['llm_translation']}" for p in out_pairs)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4,ensure_ascii=False)
        messagebox.showinfo("Done", f"Bulk translation complete.\nSaved to: {out_path}")
    
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"{numbered_output}")
        log_text.insert(tk.END, f"Bulk translation complete -> {out_path}\nTime: {finish-start:.2f}\n\n")
    
    else:
        messagebox.showinfo("Cancelled", "Export cancelled.")

# Call model by promt and model
def call_model(prompt, model):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages":[
            {"role": "system", "content": SYSTEM_ROLES[0]},
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
    #TODO
    #Open the window to ask for JSON files to compare and compute
    return

def open_preferences():
    pref = tk.Toplevel(root)
    pref.title("Preferences")
    pref.geometry("640x480")
    pref.minsize(640, 480)
    pref.resizable(False, False)
    pref.grab_set()

    # --- Canvas + Scroll setup ---
    canvas = tk.Canvas(pref, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(pref, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    # Correct configure event binding
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Helper: consistent left padding ---
    PADX = 10

    # === THEME SECTION ===
    tk.Label(scroll_frame, text="Theme", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PADX, pady=(15, 5))
    theme_var = tk.StringVar(value="Light")

    def apply_theme(event=None):
        selected = theme_var.get()
        if selected == "Dark":
            root.config(bg="#1e1e1e")
            for w in [input_text, output_text, log_text]:
                w.config(bg="#2d2d2d", fg="white", insertbackground="white")
        else:
            root.config(bg="SystemButtonFace")
            for w in [input_text, output_text, log_text]:
                w.config(bg="white", fg="black", insertbackground="black")

    theme_box = ttk.Combobox(scroll_frame, textvariable=theme_var,
                             values=["Light", "Dark"], width=20, state="readonly")
    theme_box.pack(anchor="w", padx=PADX, pady=(0, 10))
    theme_box.bind("<<ComboboxSelected>>", apply_theme)

    # === MODEL SECTION ===
    ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", padx=PADX, pady=5)
    tk.Label(scroll_frame, text="Remove Model", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PADX, pady=(5, 2))

    rm_model_var = tk.StringVar(value="")
    rm_model_menu = ttk.Combobox(scroll_frame, textvariable=rm_model_var, values=MODELS, width=40, state="readonly")
    rm_model_menu.pack(anchor="w", padx=PADX, pady=(0, 2))

    def remove_model():
        target = rm_model_var.get()
        if target in MODELS:
            MODELS.remove(target)
            save_config()
            refresh_menus()
            rm_model_menu["values"] = MODELS
            rm_model_var.set("")
            messagebox.showinfo("Removed", f"Model '{target}' was removed.")

    tk.Button(scroll_frame, text="Remove Selected Model", command=remove_model)\
        .pack(anchor="w", padx=PADX, pady=(0, 8))

    # === LANGUAGE SECTION ===
    tk.Label(scroll_frame, text="Remove Language", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PADX, pady=(5, 2))
    rm_lang_var = tk.StringVar(value="")
    rm_lang_menu = ttk.Combobox(scroll_frame, textvariable=rm_lang_var, values=LANGUAGES, width=40, state="readonly")
    rm_lang_menu.pack(anchor="w", padx=PADX, pady=(0, 2))

    def remove_lang():
        target = rm_lang_var.get()
        if target in LANGUAGES:
            LANGUAGES.remove(target)
            save_config()
            refresh_menus()
            rm_lang_menu["values"] = LANGUAGES
            rm_lang_var.set("")
            messagebox.showinfo("Removed", f"Language '{target}' was removed.")

    tk.Button(scroll_frame, text="Remove Selected Language", command=remove_lang)\
        .pack(anchor="w", padx=PADX, pady=(0, 8))

    # === API SECTION ===
    ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", padx=PADX, pady=5)
    tk.Label(scroll_frame, text="API URL", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PADX, pady=(5, 2))

    api_var = tk.StringVar(value=API_URL)
    api_entry = tk.Entry(scroll_frame, textvariable=api_var, width=60)
    api_entry.pack(anchor="w", padx=PADX, pady=(0, 2))

    def save_api():
        global API_URL
        API_URL = api_var.get().strip()
        save_config()
        messagebox.showinfo("Saved", "API URL updated successfully.")

    tk.Button(scroll_frame, text="Save API URL", command=save_api).pack(anchor="w", padx=PADX, pady=(2, 8))

    # === SYSTEM ROLES SECTION ===
    ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", padx=PADX, pady=5)
    tk.Label(scroll_frame, text="System Roles", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=PADX, pady=(5, 2))

    role_var = tk.StringVar(value=SYSTEM_ROLES[0] if SYSTEM_ROLES else "")
    role_menu = ttk.Combobox(scroll_frame, textvariable=role_var,
                             values=SYSTEM_ROLES + ["+ Add new..."], width=60, state="readonly")
    role_menu.pack(anchor="w", padx=PADX, pady=(0, 2))

    def add_role():
        new = simpledialog.askstring("Add System Role", "Enter new system role:")
        if new and new not in SYSTEM_ROLES:
            SYSTEM_ROLES.append(new)
            save_config()
            role_menu["values"] = SYSTEM_ROLES + ["+ Add new..."]

    def set_role(event=None):
        global SYSTEM_ROLES
        if role_var.get() == "+ Add new...":
            add_role()
            return
        selected = role_var.get()
        if selected:
            SYSTEM_ROLES = [selected]
            save_config()

    role_menu.bind("<<ComboboxSelected>>", set_role)

    def remove_role():
        selected = role_var.get()
        if selected in SYSTEM_ROLES:
            SYSTEM_ROLES.remove(selected)
            save_config()
            role_menu["values"] = SYSTEM_ROLES + ["+ Add new..."]
            messagebox.showinfo("Removed", f"System role removed: {selected}")

    tk.Button(scroll_frame, text="Remove Selected Role", command=remove_role)\
        .pack(anchor="w", padx=PADX, pady=(2, 8))

    # === RESET & CLOSE ===
    ttk.Separator(scroll_frame, orient="horizontal").pack(fill="x", padx=PADX, pady=5)
    tk.Button(scroll_frame, text="Reset to Default Configuration", command=reset_to_default, fg="red")\
        .pack(anchor="w", padx=PADX, pady=(10, 5))
    tk.Button(scroll_frame, text="Close", command=pref.destroy)\
        .pack(anchor="w", padx=PADX, pady=(0, 15))

    # --- Final scroll calibration ---
    pref.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.update_idletasks()
    pref.geometry("")


def open_about():
    about = tk.Toplevel(root)
    about.title("About OpenRouter Langer")
    about.geometry("640x680")
    about.minsize(200,200)
    about.resizable(False, False)
    about.grab_set()

    about.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2 - about.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2 - about.winfo_height() // 2)
    about.geometry(f"+{x}+{y}")

    info_text = (
        f"OpenRouter Langer - LLM Translation and comparison Tool\n"
        f"Version: {VERSION}\n\n"
        f"Developed by {AUTHOR}\n"
        "University of Alicante\n\n"
        "contact: \n"
        "- Email: yevheniiedelshteyn17@gmail.com\n\n"
        "- GitHub: https://github.com/2PSYV2\n\n"
        "Licensed under the MIT License\n"
        "© 2025 Yevhenii Edelshteyn Kylymnyk"
    )

    try:
        logo_img = tk.PhotoImage(file=PNG_PATH)
    except Exception as e:
        print("[Error] image could not be loaded: {e}")
        logo_img = None
    if logo_img:
        img_label = tk.Label(about, image=logo_img)
        img_label.image = logo_img
        img_label.pack(anchor="center")

    tk.Label(about, text=info_text, justify="left", font=("Segoe UI", 10)).pack(padx=20, pady=20)

    about.update_idletasks()
    about.geometry("")

####################################################################

# Fix for blurry screens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

if os.path.exists(DEFAULT_CONFIG_PATH):
    with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
        DEFAULT_CONFIG = json.load(f)
else:
    messagebox.showwarning("Warning", "No default settings found.")

# load API key
load_dotenv()
OPENROUTER_API_KEY = get_api_key()

root = tk.Tk()

if not OPENROUTER_API_KEY:
    messagebox.showwarning("Missing API Key","No OpenRouter API key detected.\nPlease input one in the next window.\nIf you are not sure where to get it, refer to readme.md")
    open_api_key_window()
    OPENROUTER_API_KEY = get_api_key()

try:
    root.iconbitmap(ICO_PATH)
except:
    icon = PhotoImage(file=PNG_PATH)
    root.iconphoto(True, icon)

config =load_config()
MODELS = config["models"]
LANGUAGES = config["languages"]

root.title(f"OpenRouter Langer - LLM Translation Testing Tool")
root.geometry("1280x800")

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar,tearoff=0)
file_menu.add_command(label="Preferences", command=open_preferences)
file_menu.add_command(label="Set API Key", command=open_api_key_window)
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
tk.Button(button_frame, text="Translate from JSON", command=bulk_translate_json).pack(side="left", padx=5)
tk.Button(button_frame, text="Compare Outputs", command=open_results).pack(side="left", padx=5)

# --- Log section (bottom, full width) ---
log_frame = tk.Frame(content_frame)
log_frame.pack(fill="both", expand=False, padx=10, pady=(0, 10))
tk.Label(log_frame, text="Log:").pack(anchor="w")
log_text = tk.Text(log_frame, height=8, wrap="word", bg="#e6e6e6", font=("Consolas", 10))
log_text.pack(fill="both", expand=True)

root.mainloop()