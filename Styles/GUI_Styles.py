def configure_styles(style):
    """Configure custom styles for widgets"""
    # Configure modern fonts
    default_font = ("Roboto", 10)
    header_font = ("Roboto", 12, "bold")
    
    style.configure("TLabel", font=default_font)
    style.configure("TButton", 
        font=default_font,
        padding=10,
        borderwidth=0,
        borderradius=8
    )
    
    # Custom submit button style
    style.configure("Submit.TButton",
        font=header_font,
        padding=10,
        borderwidth=0,
        borderradius=8,
        background="#00A3E0",
        foreground="white"
    )
    style.map("Submit.TButton",
        background=[("active", "#0088BF"), ("disabled", "#CCE5FF")],
        foreground=[("disabled", "#666666")]
    ) 