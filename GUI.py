import tkinter as tk
from tkinter import StringVar, Radiobutton, Menu

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Input GUI")
        self.root.iconphoto(True, tk.PhotoImage(file="./SentencesFile/app_icon.png"))
        
        # Create the menu bar
        self.menubar = Menu(root)
        root.config(menu=self.menubar)
        
        # Create menu items
        self.path_menu = Menu(self.menubar, tearoff=0)
        self.language_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)
        
        # Add menus to the menubar
        self.menubar.add_cascade(label="Path", menu=self.path_menu)
        self.menubar.add_cascade(label="Language", menu=self.language_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        
        # Add some example menu items (you can customize these)
        self.path_menu.add_command(label="Open Directory")
        self.path_menu.add_command(label="Set Output Path")
        
        self.language_menu.add_command(label="English")
        self.language_menu.add_command(label="Spanish")
        
        self.help_menu.add_command(label="Documentation")
        self.help_menu.add_command(label="About")
        
        # Main text entry
        # Create a frame to hold the text widget and scrollbar
        text_frame = tk.Frame(root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        # Create label inside the frame
        self.text_label = tk.Label(text_frame, text="Insert text here", justify=tk.LEFT)
        self.text_label.pack(anchor=tk.W)
        # Create the text widget and scrollbar
        self.text_entry = tk.Text(text_frame, height=5)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar.set)
        # Pack the text widget and scrollbar
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Author entry
        self.author_label = tk.Label(root, text="Author", justify=tk.LEFT)
        self.author_label.pack(anchor=tk.W, padx=10)
        self.author_entry = tk.Entry(root)
        self.author_entry.pack(fill=tk.X, padx=10)
        
        # Theme drop-down menu
        '''self.theme_label = tk.Label(root, text="Theme")
        self.theme_label.pack()'''
        # List of themes
        self.themes = ["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"]
        # Create separate StringVars for each menu
        self.theme_var1 = StringVar(value=self.themes[0])  # Default to first theme
        self.theme_var2 = StringVar(value=self.themes[0])
        self.theme_var3 = StringVar(value=self.themes[0])
        # Create a frame to hold the theme menus horizontally
        theme_frame = tk.Frame(root)
        theme_frame.pack(pady=20)  # Add vertical padding
        
        self.theme_menu1 = tk.OptionMenu(theme_frame, self.theme_var1, *self.themes)
        self.theme_menu2 = tk.OptionMenu(theme_frame, self.theme_var2, *self.themes) 
        self.theme_menu3 = tk.OptionMenu(theme_frame, self.theme_var3, *self.themes)
        
        self.theme_menu1.pack(side=tk.LEFT)
        self.theme_menu2.pack(side=tk.LEFT)
        self.theme_menu3.pack(side=tk.LEFT)
        
        # Output format options
        self.output_format_label = tk.Label(root, text="Output")
        self.output_format_label.pack()
        self.output_format_var = StringVar(value="json")
        
        self.json_radio = Radiobutton(root, text="json", variable=self.output_format_var, value="json")
        self.json_radio.pack()
        
        self.yaml_radio = Radiobutton(root, text="yaml", variable=self.output_format_var, value="yaml")
        self.yaml_radio.pack()
        
        # Button to submit data
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_data, font=('Arial', 14, 'bold'), width=20, height=2)
        self.submit_button.pack(pady=10)

    def submit_data(self):
        # Extract data
        text = self.text_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()
        themes = [
            self.theme_var1.get(),
            self.theme_var2.get(),
            self.theme_var3.get()
        ]
        output_format = self.output_format_var.get()

        # This would share data with another file or process (currently, it just prints for testing)
        data = {
            "text": text,
            "author": author,
            "themes": themes,  # Now returns a list of all three themes
            "output_format": output_format
        }
        
        print("Collected Data:", data)  # This is just for demonstration

# Run the GUI
root = tk.Tk()
app = SimpleGUI(root)
root.mainloop()
