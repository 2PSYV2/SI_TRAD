import json, os
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

VERSION = "V-1.5-Knorozov"
AUTHOR = "Eugene Edelshteyn Kylymnyk"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ICO_PATH = os.path.join(DATA_DIR, "icon.ico")
PNG_PATH = os.path.join(DATA_DIR, "icon.png")

JSON_FILE = ""

def load_evaL_json():
    global JSON_FILE
    sets_dir = Path("sets")
    json_dir = sets_dir / "output/evaluation_output"
    path = filedialog.askopenfilename(initialdir=json_dir, title="Select evaluation output JSON", filetypes=[("JSON files", "*.json")])
    if not path:
        return None

    JSON_FILE = path

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rows = []
    for model_name, metrics in data["models"].items():
        for metric_name, entries in metrics.items():
            for e in entries:
                rows.append(
                    {
                        "model": model_name,
                        "metric": metric_name,
                        "id": e["id"],
                        "score": e["score"]
                    }
                )
            
    df = pd.DataFrame(rows)
    return df

def graph_average_scores(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))

    avg = df.groupby(["model", "metric"])["score"].mean().unstack()

    bars = avg.plot(kind="bar", ax=ax)

    ax.set_title("Average Metric Scores by Model", fontsize=14)
    plt.suptitle("Computed from evaluation JSON: mean BLEU / METEOR / ROUGE-L per model", fontsize=9)

    ax.set_xlabel("Model")
    ax.set_ylabel("Average Score")
    plt.xticks(rotation=30, ha="right")

    for container in bars.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(
                f"{height:.3f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=8
            )

    plt.tight_layout()
    plt.show()

def graph_per_id(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))

    mean_df = df.groupby(["model", "id"])["score"].mean().reset_index()

    for model in mean_df["model"].unique():
        subset = mean_df[mean_df["model"] == model]
        ax.plot(subset["id"], subset["score"], marker="o", label=model)

    ax.set_title("Average Score per Phrase ID", fontsize=14)
    plt.suptitle("Each point = mean BLEU/METEOR/ROUGE-L for that phrase", fontsize=9)

    ax.set_xlabel("Phrase ID")
    ax.set_ylabel("Score")
    ax.legend()

    plt.tight_layout()
    plt.show()

def graph_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))

    for metric in df["metric"].unique():
        subset = df[df["metric"] == metric]["score"]
        ax.hist(subset, alpha=0.6, bins=10, label=metric)

    ax.set_title("Score Distribution per Metric", fontsize=14)
    plt.suptitle("Histogram of BLEU / METEOR / ROUGE-L scores", fontsize=9)

    ax.set_xlabel("Score")
    ax.set_ylabel("Frequency")
    ax.legend()

    plt.tight_layout()
    plt.show()

def graph_metric_by_phrase(df: pd.DataFrame):
    win = tk.Toplevel()
    win.title("Select Metric")
    win.geometry("250x120")
    win.resizable(False, False)

    tk.Label(win, text="Select metric:", font=("Segoe UI", 10)).pack(pady=5)

    metrics = sorted(df["metric"].unique())

    metric_var = tk.StringVar(value=metrics[0])

    dropdown = tk.OptionMenu(win, metric_var, *metrics)
    dropdown.pack(pady=5)

    def plot_selected():
        metric = metric_var.get()
        sub = df[df["metric"] == metric]

        fig, ax = plt.subplots(figsize=(7, 4))

        for model in sub["model"].unique():
            part = sub[sub["model"] == model]
            ax.plot(
                part["id"], part["score"], marker="o", label=model
            )

        ax.set_title(f"{metric} Score per Phrase ID", fontsize=14)
        plt.suptitle(f"Plot of {metric} across all phrases for each model", fontsize=9)

        ax.set_xlabel("Phrase ID")
        ax.set_ylabel(f"{metric} Score")
        ax.legend()

        plt.tight_layout()
        plt.show()

    tk.Button(win, text="Plot", command=plot_selected).pack(pady=10)

def open_graph_window():
    df = load_evaL_json()
    if df is None:
        return

    win = tk.Toplevel()
    win.title(f"Graph Evaluation: {JSON_FILE}")
    win.geometry("540x480")
    win.resizable(False, False)

    try:
        win.iconbitmap(ICO_PATH)
    except:
        icon = PhotoImage(file=PNG_PATH)
        win.iconphoto(True, icon)

    tk.Button(win, text="Average Scores", width=25,
              command=lambda: graph_average_scores(df)).pack(pady=10)

    tk.Button(win, text="Trend per ID", width=25,
              command=lambda: graph_per_id(df)).pack(pady=10)

    tk.Button(win, text="Score Distribution", width=25,
              command=lambda: graph_distribution(df)).pack(pady=10)
    
    tk.Button(win, text="Metric per Phrase", width=25,
          command=lambda: graph_metric_by_phrase(df)).pack(pady=10)

    tk.Label(win, text="Graphs generated with matplotlib").pack(pady=10)