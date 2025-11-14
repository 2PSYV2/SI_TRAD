import json, os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
from pathlib import Path

VERSION = "V-1.2-Knorozov"
AUTHOR = "Eugene Edelshteyn Kylymnyk"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ICO_PATH = os.path.join(DATA_DIR, "icon.ico")
PNG_PATH = os.path.join(DATA_DIR, "icon.png")

parsed_files = []

main_content_frame = None
file_selector = None
scroll_canvas = None
scroll_frame = None

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

    if loaded_count > 0:
        show_file_selector()

def show_file_selector():
    global main_content_frame, file_selector

    for widget in root.pack_slaves():
        widget.destroy()

    main_content_frame = tk.Frame(root)
    main_content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(main_content_frame, text="Select a file to view:", font=("Segoe UI", 12, "bold")).pack(anchor="w")

    file_selector = ttk.Combobox(
        main_content_frame,
        values=[f["filename"] for f in parsed_files],
        state="readonly",
        width=50
    )
    file_selector.pack(anchor="w", pady=5)
    file_selector.bind("<<ComboboxSelected>>", lambda e: display_file_data())

    file_selector.current(0)
    display_file_data()


def display_file_data():
    global scroll_canvas, scroll_frame

    filename = file_selector.get()
    file_data = next(f for f in parsed_files if f["filename"] == filename)

    for widget in main_content_frame.pack_slaves():
        if widget not in (file_selector, main_content_frame.pack_slaves()[0]):
            widget.destroy()
    
    header = tk.Frame(main_content_frame)
    header.pack(fill="x", pady=(10,5))

    info_text = (
        f"Model: {file_data['model']}\n"
        f"Languages: {file_data['source_language']} -> {file_data['target_language']}\n"
        f"Phrases: {len(file_data['results'])}"
    )
    tk.Label(header, text=info_text, font=("Segoe UI", 11), justify="left").pack(anchor="w")

    scroll_canvas = tk.Canvas(main_content_frame, height=350)
    scrollbar = ttk.Scrollbar(main_content_frame, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = tk.Frame(scroll_canvas)
    scroll_canvas.create_window((0,0), window=scroll_frame, anchor="nw")

    scroll_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

    for entry in file_data["results"]:
        block = tk.Frame(scroll_frame, bd=1, relief="solid", padx=5, pady=5)
        block.pack(fill="x", pady=3)

        tk.Label(block, text=f"ID: {entry['id']}", font=("Segoe UI", 10, "bold")).pack(anchor="w")

        tk.Label(block, text=f"Original: {entry['original']}", wraplength=700).pack(anchor="w")
        tk.Label(block, text=f"Reference: {entry.get('reference','')}", wraplength=700).pack(anchor="w")
        tk.Label(block, text=f"LLM: {entry['llm_translation']}", wraplength=700).pack(anchor="w")

    root.update_idletasks()

    content_height = scroll_frame.winfo_reqheight() + 250
    content_width = scroll_frame.winfo_width() + 50
    max_height = 900

    final_height = min(content_height, max_height)
    root.geometry(f"{content_width}x{final_height}")

def auto_evaluate():
    messagebox.showinfo("Auto Evaluate", "STUB")

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
root.geometry("900x700")
root.resizable(False,True)

try:
    root.iconbitmap(ICO_PATH)
except:
    icon = PhotoImage(file=PNG_PATH)
    root.iconphoto(True, icon)

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Load JSON Files...", command=load_json_files)
file_menu.add_command(label="Evaluate Automatically...", command=auto_evaluate)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=open_about)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

tk.Label(root, text="Load JSON result files to begin.", font=("Segoe UI", 14)).pack(pady=50)
root.geometry("")

root.mainloop()