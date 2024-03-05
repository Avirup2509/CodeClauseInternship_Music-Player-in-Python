import os
import tkinter as tk
from tkinter import filedialog
import pygame
import mutagen.mp3
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x400")

        pygame.init()  # Initialize pygame
        pygame.mixer.init()    # Initialize the mixer

        self.music_folder = ""
        self.current_song_index = 0
        self.playing = False
        self.paused = False

        self.setup_ui()

    def setup_ui(self):
        # Logo
        logo_image = Image.open("logo.png").resize((150, 100))
        self.logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.pack(pady=10)

        # Select Folder Button
        self.select_folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=5)

        # Music Control Buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        play_image = Image.open("play.png").resize((40, 40))
        self.play_icon = ImageTk.PhotoImage(play_image)
        self.play_button = tk.Button(control_frame, image=self.play_icon, command=self.toggle_play)
        self.play_button.grid(row=0, column=0, padx=10)

        pause_image = Image.open("pause.png").resize((40, 40))
        self.pause_icon = ImageTk.PhotoImage(pause_image)
        self.pause_button = tk.Button(control_frame, image=self.pause_icon, command=self.toggle_play)
        self.pause_button.grid(row=0, column=1, padx=10)

        stop_image = Image.open("stop.png").resize((40, 40))
        self.stop_icon = ImageTk.PhotoImage(stop_image)
        self.stop_button = tk.Button(control_frame, image=self.stop_icon, command=self.stop_music)
        self.stop_button.grid(row=0, column=2, padx=10)

        next_image = Image.open("next.png").resize((40, 40))
        self.next_icon = ImageTk.PhotoImage(next_image)
        self.next_button = tk.Button(control_frame, image=self.next_icon, command=self.next_song)
        self.next_button.grid(row=0, column=3, padx=10)

        # Volume Control
        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=5)

        self.volume_label = tk.Label(volume_frame, text="Volume:")
        self.volume_label.grid(row=0, column=0)

        self.volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.grid(row=0, column=1)

        # Song Information
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)

        self.current_song_label = tk.Label(info_frame, text="")
        self.current_song_label.grid(row=0, column=0, padx=10)

        self.song_duration_label = tk.Label(info_frame, text="")
        self.song_duration_label.grid(row=0, column=1, padx=10)

        # Update UI periodically
        self.update_ui()

    def select_folder(self):
        self.music_folder = filedialog.askdirectory()
        print("Selected Folder:", self.music_folder)
        self.load_music_files()

    def load_music_files(self):
        self.music_files = []
        if self.music_folder:
            for file in os.listdir(self.music_folder):
                if file.endswith(".mp3"):
                    self.music_files.append(os.path.join(self.music_folder, file))
            if self.music_files:
                self.current_song_index = 0
                self.update_current_song_label()
                self.update_song_duration_label()

    def toggle_play(self):
        if not self.playing:
            if self.music_files:
                pygame.mixer.music.load(self.music_files[self.current_song_index])
                pygame.mixer.music.set_volume(self.volume_slider.get() / 100)
                pygame.mixer.music.play()
                self.playing = True
                self.paused = False
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.paused = True

    def stop_music(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False

    def next_song(self):
        if self.playing:
            self.stop_music()
            self.current_song_index = (self.current_song_index + 1) % len(self.music_files)
            self.toggle_play()

    def set_volume(self, value):
        if self.playing:
            pygame.mixer.music.set_volume(int(value) / 100)

    def update_current_song_label(self):
        if self.music_files:
            current_song = os.path.basename(self.music_files[self.current_song_index])
            self.current_song_label.config(text="Current Song: " + current_song)

    def update_song_duration_label(self):
        if self.music_files:
            current_song = self.music_files[self.current_song_index]
            audio = mutagen.mp3.MP3(current_song)
            duration_seconds = audio.info.length
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            self.song_duration_label.config(text=f"Duration: {minutes}:{seconds:02d}")

    def set_song_position(self, value):
        if self.playing:
            current_song = self.music_files[self.current_song_index]
            audio = mutagen.mp3.MP3(current_song)
            duration_seconds = audio.info.length
            position_seconds = int(value) * duration_seconds / 100
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(start=position_seconds)

    def update_ui(self):
        if self.playing:
            self.update_current_song_label()
            self.update_song_duration_label()

        self.root.after(1000, self.update_ui)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
