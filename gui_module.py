#!/usr/bin/env python3
"""
Advanced Cute GUI for Raspberry Pi 4 Model B
Features: Animated character, system monitoring, interactive elements
"""

import tkinter as tk
from tkinter import ttk
import random
import math
import subprocess
import psutil
from datetime import datetime

class CuteRaspberryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍓 Raspberry Pi Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFE5E5")
        
        # Animation variables
        self.blink_state = False
        self.bounce_offset = 0
        self.bounce_direction = 1
        self.mood = "happy"  # happy, excited, sleepy, worried
        self.expression_timer = 0
        
        # Create main container
        self.main_frame = tk.Frame(root, bg="#FFE5E5")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create character canvas
        self.canvas = tk.Canvas(
            self.main_frame, 
            width=400, 
            height=300, 
            bg="#FFE5E5", 
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Info panel
        self.create_info_panel()
        
        # Control buttons
        self.create_controls()
        
        # Status bar
        self.create_status_bar()
        
        # Draw initial character
        self.draw_character()
        
        # Start animations
        self.animate()
        self.update_system_info()
        
    def draw_character(self):
        """Draw the cute character with current expression"""
        self.canvas.delete("all")
        
        # Calculate bounce position
        y_offset = self.bounce_offset
        
        # Body (rounded rectangle/screen)
        body_x1, body_y1 = 150, 100 + y_offset
        body_x2, body_y2 = 250, 200 + y_offset
        
        # Shadow
        self.canvas.create_oval(
            body_x1 - 10, body_y2 + 5,
            body_x2 + 10, body_y2 + 15,
            fill="#DDD", outline=""
        )
        
        # Body outline
        self.canvas.create_rectangle(
            body_x1, body_y1, body_x2, body_y2,
            fill="#FFFFFF", outline="#333", width=3,
            tags="body"
        )
        
        # Screen glare effect
        self.canvas.create_oval(
            body_x1 + 10, body_y1 + 10,
            body_x1 + 40, body_y1 + 30,
            fill="#F0F8FF", outline="", stipple="gray50"
        )
        
        # Eyes
        eye_y = body_y1 + 40
        left_eye_x = body_x1 + 30
        right_eye_x = body_x2 - 30
        
        if self.blink_state:
            # Closed eyes
            self.canvas.create_line(
                left_eye_x - 10, eye_y, left_eye_x + 10, eye_y,
                width=3, fill="#333"
            )
            self.canvas.create_line(
                right_eye_x - 10, eye_y, right_eye_x + 10, eye_y,
                width=3, fill="#333"
            )
        else:
            # Open eyes based on mood
            if self.mood == "happy":
                self.draw_happy_eyes(left_eye_x, right_eye_x, eye_y)
            elif self.mood == "excited":
                self.draw_excited_eyes(left_eye_x, right_eye_x, eye_y)
            elif self.mood == "sleepy":
                self.draw_sleepy_eyes(left_eye_x, right_eye_x, eye_y)
            elif self.mood == "worried":
                self.draw_worried_eyes(left_eye_x, right_eye_x, eye_y)
        
        # Mouth based on mood
        mouth_y = body_y1 + 70
        if self.mood == "happy":
            self.canvas.create_arc(
                body_x1 + 30, mouth_y - 10,
                body_x2 - 30, mouth_y + 20,
                start=0, extent=-180, width=3,
                outline="#333", style=tk.ARC
            )
        elif self.mood == "excited":
            self.canvas.create_oval(
                body_x1 + 40, mouth_y - 5,
                body_x2 - 40, mouth_y + 15,
                fill="#333", outline="#333"
            )
        elif self.mood == "sleepy":
            self.canvas.create_oval(
                body_x1 + 45, mouth_y,
                body_x2 - 45, mouth_y + 8,
                fill="#333", outline="#333"
            )
        elif self.mood == "worried":
            self.canvas.create_arc(
                body_x1 + 30, mouth_y + 20,
                body_x2 - 30, mouth_y - 10,
                start=0, extent=180, width=3,
                outline="#333", style=tk.ARC
            )
        
        # Cheeks
        self.canvas.create_oval(
            body_x1 + 5, body_y1 + 60,
            body_x1 + 25, body_y1 + 80,
            fill="#FFB6C1", outline=""
        )
        self.canvas.create_oval(
            body_x2 - 25, body_y1 + 60,
            body_x2 - 5, body_y1 + 80,
            fill="#FFB6C1", outline=""
        )
        
        # Arms
        arm_y = body_y1 + 50 + y_offset
        # Left arm
        self.canvas.create_line(
            body_x1, arm_y,
            body_x1 - 30, arm_y + 20 - abs(y_offset),
            width=8, fill="#333", capstyle=tk.ROUND
        )
        # Right arm
        self.canvas.create_line(
            body_x2, arm_y,
            body_x2 + 30, arm_y + 20 - abs(y_offset),
            width=8, fill="#333", capstyle=tk.ROUND
        )
        
        # Raspberry Pi logo
        logo_x, logo_y = 200, 220 + y_offset
        self.canvas.create_text(
            logo_x, logo_y,
            text="🍓", font=("Arial", 24)
        )
        
        # Antenna
        antenna_x = 200
        antenna_y = body_y1 - 20
        self.canvas.create_line(
            antenna_x, body_y1,
            antenna_x, antenna_y,
            width=3, fill="#333"
        )
        self.canvas.create_oval(
            antenna_x - 5, antenna_y - 10,
            antenna_x + 5, antenna_y,
            fill="#FF1493", outline="#333", width=2
        )
    
    def draw_happy_eyes(self, left_x, right_x, y):
        # Large round eyes
        self.canvas.create_oval(left_x - 12, y - 12, left_x + 12, y + 12,
                               fill="#000", outline="")
        self.canvas.create_oval(right_x - 12, y - 12, right_x + 12, y + 12,
                               fill="#000", outline="")
        # Highlights
        self.canvas.create_oval(left_x - 5, y - 8, left_x + 1, y - 2,
                               fill="#FFF", outline="")
        self.canvas.create_oval(right_x - 5, y - 8, right_x + 1, y - 2,
                               fill="#FFF", outline="")
    
    def draw_excited_eyes(self, left_x, right_x, y):
        # Star eyes
        for x in [left_x, right_x]:
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10 - math.pi / 2
                radius = 12 if i % 2 == 0 else 6
                points.extend([x + radius * math.cos(angle),
                             y + radius * math.sin(angle)])
            self.canvas.create_polygon(points, fill="#FFD700", outline="#333", width=2)
    
    def draw_sleepy_eyes(self, left_x, right_x, y):
        # Half-closed eyes
        self.canvas.create_arc(left_x - 12, y - 12, left_x + 12, y + 12,
                              start=180, extent=180, fill="#000", outline="")
        self.canvas.create_arc(right_x - 12, y - 12, right_x + 12, y + 12,
                              start=180, extent=180, fill="#000", outline="")
    
    def draw_worried_eyes(self, left_x, right_x, y):
        # Small worried eyes
        self.canvas.create_oval(left_x - 8, y - 8, left_x + 8, y + 8,
                               fill="#000", outline="")
        self.canvas.create_oval(right_x - 8, y - 8, right_x + 8, y + 8,
                               fill="#000", outline="")
    
    def create_info_panel(self):
        """Create system information panel"""
        info_frame = tk.LabelFrame(
            self.main_frame,
            text="📊 System Info",
            font=("Arial", 12, "bold"),
            bg="#FFF0F5",
            fg="#333"
        )
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # CPU
        self.cpu_label = tk.Label(
            info_frame,
            text="CPU: ---%",
            font=("Arial", 10),
            bg="#FFF0F5",
            anchor="w"
        )
        self.cpu_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        self.cpu_bar = ttk.Progressbar(
            info_frame,
            length=200,
            mode='determinate'
        )
        self.cpu_bar.grid(row=0, column=1, padx=10, pady=2)
        
        # Memory
        self.mem_label = tk.Label(
            info_frame,
            text="Memory: ---%",
            font=("Arial", 10),
            bg="#FFF0F5",
            anchor="w"
        )
        self.mem_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        
        self.mem_bar = ttk.Progressbar(
            info_frame,
            length=200,
            mode='determinate'
        )
        self.mem_bar.grid(row=1, column=1, padx=10, pady=2)
        
        # Temperature
        self.temp_label = tk.Label(
            info_frame,
            text="Temp: --°C",
            font=("Arial", 10),
            bg="#FFF0F5",
            anchor="w"
        )
        self.temp_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)
        
        self.temp_bar = ttk.Progressbar(
            info_frame,
            length=200,
            mode='determinate'
        )
        self.temp_bar.grid(row=2, column=1, padx=10, pady=2)
    
    def create_controls(self):
        """Create control buttons"""
        control_frame = tk.Frame(self.main_frame, bg="#FFE5E5")
        control_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        moods = [
            ("😊 Happy", "happy"),
            ("🤩 Excited", "excited"),
            ("😴 Sleepy", "sleepy"),
            ("😰 Worried", "worried")
        ]
        
        for i, (text, mood) in enumerate(moods):
            btn = tk.Button(
                control_frame,
                text=text,
                font=("Arial", 10),
                bg="#FFB6C1",
                fg="#333",
                relief=tk.RAISED,
                command=lambda m=mood: self.change_mood(m),
                padx=10,
                pady=5
            )
            btn.grid(row=0, column=i, padx=5)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_label = tk.Label(
            self.main_frame,
            text="🍓 Raspberry Pi is running smoothly!",
            font=("Arial", 10),
            bg="#FFB6C1",
            fg="#333",
            relief=tk.SUNKEN,
            anchor="w"
        )
        self.status_label.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
    
    def change_mood(self, mood):
        """Change character mood"""
        self.mood = mood
        self.draw_character()
        
        messages = {
            "happy": "🍓 Feeling great!",
            "excited": "🎉 So excited!",
            "sleepy": "😴 Time for a nap...",
            "worried": "😰 Is everything okay?"
        }
        self.status_label.config(text=messages[mood])
    
    def animate(self):
        """Main animation loop"""
        # Bounce animation
        self.bounce_offset += self.bounce_direction * 0.5
        if abs(self.bounce_offset) > 5:
            self.bounce_direction *= -1
        
        # Blink randomly
        if random.random() < 0.02:
            self.blink_state = not self.blink_state
        elif self.blink_state and random.random() < 0.5:
            self.blink_state = False
        
        # Random mood changes
        self.expression_timer += 1
        if self.expression_timer > 200 and random.random() < 0.01:
            moods = ["happy", "excited", "sleepy", "worried"]
            self.mood = random.choice(moods)
            self.expression_timer = 0
        
        self.draw_character()
        self.root.after(50, self.animate)
    
    def update_system_info(self):
        """Update system information"""
        try:
            # CPU usage
            cpu = psutil.cpu_percent(interval=0.1)
            self.cpu_label.config(text=f"CPU: {cpu:.1f}%")
            self.cpu_bar['value'] = cpu
            
            # Memory usage
            mem = psutil.virtual_memory().percent
            self.mem_label.config(text=f"Memory: {mem:.1f}%")
            self.mem_bar['value'] = mem
            
            # Temperature (Raspberry Pi specific)
            try:
                temp_output = subprocess.check_output(['vcgencmd', 'measure_temp'])
                temp = float(temp_output.decode().split('=')[1].split("'")[0])
                self.temp_label.config(text=f"Temp: {temp:.1f}°C")
                self.temp_bar['value'] = min(temp, 100)
                
                # Change mood based on temperature
                if temp > 70 and self.mood != "worried":
                    self.mood = "worried"
                    self.status_label.config(text="😰 Getting warm!")
            except:
                self.temp_label.config(text="Temp: N/A")
            
            # Update system load status
            if cpu < 30 and mem < 50:
                self.status_label.config(text="🍓 All systems normal!")
            elif cpu > 70 or mem > 80:
                self.status_label.config(text="⚡ Working hard!")
        
        except Exception as e:
            print(f"Error updating system info: {e}")
        
        self.root.after(2000, self.update_system_info)

def main():
    root = tk.Tk()
    app = CuteRaspberryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
