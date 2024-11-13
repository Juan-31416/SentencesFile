import tkinter as tk
from tkinter import StringVar, Radiobutton, Menu
from add_data_to_file import add_data_to_json  # This is the function to add data to the JSON file
import os


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Input GUI")
        
        # Set icon if available
        icon_path = "./SentencesFile/app_icon.png"
        if os.path.exists(icon_path):
            self.root.iconphoto(True, tk.PhotoImage(file=icon_path))

        # Create all components of the GUI
        self.create_menu()
        self.create_text_entry()
        self.create_author_entry()
        self.create_theme_menu()
        self.create_output_format()
        self.create_submit_button()

    def create_menu(self):
        # Create the menu bar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create and add menu items
        self.path_menu = Menu(self.menubar, tearoff=0)
        self.language_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Path", menu=self.path_menu)
        self.menubar.add_cascade(label="Language", menu=self.language_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # Add some example menu items (you can customize these)
        self.path_menu.add_command(label="Open Directory")
        self.path_menu.add_command(label="Set Output extension")

        self.language_menu.add_command(label="English")
        self.language_menu.add_command(label="Spanish")

        self.help_menu.add_command(label="Documentation")
        self.help_menu.add_command(label="About")

    def create_text_entry(self):
        # Create a frame to hold the text widget and scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create label inside the frame
        self.text_label = tk.Label(text_frame, text="Insert text here", justify=tk.LEFT)
        self.text_label.grid(row=0, column=0, sticky="w", padx=10)

        # Create the text widget and scrollbar
        self.text_entry = tk.Text(text_frame, height=5)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar.set)

        # Pack the text widget and scrollbar using grid
        self.text_entry.grid(row=1, column=0, columnspan=2, sticky="nsew")
        scrollbar.grid(row=1, column=2, sticky="ns")

        # Allow grid resizing
        text_frame.grid_rowconfigure(1, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

    def create_author_entry(self):
        # Author entry
        self.author_label = tk.Label(self.root, text="Author", justify=tk.LEFT)
        self.author_label.pack(anchor=tk.W, padx=10)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack(fill=tk.X, padx=10)

    def create_theme_menu(self):
        # Create a frame to hold the theme menus horizontally
        theme_frame = tk.Frame(self.root)
        theme_frame.pack(pady=20)  # Add vertical padding
        
        # List of themes
        self.themes = ["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"]
        self.theme_vars = []  # List to store StringVar objects

        # Create OptionMenu widgets for themes
        for i in range(3):
            theme_var = StringVar(value=self.themes[0])  # Default to first theme
            self.theme_vars.append(theme_var)
            theme_menu = tk.OptionMenu(theme_frame, theme_var, *self.themes)
            theme_menu.pack(side=tk.LEFT)

    def create_output_format(self):
        # Output format options
        self.output_format_label = tk.Label(self.root, text="Output")
        self.output_format_label.pack()
        self.output_format_var = StringVar(value="json")

        self.json_radio = Radiobutton(self.root, text="json", variable=self.output_format_var, value="json")
        self.json_radio.pack()

        self.yaml_radio = Radiobutton(self.root, text="yaml", variable=self.output_format_var, value="yaml")
        self.yaml_radio.pack()

    def create_submit_button(self):
        # Button to submit data
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_data, font=('Arial', 14, 'bold'), width=20, height=2)
        self.submit_button.pack(pady=10)

    def submit_data(self):
        # Extract data and handle submission
        data = self.extract_data()
        try:
            add_data_to_json(data)
        except Exception as e:
            print(f"Error al añadir datos al archivo: {e}")
        self.clear_form()

    def extract_data(self):
        # Extract data from the form
        return {
            "text": self.text_entry.get("1.0", tk.END).strip(),
            "author": self.author_entry.get().strip(),
            "themes": [theme_var.get() for theme_var in self.theme_vars],
            "output_format": self.output_format_var.get()
        }

    def clear_form(self):
        # Clear the form after submission
        self.text_entry.delete("1.0", tk.END)
        self.author_entry.delete(0, tk.END)
        for theme_var in self.theme_vars:
            theme_var.set(self.themes[0])


# Run the GUI
root = tk.Tk()
app = SimpleGUI(root)
root.mainloop()
