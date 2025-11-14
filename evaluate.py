import json, os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
from pathlib import Path

VERSION = "V-1.1-Knorozov"
AUTHOR = "Eugene Edelshteyn Kylymnyk"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ICO_PATH = os.path.join(DATA_DIR, "icon.ico")
PNG_PATH = os.path.join(DATA_DIR, "icon.png")

parsed_files = []

def load_json_files():
    global parsed_files

    sets_dir = Path("sets")
    output_dir = sets_dir / "output"

    paths = filedialog.askopenfilenames(initialdir=output_dir ,filetypes=[("JSON files", "*.json")])

    if not paths:
        return
    
    loaded_count = 0
    parsed_files = [] # reset

    for p in paths:
        try:
            with open(p,"r", encoding="utf-8") as f:
                data = json.load(f)

            required_keys = {"model", "source_language", "target_language", "results"}
            if not required_keys.issubset(data):
                messagebox.showerror("Error", f"File '{Path(p).name}' is missing fields.")
                continue

            parsed_files.append(
                {
                    "path": p,
                    "filename": Path(p).name,
                    "model": data["model"],
                    "source_language": data["source_language"],
                    "target_language": data["target_language"],
                    "results": data["results"],
                    "processing_time": data.get("processing_time_sec", None) # If for whathever reason it fails or we remove it
                }
            )
            loaded_count += 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {p}:\n{e}")
        
    messagebox.showinfo("Loaded", f"Succesfully loaded {loaded_count} files.")

def open_about():
    about = tk.Toplevel(root)
    about.title("About - OpenRouter Langer - Evaluator")
    about.geometry("640x680")
    about.minsize(200,200)
    about.resizable(False, False)
    about.grab_set()
    try:
        about.iconbitmap(ICO_PATH)
    except:
        icon = PhotoImage(file=PNG_PATH)
        about.iconphoto(True, icon)

    info_text = (
        f"OpenRouter Langer - Evaluation Tool\n"
    f"Version: {VERSION}\n\n"
    f"Developed by {AUTHOR}\n"
    "University of Alicante\n\n"
    "Tool is used to evaluate the aoutput of LLMS.\n\n"
    "contact: \n"
        "- Email: yevheniiedelshteyn17@gmail.com\n\n"
        "- GitHub: https://github.com/2PSYV2\n\n"
        "Licensed under the MIT License\n"
        f"© 2025 {AUTHOR}"
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

# MAIN SEGMENT

root = tk.Tk()
root.title("OpenTouter Langer - Evaluator")
root.geometry("800x600")

try:
    root.iconbitmap(ICO_PATH)
except:
    icon = PhotoImage(file=PNG_PATH)
    root.iconphoto(True, icon)

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Load JSON Files...", command=load_json_files)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=open_about)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

tk.Label(root, text="Load JSON result files to begin.", font=("Segoe UI", 14)).pack(pady=50)

root.mainloop()