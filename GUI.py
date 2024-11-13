import tkinter as tk
from tkinter import StringVar, Radiobutton

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Input GUI")
        self.root.iconphoto(True, tk.PhotoImage(file="./SentencesFile/app_icon.png"))
        
        # Main text entry
        self.text_label = tk.Label(root, text="Insert text here")
        self.text_label.pack()
        
        # Create a frame to hold the text widget and scrollbar
        text_frame = tk.Frame(root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create the text widget and scrollbar
        self.text_entry = tk.Text(text_frame, height=5)
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.text_entry.yview)
        self.text_entry.configure(yscrollcommand=scrollbar.set)
        
        # Pack the text widget and scrollbar
        self.text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Author entry
        self.author_label = tk.Label(root, text="Author")
        self.author_label.pack()
        self.author_entry = tk.Entry(root)
        self.author_entry.pack()
        
        # Theme drop-down menu
        self.theme_label = tk.Label(root, text="Theme")
        self.theme_label.pack()
        
        # List of themes
        self.themes = ["Theme 1", "Theme 2", "Theme 3", "Theme 4", "Theme 5"]
        self.theme_var = StringVar(value=self.themes[0])  # Default to the first theme
        
        # Create a frame to hold the theme menus horizontally
        theme_frame = tk.Frame(root)
        theme_frame.pack()
        
        self.theme_menu1 = tk.OptionMenu(theme_frame, self.theme_var, *self.themes)
        self.theme_menu2 = tk.OptionMenu(theme_frame, self.theme_var, *self.themes) 
        self.theme_menu3 = tk.OptionMenu(theme_frame, self.theme_var, *self.themes)
        
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
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_data)
        self.submit_button.pack()

    def submit_data(self):
        # Extract data
        text = self.text_entry.get("1.0", tk.END).strip()
        author = self.author_entry.get().strip()
        theme = self.theme_var.get()
        output_format = self.output_format_var.get()

        # This would share data with another file or process (currently, it just prints for testing)
        data = {
            "text": text,
            "author": author,
            "theme": theme,
            "output_format": output_format
        }
        
        print("Collected Data:", data)  # This is just for demonstration

# Run the GUI
root = tk.Tk()
app = SimpleGUI(root)
root.mainloop()
