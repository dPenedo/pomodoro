import time
import threading
import tkinter as tk
from tkinter import ttk 
from tkinter import *
from PIL import ImageTk, Image
import pygame



pygame.mixer.init()
pygame.mixer.music.load("sonido/sonido.mp3")
# Sound

# Colors:

# Colors
dark= '#be161c'
light= '#e05648'
accent = '#A5C9FF'
# Font
font = 'Inter'



class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        # Size
        self.root.geometry("600x400")
        self.root.title("Pomodoro Timer")
        #self.root.tk.call('wm','iconphoto', self.root._w, PhotoImage(file='tomate.png'))
        self.root.iconphoto(False, tk.PhotoImage(file='img/tomate.png'))

        # Estilo de pestañas y botones
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", background=light, font=(font, 14))
        self.s.configure("TButton", font=(font, 14), background=light)
        self.s.map('TButton', background=[('active',dark)])

        self.s.map("TNotebook.Tab", background=[("selected", dark)])
        self.root.configure(bg=dark)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)
        
        # Pestañas
        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        
        # Sonidos
        self.sonido_alerta = pygame.mixer.Sound('sonido/alerta1.mp3')
        self.sonido_alerta2 = pygame.mixer.Sound('sonido/alerta2.mp3')

        
        # Texto de las pestañas
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.center_frame = Frame(self.root,  bg=dark)
        self.center_frame.pack(side=TOP, pady=10)
        
        # The tomato image
        self.img_pomodoro = Image.open("img/tomate.png")
        self.resizing_pomodoro = self.img_pomodoro.resize((150, 150), Image.ANTIALIAS)
        self.final_pomodoro = ImageTk.PhotoImage(self.resizing_pomodoro)
        self.center_frame.label = Label(self.tab1, image=self.final_pomodoro)
        self.center_frame.label.pack()
        # Short pause image 
        self.img_short_pause = Image.open("img/pausa_corta.png")
        self.resizing_short = self.img_short_pause.resize((150, 150), Image.ANTIALIAS)
        self.final_short_pause = ImageTk.PhotoImage(self.resizing_short)
        self.center_frame.label = Label(self.tab2, image=self.final_short_pause)
        self.center_frame.label.pack()
        # Long pause image 
        self.img_long_pause = Image.open("img/pausa_larga.png")
        self.resizing_long_pause = self.img_long_pause.resize((150, 150), Image.ANTIALIAS)
        self.final_long_pause = ImageTk.PhotoImage(self.resizing_long_pause)
        self.center_frame.label = Label(self.tab3, image=self.final_long_pause)
        self.center_frame.label.pack()

        # Sound icon
        self.sound_icon = PhotoImage(file = "img/sonido.png")
        self.sound_icon_resized = self.sound_icon.subsample(18)
        
        # Mute icon
        self.mute_icon = Image.open("img/mute.png")
        self.resizing_mute = self.mute_icon.resize((27, 27), Image.ANTIALIAS)

        self.mute_icon_resized = ImageTk.PhotoImage(self.resizing_mute)
        

        # Pomodoro time
        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=('hack', 38), foreground=dark)
        self.pomodoro_timer_label.pack( pady=5)

        # Short rest time 
        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=('hack', 38), foreground=dark)
        self.short_break_timer_label.pack(pady=5)
        # Long rest time 
        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=('hack', 38), foreground=dark)
        self.long_break_timer_label.pack(pady=5)

        # Formato del grid
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        

        # Buttons
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)
        
        self.pause_button = ttk.Button(self.grid_layout, text="Pause", command=self.pause_clock)
        self.pause_button.grid(row=0, column=1)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=2)
        
        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=3)
        
        self.music_button = ttk.Button(self.grid_layout, image=self.sound_icon_resized, command=self.music)
        self.music_button.grid(row=1, column=3)
        

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros = 0", font=('hack', 16), foreground=dark)
        self.pomodoro_counter_label.grid(row=1, column =0, columnspan= 3, pady=10)
        


        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False
        self.playing_sound = True
        self.music_pause = False
        

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        self.running = True
        timer_id = self.tabs.index(self.tabs.select()) +1
        
        # Pomodoro running
        if timer_id == 1:
            full_seconds = 60 * 25
            pygame.mixer.music.unpause()
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1

            if full_seconds == 0 and not self.stopped:
                self.sonido_alerta.play()
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros = {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()


        # On short pause
        elif timer_id ==2:
            pygame.mixer.music.pause()
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.short_break_timer_label.configure(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if full_seconds == 0 and not self.stopped:
                self.sonido_alerta2.play()
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

        # On long pause
        elif timer_id == 3:
            pygame.mixer.music.pause()
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.configure(text=f'{minutes:02d}:{seconds:02d}')
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid timer id")



    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0:
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab ==1:
            self.short_break_timer_label.config(text="05:00")
        elif current_tab ==2:
            self.long_break_timer_label.config(text="15:00")

        self.stopped = True
        self.skipped = True


    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.running = False

    def pause_clock(self):
        if self.running and self.music_pause == False:
            self.stopped = True
            self.running = False

    def music(self):
        if self.playing_sound:
            pygame.mixer.music.load("sonido/sonido.mp3")
            pygame.mixer.music.play(-1)
            self.playing_sound=False
            self.music_button['image'] = self.sound_icon_resized

        else:
            pygame.mixer.music.pause()
            self.playing_sound=True

            self.music_button['image'] = self.mute_icon_resized


         

    
    def pause(self):
        self.music_pause = True
        pygame.mixer.music.pause()

    



PomodoroTimer()

