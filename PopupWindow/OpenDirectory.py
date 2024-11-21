import os
import tkinter as tk
from tkinter import filedialog, messagebox


def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml")],
        title="Select a file"
    )
    if file_path:
        messagebox.showinfo("Success", f"File selected: {file_path}")
        return file_path
    else:
        messagebox.showerror("Error", "No file selected.")
        return None


if __name__ == "__main__":
    # Initial configuration of the main window
    root = tk.Tk()
    root.title("Main GUI")
    root.geometry("300x100")

    # Menu bar
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open Directory", command=lambda: browse_file())
    menu_bar.add_cascade(label="File", menu=file_menu)
    root.config(menu=menu_bar)

    root.mainloop()
