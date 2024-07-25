import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import webbrowser

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project Menu")
        
        # Set the window to full screen
        
        
        # Optionally, you can bind a key to toggle full-screen mode
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        self.configure(bg='#add8e6')  # Set the background color of the main window

        # Define a larger font size
        large_font = ("Arial", 24)  # Adjust the font family and size as needed

        # Main frame
        main_frame = tk.Frame(self, bg='#add8e6')
        main_frame.pack(fill='both', expand=True)

        # Left frame for project buttons and descriptions
        left_frame = tk.Frame(main_frame, bg='#add8e6')
        left_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)

        tk.Label(left_frame, text="Nikko Nickerson's Coding Projects:", bg='#add8e6', font=large_font).pack(pady=20)  # Set the background color and font of the label

        self.preview_window = None
        self.preview_id = None
        self.hide_preview_id = None

        projects = [
            ("AI ChatBot", "/Users/nikkonickerson/Desktop/MenuForAllProjects/chatty/chatty.py", "A chatbot that uses AI to converse with users.", "/Users/nikkonickerson/Desktop/MenuForAllProjects/AiChatbot.png"),
            ("Weather App", "/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/weatherApp_Gui.py", "A GUI application to display weather information.", "/Users/nikkonickerson/Desktop/MenuForAllProjects/WeatherAPP.png"),
            ("AI Image Generator", "/Users/nikkonickerson/Desktop/MenuForAllProjects/OpenAIImageGenerator/main.py", "Generate images using AI.", "/Users/nikkonickerson/Desktop/MenuForAllProjects/AIImageGenerator.png"),
            ("Snake Game", "/Users/nikkonickerson/Desktop/MenuForAllProjects/TheSnakeGame/SnakeGame.py", "A classic snake game.", "/Users/nikkonickerson/Desktop/MenuForAllProjects/SnakeGame.png"),
            ("Image Recognition", "/Users/nikkonickerson/Desktop/MenuForAllProjects/hgp-vision/vision.py", "Recognize images using AI.", "/Users/nikkonickerson/Desktop/MenuForAllProjects/ImageGenerator.png")
        ]

        for project in projects:
            btn = tk.Button(left_frame, text=project[0], command=lambda p=project[1]: self.run_project(p), bg='#add8e6', font=large_font)
            btn.pack(pady=10)
            tk.Label(left_frame, text=project[2], bg='#add8e6', font=("Arial", 16)).pack(pady=5)  # Set a slightly smaller font for the descriptions
            btn.bind("<Enter>", lambda e, img=project[3]: self.schedule_preview(e, img))
            btn.bind("<Leave>", self.schedule_hide_preview)

        # Right frame for your image and text
        right_frame = tk.Frame(main_frame, bg='#add8e6')
        right_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        self.load_personal_image_and_text(right_frame, "/Users/nikkonickerson/Desktop/MenuForAllProjects/MeFrFr.jpg", "Hello. My name is Nikko Nickerson and I am an esteemed member of the Hidden Genius Project. Throughout this summer, I have worked with my fellow brothers in the Artifical Intelligence Pod to code numerous different projects which YOU can access by clicking on the corresponding buttons to the left")  # Replace with the path to your image

    def load_personal_image_and_text(self, parent, img_path, text):
        # Frame to hold the image and text
        content_frame = tk.Frame(parent, bg='#add8e6')
        content_frame.pack(pady=20, fill='both', expand=True)

        # Frame to hold the image and buttons side by side
        image_button_frame = tk.Frame(content_frame, bg='#add8e6')
        image_button_frame.pack()

        # Load and display the image
        image = Image.open(img_path)
        image = image.resize((400, 600), Image.LANCZOS)  # Resize the image to fit the frame (adjust size as needed)
        photo = ImageTk.PhotoImage(image)
        
        personal_image_label = tk.Label(image_button_frame, image=photo, bg='#add8e6')
        personal_image_label.image = photo  # Keep a reference to avoid garbage collection
        personal_image_label.pack(side='left', pady=0)

        # Frame to hold the buttons
        buttons_frame = tk.Frame(image_button_frame, bg='#add8e6')
        buttons_frame.pack(side='left', padx=10)

        imessage_button = tk.Button(buttons_frame, text="iMessage", command=self.open_imessage, bg='#add8e6', font=("Arial", 16))
        imessage_button.pack(pady=10)

        gmail_button = tk.Button(buttons_frame, text="Gmail", command=self.open_gmail, bg='#add8e6', font=("Arial", 16))
        gmail_button.pack(pady=10)

        # Add text below the image and buttons with wrapping
        text_label = tk.Label(content_frame, text=text, bg='#add8e6', font=("Arial", 18), wraplength=900)  # Adjust wraplength as needed
        text_label.pack(pady=5, fill='x')

    def open_imessage(self):
        phone_number = "3238674142"  # Replace with your phone number
        url = f"sms:{phone_number}"
        webbrowser.open(url)

    def open_gmail(self):
        email_address = "nikko.nickerson@hgs.hiddengeniusproject.org"  # Replace with your email address
        url = f"mailto:{email_address}"
        webbrowser.open(url)

    def schedule_preview(self, event, img_path):
        if self.preview_id is not None:
            self.after_cancel(self.preview_id)
        if self.hide_preview_id is not None:
            self.after_cancel(self.hide_preview_id)
        self.preview_id = self.after(500, lambda: self.show_preview(event, img_path))  # Delay of 500ms

    def show_preview(self, event, img_path):
        if self.preview_window is None or not self.preview_window.winfo_exists():
            self.preview_window = tk.Toplevel(self)
            self.preview_window.title("Preview")
            self.preview_window.configure(bg='#add8e6')
            self.preview_image_label = tk.Label(self.preview_window, bg='#add8e6')
            self.preview_image_label.pack(pady=10, padx=10, fill='both', expand=True)
        
        image = Image.open(img_path)

        # Calculate the size of the preview window based on the image size
        max_width, max_height = 600, 600  # Define the maximum size of the preview window
        aspect_ratio = image.width / image.height

        if image.width > image.height:
            new_width = min(max_width, image.width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_height, image.height)
            new_width = int(new_height * aspect_ratio)

        image = image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        self.preview_image_label.config(image=photo)
        self.preview_image_label.image = photo  # Keep a reference to avoid garbage collection

        # Adjust the size of the preview window based on the resized image
        self.preview_window.geometry(f"{new_width + 20}x{new_height + 60}")
        self.preview_window.geometry(f"+{event.widget.winfo_rootx() + 50}+{event.widget.winfo_rooty() + 50}")
        self.preview_window.deiconify()

    def schedule_hide_preview(self, event):
        if self.hide_preview_id is not None:
            self.after_cancel(self.hide_preview_id)
        self.hide_preview_id = self.after(1000, self.hide_preview)  # Delay of 1000ms (1 second)

    def hide_preview(self):
        if self.preview_window is not None and self.preview_window.winfo_exists():
            self.preview_window.withdraw()

    # Function to run the project
    def run_project(self, project_name):
        try:
            subprocess.Popen(["python3", project_name])
            self.withdraw()
            self.wait_window(tk.Toplevel(self))
            self.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run {project_name}: {e}")

    # Function to toggle full-screen mode
    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    # Function to exit full-screen mode
    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
