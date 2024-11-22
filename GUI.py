import sys
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, Menu, messagebox
from WorkData.add_data_to_file import add_data_to_file  # This is the function to add data to the JSON file
import yaml
from languages.load_languages import load_all_languages  # Import function to load language translations from YAML files
from Styles.GUI_Styles import configure_styles  # Import function to configure custom styles for the GUI elements

def resource_path(relative_path):
    """Get the absolute path to the resource, considering packaging."""
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        base_path = sys._MEIPASS
    else:  # Running as a script
        base_path = os.path.dirname(__file__)
    
    path = os.path.join(base_path, relative_path)
    print(f"Resource path for {relative_path}: {path}")  # Debugging statement
    return path

class SimpleGUI:
    def __init__(self, root):
        # Initialize the root window and configure styles
        self.root = root
        self.style = ttk.Style("cosmo")
        configure_styles(self.style)
        
        # Load available languages and their translations
        languages_path = resource_path("Languages")
        print(f"Languages path: {languages_path}")  # Debugging statement
        self.languages = load_all_languages(languages_path)  # Pass the path to the function
        self.current_language = "spanish"  # Default language
        
        # Set window properties
        self.configure_window()
        
        # Create all GUI components
        self.create_menu()  # Menu bar
        self.create_main_frame()  # Main frame for user input
        self.create_submit_button()  # Submit button
        
        # Load help content
        self.load_help_content()

    def configure_window(self):
        """Configure the root window properties"""
        # Set the title of the window based on the current language
        self.root.title(self.languages[self.current_language]["window_title"])
        
        # Set the application icon if the file exists
        icon_path = "./SentencesFile/img/app_icon.png"
        if os.path.exists(icon_path):
            self.root.iconphoto(True, ttk.PhotoImage(file=icon_path))

    def load_help_content(self):
        """Load documentation and about content from YAML files"""
        try:
            # Use resource_path to load YAML files
            doc_path = resource_path('Help/documentation.yaml')
            about_path = resource_path('Help/about.yaml')
            print(f"Documentation path: {doc_path}")  # Debugging statement
            print(f"About path: {about_path}")  # Debugging statement
            with open(doc_path, 'r', encoding='utf-8') as doc_file:
                self.documentation = yaml.safe_load(doc_file)
            with open(about_path, 'r', encoding='utf-8') as about_file:
                self.about = yaml.safe_load(about_file)
        except Exception as e:
            print(f"Error loading help content: {e}")
            self.documentation = {"default": "Documentation not available"}
            self.about = {"default": "About information not available"}

    def show_info_message(self, content_key):
        """Display information in a message box with formatted content"""
        # Get the content based on the current language, fallback to default if necessary
        content_data = content_key.get(self.current_language, content_key.get("default", {}))
        
        # Extract title and content
        title = content_data.get('title', '')
        content = content_data.get('content', '')

        # Format the text for display
        formatted_text = f"{title}\n\n{content}".replace("\\n", "\n").strip("{}'\"")

        # Show the information in a message box
        messagebox.showinfo(
            title,  # Use the title from the YAML content
            formatted_text
        )

    def show_documentation(self):
        # Show the documentation content
        self.show_info_message(self.documentation)

    def show_about(self):
        # Show the about content
        self.show_info_message(self.about)

    def create_menu(self):
        """Create the menu bar"""
        # Create the menu bar and configure it for the root window
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # Create language and help menus
        self.language_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)
        
        # Add language and help menus to the menu bar
        self.menubar.add_cascade(label=self.languages[self.current_language]["language_menu"], menu=self.language_menu)
        self.menubar.add_cascade(label=self.languages[self.current_language]["help_menu"], menu=self.help_menu)

        # Populate language options dynamically
        for language in self.languages.keys():
            display_name = self.languages[self.current_language].get(f"language_{language}", language.capitalize())
            self.language_menu.add_command(
                label=display_name, 
                command=lambda lang=language: self.change_language(lang)
            )

        # Add help menu items for documentation and about
        self.help_menu.add_command(
            label=self.languages[self.current_language]["documentation"],
            command=self.show_documentation
        )
        self.help_menu.add_command(
            label=self.languages[self.current_language]["about"],
            command=self.show_about
        )

    def create_main_frame(self):
        """Create main frame for user input"""
        # Create a frame to hold the text entry, author entry, and theme menu
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create text input label and text widget
        self.create_label(main_frame, "insert_text", 0, 0)
        self.text_entry = self.create_text_widget(main_frame, 1, 0)
        
        # Create author label and entry field
        self.create_label(main_frame, "author", 2, 0)
        self.author_entry = ttk.Entry(main_frame, font=("Roboto", 10))
        self.author_entry.grid(row=3, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        # Create theme menu for selecting themes
        self.create_theme_menu(main_frame, 4, 0)
        
        # Allow the main frame to be resizable
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def create_label(self, parent, text_key, row, column):
        """Create and place a label in the parent frame"""
        # Get the label text from the current language
        text = self.languages[self.current_language].get(text_key, text_key.capitalize())
        label = ttk.Label(parent, text=text, justify=LEFT, font=("Roboto", 12))
        # Place the label in the specified row and column
        label.grid(row=row, column=column, sticky="w", padx=5, pady=(0, 5))

    def create_text_widget(self, parent, row, column):
        """Create and place a text widget with a scrollbar"""
        # Create a text widget for user input
        text_entry = ttk.Text(parent, height=5, font=("Roboto", 10), relief="flat")
        # Create a scrollbar and attach it to the text widget
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=text_entry.yview)
        text_entry.configure(yscrollcommand=scrollbar.set)
        
        # Place the text widget and scrollbar in the parent frame
        text_entry.grid(row=row, column=column, columnspan=2, sticky="nsew", padx=10, pady=5)
        scrollbar.grid(row=row, column=2, sticky="ns")
        return text_entry

    def create_theme_menu(self, parent, row, column):
        """Create and place a theme menu"""
        # Get the list of themes from the current language settings
        themes = self.languages[self.current_language].get("themes", [])
        self.theme_var = StringVar(value=themes[0])
        
        # Configure the style for the theme menu button
        self.style.configure("Custom.TMenubutton", font=("Roboto", 10))
        # Create the option menu for themes and place it in the specified position
        self.theme_menu = ttk.OptionMenu(parent, self.theme_var, themes[0], *themes, style="Custom.TMenubutton")
        self.theme_menu.grid(row=row, column=column, sticky="ew", padx=5, pady=(0, 5))

    def create_submit_button(self):
        """Create the submit button"""
        # Create a submit button with a specific style and command to handle data submission
        self.submit_button = ttk.Button(
            self.root,
            text=self.languages[self.current_language]["submit"],  # Update button text based on language
            command=self.submit_data,
            style="Submit.TButton",
            width=20
        )
        # Place the submit button at the bottom of the window
        self.submit_button.pack(pady=20)

    def submit_data(self):
        # Extract data from the form fields
        data = self.extract_data()
        # Validate data - check if any field is empty
        if not all(data.values()):
            # Show an error message if fields are missing
            messagebox.showerror(
                self.languages[self.current_language].get("error_title", "Error"),
                self.languages[self.current_language].get("empty_fields", "Please fill in all fields.")
            )
            return
        
        try:
            # Pass both the data and current GUI language
            add_data_to_file(data, self.current_language)
            # Show a success message if data is saved successfully
            messagebox.showinfo(
                self.languages[self.current_language].get("success_title", "Success"),
                self.languages[self.current_language].get("save_success", "Data saved successfully!")
            )
            # Clear the form after submission
            self.clear_form()
        except Exception as e:
            # Show an error message if saving fails
            messagebox.showerror(
                self.languages[self.current_language].get("error_title", "Error"),
                str(e)
            )

    def extract_data(self):
        """Extract data from form fields"""
        # Retrieve the text, author, and theme from their respective widgets
        return {
            "text": self.text_entry.get("1.0", ttk.END).strip(),
            "author": self.author_entry.get().strip(),
            "theme": self.theme_var.get(),
        }

    def clear_form(self):
        """Clear the form after submission"""
        # Clear the text entry widget
        self.text_entry.delete("1.0", ttk.END)
        # Clear the author entry widget
        self.author_entry.delete(0, ttk.END)
        # Reset the theme menu to its default value
        self.theme_var.set(self.languages[self.current_language].get("themes", [""])[0])

    def change_language(self, language):
        """Update the language of all GUI components"""
        # Update the current language and retrieve new translations
        self.current_language = language
        translations = self.languages[language]
        
        # Update text elements such as window title and submit button
        self.root.title(translations["window_title"])
        self.submit_button.config(text=translations["submit"])
        
        # Update text labels for input fields
        self.update_text_labels(translations)
        
        # Update the labels of the menu items
        self.update_menu_labels(translations)

    def update_text_labels(self, translations):
        """Update the text labels of form fields"""
        # Update the labels for the text input and author fields
        self.text_entry_label = translations.get("insert_text", "Insert Text Here")
        self.create_label(self.text_entry.master, "insert_text", 0, 0)  # Recreate label with new translation
        self.author_entry_label = translations.get("author", "Author")
        self.create_label(self.author_entry.master, "author", 2, 0)  # Recreate label with new translation
        
        # Update the theme menu options
        themes = translations.get("themes", [])
        self.theme_var.set(themes[0]) if themes else None
        menu = self.theme_menu["menu"]
        menu.delete(0, "end")
        for theme in themes:
            menu.add_command(label=theme, command=lambda t=theme: self.theme_var.set(t))

    def update_menu_labels(self, translations):
        """Update the labels of the menu items"""
        # Update the labels for language menu and help menu
        self.menubar.entryconfigure(0, label=translations["language_menu"])
        self.menubar.entryconfigure(1, label=translations["help_menu"])
        
        # Clear existing language menu items
        self.language_menu.delete(0, "end")
        
        # Add updated language menu items
        for language in self.languages.keys():
            display_name = translations.get(f"language_{language}", language.capitalize())
            self.language_menu.add_command(
                label=display_name, 
                command=lambda lang=language: self.change_language(lang)
            )
        
        # Update the labels for documentation and about menu items
        self.help_menu.entryconfigure(0, label=translations["documentation"])
        self.help_menu.entryconfigure(1, label=translations["about"])


# Run the GUI
root = ttk.Window(themename="cosmo")
app = SimpleGUI(root)
root.mainloop()
