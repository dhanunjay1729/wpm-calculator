import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput import keyboard

class WPMCalculator:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("WPM Calculator")
        self.root.geometry("250x120")
        
        # Make window stay on top (optional)
        self.root.wm_attributes("-topmost", True)
        
        # Create the WPM display label
        self.wpm_label = tk.Label(
            self.root, 
            text="WPM: 0", 
            font=("Arial", 18, "bold"),
            fg="blue"
        )
        self.wpm_label.pack(expand=True)
        
        # Create reset button
        self.reset_button = tk.Button(
            self.root,
            text="Reset",
            command=self.reset_counter,
            font=("Arial", 10)
        )
        self.reset_button.pack(pady=5)
        
        # Initialize WPM tracking variables
        self.word_count = 0
        self.start_time = time.time()
        self.last_keypress_time = time.time()
        
        # Start keystroke listener
        self.start_keystroke_listener()
        
        # Start WPM update timer
        self.update_wpm()
        
    def on_key_press(self, key):
        try:
            # Check if spacebar was pressed
            if key == keyboard.Key.space:
                self.word_count += 1
                self.last_keypress_time = time.time()
                
                # Reset timer on first word
                if self.word_count == 1:
                    self.start_time = time.time()
        except AttributeError:
            pass
    
    def reset_counter(self):
        self.word_count = 0
        self.start_time = time.time()
        self.last_keypress_time = time.time()
    
    def calculate_wpm(self):
        # Auto-reset if no typing for 10 seconds
        # Auto-reset if no typing for 5 seconds
        if time.time() - self.last_keypress_time > 5:
            self.reset_counter()
            return 0
            
        if self.word_count == 0:
            return 0
        
        elapsed_time = time.time() - self.start_time
        elapsed_minutes = elapsed_time / 60
        
        if elapsed_minutes > 0:
            wpm = self.word_count / elapsed_minutes
            return int(wpm)
        return 0
    
    def update_wpm(self):
        # Calculate and update WPM display
        current_wpm = self.calculate_wpm()
        self.wpm_label.config(text=f"WPM: {current_wpm}")
        
        # Schedule next update in 500ms
        self.root.after(500, self.update_wpm)
    
    def start_keystroke_listener(self):
        # Start listening for keystrokes in a separate thread
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
    def run(self):
        # Start the GUI
        self.root.mainloop()
        # Stop listener when window closes
        self.listener.stop()

# Create and run the application
if __name__ == "__main__":
    app = WPMCalculator()
    app.run()