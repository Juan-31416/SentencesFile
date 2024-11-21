import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, Menu
from add_data_to_file import add_data_to_json  # This is the function to add data to the JSON file
import os
import yaml
from PopupWindow.OpenDirectory import browse_file
from languages.load_languages import load_all_languages


class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style("cosmo")  # You can change the theme to "darkly", "flatly", "solar", among others
        self.configure_custom_styles()
        
        # Load available languages and their translations
        self.languages = load_all_languages()
        self.current_language = "spanish"  # Default language
        
        self.root.title(self.languages[self.current_language]["window_title"])

        # Set icon if available
        icon_path = "./SentencesFile/app_icon.png"
        if os.path.exists(icon_path):
            self.root.iconphoto(True, ttk.PhotoImage(file="app_icon.png"))

        # Create all GUI components
        self.create_menu()
        self.create_text_entry()
        self.create_author_entry()
        self.create_theme_menu()
        self.create_submit_button()

    def configure_custom_styles(self):
        """Configure custom styles for widgets"""
        # Configure modern fonts
        default_font = ("Roboto", 10)
        header_font = ("Roboto", 12, "bold")
        
        self.style.configure("TLabel", font=default_font)
        self.style.configure("TButton", 
            font=default_font,
            padding=10,
            borderwidth=0,
            borderradius=8
        )
        
        # Custom submit button style
        self.style.configure("Submit.TButton",
            font=header_font,
            padding=10,
            borderwidth=0,
            borderradius=8,
            background="#00A3E0",
            foreground="white"
        )
        self.style.map("Submit.TButton",
            background=[("active", "#0088BF"), ("disabled", "#CCE5FF")],
            foreground=[("disabled", "#666666")]
        )

    def create_menu(self):
        # Create the menu bar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        # Create and add menu items
        self.path_menu = Menu(self.menubar, tearoff=0)
        self.language_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)

        # Store menu references for later language updates
        self.menu_cascades = {
            "path_menu": self.menubar.add_cascade(label=self.languages[self.current_language]["path_menu"], menu=self.path_menu),
            "language_menu": self.menubar.add_cascade(label=self.languages[self.current_language]["language_menu"], menu=self.language_menu),
            "help_menu": self.menubar.add_cascade(label=self.languages[self.current_language]["help_menu"], menu=self.help_menu)
        }

        # Add path menu items
        self.path_menu.add_command(
            label=self.languages[self.current_language]["open_directory"], 
            command=lambda: browse_file()
        )

        # Add language options dynamically
        for language in self.languages.keys():
            display_name = self.languages[self.current_language].get(f"language_{language}", language.capitalize())
            self.language_menu.add_command(
                label=display_name, 
                command=lambda lang=language: self.change_language(lang)
            )

        # Add help menu items
        self.help_menu.add_command(label=self.languages[self.current_language]["documentation"])
        self.help_menu.add_command(label=self.languages[self.current_language]["about"])

    def create_text_entry(self):
        text_frame = ttk.Frame(self.root)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.text_label = ttk.Label(
            text_frame,
            text="Insert text here",
            justify=LEFT,
            font=("Roboto", 12)
        )
        self.text_label.grid(row=0, column=0, sticky="w", padx=5, pady=(0, 5))
        
        self.text_entry = ttk.Text(
            text_frame,
            height=5,
            font=("Roboto", 10),
            relief="flat"
        )
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar.set)

        # Organize the text widget and scrollbar with grid
        self.text_entry.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        scrollbar.grid(row=1, column=2, sticky="ns")

        # Allow resizing
        text_frame.grid_rowconfigure(1, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

    def create_author_entry(self):
        # Create a frame to hold both author entry and theme menu
        author_theme_frame = ttk.Frame(self.root)
        author_theme_frame.pack(fill=X, padx=10, pady=10)
        
        # Author label and entry (left side)
        self.author_label = ttk.Label(author_theme_frame, text="Author", justify=LEFT, font=("Roboto", 12))
        self.author_label.pack(side=LEFT)
        self.author_entry = ttk.Entry(author_theme_frame, font=("Roboto", 10))
        self.author_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 20))

    def create_theme_menu(self):
        # Get themes from current language
        self.themes = self.languages[self.current_language].get("themes", [])
        self.theme_vars = []

        # Create OptionMenu widget for theme
        theme_var = StringVar(value=self.themes[0])
        self.theme_vars = [theme_var]  # Keep as list for compatibility
        
        # Create and configure style for OptionMenu
        self.style.configure("Custom.TMenubutton", font=("Roboto", 10))
        self.theme_menu = ttk.OptionMenu(
            self.author_entry.master,  # Use the same frame as author entry
            theme_var, 
            self.themes[0],
            *self.themes,
            style="Custom.TMenubutton"
        )
        self.theme_menu.pack(side=RIGHT)

    def create_submit_button(self):
        # Modern submit button with custom style
        self.submit_button = ttk.Button(
            self.root,
            text="Submit",
            command=self.submit_data,
            style="Submit.TButton",
            width=20
        )
        self.submit_button.pack(pady=20)

    def submit_data(self):
        # Extract data and handle presentation
        data = self.extract_data()
        try:
            add_data_to_json(data)
        except Exception as e:
            print(f"Error adding data to file: {e}")
        self.clear_form()

    def extract_data(self):
        # Extract data from the form
        return {
            "text": self.text_entry.get("1.0", ttk.END).strip(),
            "author": self.author_entry.get().strip(),
            "themes": [theme_var.get() for theme_var in self.theme_vars],
        }

    def clear_form(self):
        # Clear the form after submission
        self.text_entry.delete("1.0", ttk.END)
        self.author_entry.delete(0, ttk.END)
        for theme_var in self.theme_vars:
            theme_var.set(self.themes[0])

    def change_language(self, language):
        """Updates the GUI text elements to the selected language"""
        self.current_language = language
        translations = self.languages[language]
        
        # Update all text elements
        self.root.title(translations["window_title"])
        self.text_label.config(text=translations["insert_text"])
        self.author_label.config(text=translations["author"])
        self.submit_button.config(text=translations["submit"])
        
        # Update menu labels
        self.menubar.entryconfigure(0, label=translations["path_menu"])  # Path menu
        self.menubar.entryconfigure(1, label=translations["language_menu"])  # Language menu
        self.menubar.entryconfigure(2, label=translations["help_menu"])  # Help menu
        
        # Update submenu items
        self.path_menu.entryconfigure(0, label=translations["open_directory"])
        self.help_menu.entryconfigure(0, label=translations["documentation"])
        self.help_menu.entryconfigure(1, label=translations["about"])
        
        # Update theme menu
        self.themes = translations.get("themes", [])
        if self.themes:
            self.theme_vars[0].set(self.themes[0])
            menu = self.theme_menu["menu"]
            menu.delete(0, "end")
            for theme in self.themes:
                menu.add_command(label=theme, 
                               command=lambda t=theme: self.theme_vars[0].set(t))
        
        # Update language menu items
        for i, lang in enumerate(self.languages.keys()):
            display_name = translations.get(f"language_{lang}", lang.capitalize())
            self.language_menu.entryconfigure(i, label=display_name)


# Run the GUI
root = ttk.Window(themename="cosmo")
app = SimpleGUI(root)
root.mainloop()
