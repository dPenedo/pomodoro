import time
import threading
import tkinter as tk
from tkinter import ttk
import pygame





pygame.mixer.init()
def music():
    pygame.mixer.music.load("sonido/sonido.mp3")
    pygame.mixer.music.play(loops=0)

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        #self.root.tk.call('wm','iconphoto', self.root._w, PhotoImage(file='tomate.png'))
        self.root.iconphoto(False, tk.PhotoImage(file='img/tomate.png'))

        # Estilo de pestañas y botones
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))
        
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        # Pestañas
        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        # Tiempo en pomodoro

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        # Tiempo en descanso corto 
        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=20)
        # Tiempo en descanso largo 
        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=20)
        
        # Sonidos
        self.sonido_alerta = pygame.mixer.Sound('sonido/alerta1.mp3')
        self.sonido_alerta2 = pygame.mixer.Sound('sonido/alerta2.mp3')

        
        # Texto de las pestañas
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        
        
        # Formato del grid
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        

        # Botones
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)
        
        self.pause_button = ttk.Button(self.grid_layout, text="Pause", command=self.pause_clock)
        self.pause_button.grid(row=0, column=1)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=2)
        
        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=3)
        
        self.music_button = ttk.Button(self.grid_layout, text="Music", command=music)
        self.music_button.grid(row=1, column=3)


        self.pomodoro_counter_label = ttk.Label(self.grid_layout,text="Pomodoros = 0", font=("Ubuntu", 16))
        self.pomodoro_counter_label.grid(row=1, column =0, columnspan= 3, pady=10)

        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False


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

        if timer_id == 1:
            full_seconds = 60 * 25
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



        elif timer_id ==2:
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


        elif timer_id == 3:
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
        self.stopped = True
        self.running = False


PomodoroTimer()

