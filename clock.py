from tkinter import *
from tkinter import messagebox
import time
import math
from datetime import datetime
import threading

root = Tk()
root.title("Smart Clock App")
root.geometry("1000x1000")
root.configure(bg='#1a1a2e')

nav_frame = Frame(root, bg="#1a1a2e")
nav_frame.pack(pady=10)

current_view = StringVar()
current_view.set("clock")

button_style = {"font": ("Comic Sans MS", 21, "bold"), "bg": "#05f7e3", "fg": "#050124", "padx": 18, "pady": 10}

Button(nav_frame, text="Clock", command=lambda: show_frame(clock_frame), **button_style).pack(side=LEFT, padx=10)
Button(nav_frame, text="Alarm", command=lambda: show_frame(alarm_frame), **button_style).pack(side=LEFT, padx=10)
Button(nav_frame, text="Timer", command=lambda: show_frame(timer_frame), **button_style).pack(side=LEFT, padx=10)
Button(nav_frame, text="Stopwatch", command=lambda: show_frame(stopwatch_frame), **button_style).pack(side=LEFT, padx=10)

frame_container = Frame(root, bg="#1a1a2e")
frame_container.pack(fill="both", expand=True)

clock_frame = Frame(frame_container, bg="#1a1a2e")

# Digital Clock
clock_info = Frame(clock_frame, bg="#1a1a2e")
clock_info.pack(pady=20)

digital_clock = Label(clock_info, font=("Orbitron", 58, "bold"), fg="#f7f705", bg="#1a1a2e")
digital_clock.pack()

day_label = Label(clock_info, font=("Georgia", 24, "italic"), fg="#05f7e3", bg="#1a1a2e")
day_label.pack()

date_label = Label(clock_info, font=("Georgia", 30), fg="#33ff05", bg="#1a1a2e")
date_label.pack(pady=10)

def update_digital_clock():
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%d - %m - %Y")
    day_str = now.strftime("%A")
    tz_str = now.strftime("%Z") or time.tzname[0]

    digital_clock.config(text=time_str)
    date_label.config(text=date_str)
    day_label.config(text=f"{tz_str}  |  {day_str}")
    root.after(1000, update_digital_clock)

update_digital_clock()

# Analog Clock
canvas = Canvas(clock_frame, width=420, height=420, bg="#1a1a2e", highlightthickness=0)
canvas.pack(pady=16)
center_x, center_y, radius = 210, 210, 180

def draw_analog_clock():
    canvas.delete("all")
    canvas.create_oval(center_x - radius - 10, center_y - radius - 10,
                       center_x + radius + 10, center_y + radius + 10,
                       width=10, outline="#f39c12")
    canvas.create_oval(center_x - radius, center_y - radius,
                       center_x + radius, center_y + radius,
                       width=6, outline="#570302")
    for i in range(1, 13):
        angle = math.pi / 6 * (i - 3)
        x = center_x + math.cos(angle) * (radius - 30)
        y = center_y + math.sin(angle) * (radius - 30)
        canvas.create_text(x, y, text=str(i), font=("Georgia", 30, "italic"), fill="#ffffff")

    now = datetime.now()
    h, m, s = now.hour % 12, now.minute, now.second
    sec_angle = math.radians((s / 60) * 360 - 90)
    min_angle = math.radians((m / 60) * 360 - 90)
    hour_angle = math.radians(((h + m / 60) / 12) * 360 - 90)

    canvas.create_line(center_x, center_y, center_x + math.cos(sec_angle) * (radius - 18),
                       center_y + math.sin(sec_angle) * (radius - 18), fill="#e74c3c", width=3)
    canvas.create_line(center_x, center_y, center_x + math.cos(min_angle) * (radius - 45),
                       center_y + math.sin(min_angle) * (radius - 45), fill="#2980b9", width=6)
    canvas.create_line(center_x, center_y, center_x + math.cos(hour_angle) * (radius - 75),
                       center_y + math.sin(hour_angle) * (radius - 75), fill="#ffffff", width=8)

    canvas.create_oval(center_x - 8, center_y - 8, center_x + 8, center_y + 8, fill="#ffffff")
    root.after(1000, draw_analog_clock)

draw_analog_clock()

# ================= ALARM FRAME =================
alarm_frame = Frame(frame_container, bg="#1a1a2e")
Label(alarm_frame, text="⏰ Alarm", font=("Comic Sans MS", 32, "bold"), fg="#05f551", bg="#1a1a2e").pack(pady=27)
Label(alarm_frame, text="Set Time (HH:MM):", font=("Arial", 24), fg="#f5e905", bg="#1a1a2e").pack()
alarm_time = Entry(alarm_frame, width=12, font=("Verdana", 20))
alarm_time.pack(pady=12)

alarm_status = Label(alarm_frame, text="", fg="lightgreen", bg="#1a1a2e", font=("Arial", 16))
alarm_status.pack(pady=10)

def check_alarm():
    while True:
        now = datetime.now().strftime("%H:%M")
        if alarm_time.get() == now:
            alarm_status.config(text="Alarm ringing!", fg="red")
            messagebox.showinfo("Alarm", "\u23F0 Time's up!")
            break
        alarm_status.config(text=f"Waiting for {alarm_time.get()}...", fg="lightgreen")
        time.sleep(1)

Button(alarm_frame, text="Set Alarm", font=("Verdana", 16, "bold"), bg="#f50505", fg="white", command=lambda: threading.Thread(target=check_alarm, daemon=True).start()).pack(pady=5)

# ================= TIMER FRAME =================
timer_frame = Frame(frame_container, bg="#1a1a2e")
Label(timer_frame, text="⏱ Timer", font=("Comic Sans MS", 32, "bold"), fg="#fc9905", bg="#1a1a2e").pack(pady=20)
Label(timer_frame, text="Enter Minutes:", font=("Arial", 28), fg="#d869fa", bg="#1a1a2e").pack()
timer_entry = Entry(timer_frame, font=("Verdana", 20))
timer_entry.pack(pady=10)

timer_display = Label(timer_frame, text="00:00", font=("Helvetica", 28, "bold"), fg="#00ffff", bg="#1a1a2e")
timer_display.pack(pady=10)

timer_running = False
timer_seconds = 0

def reset_timer():
    global timer_seconds, timer_running
    timer_running = False
    timer_seconds = 0
    timer_display.config(text="00:00")
    timer_entry.delete(0, END)  # Optional: clear the entry box


def set_timer():
    global timer_seconds
    try:
        mins = int(timer_entry.get())
        timer_seconds = mins * 60
        mins, secs = divmod(timer_seconds, 60)
        timer_display.config(text=f"{mins:02d}:{secs:02d}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of minutes.")

def countdown():
    global timer_seconds, timer_running
    if timer_seconds > 0 and timer_running:
        mins, secs = divmod(timer_seconds, 60)
        timer_display.config(text=f"{mins:02d}:{secs:02d}")
        timer_seconds -= 1
        root.after(1000, countdown)
    elif timer_seconds == 0 and timer_running:
        timer_display.config(text="00:00")
        messagebox.showinfo("Timer", "\u23F1 Timer finished!")
        timer_running = False

def start_timer():
    global timer_running
    if not timer_running:
        set_timer()
        timer_running = True
        countdown()

def stop_timer():
    global timer_running
    timer_running = False

# Frame to hold Start/Stop buttons centered below the timer
timer_button_frame = Frame(timer_frame, bg="#1a1a2e")
timer_button_frame.pack(pady=10)

Button(timer_button_frame, text="Start", font=("Verdana", 16, "bold"), bg="#f50505", fg="white",
       padx=15, pady=5, command=start_timer).pack(side=LEFT, padx=15)

Button(timer_button_frame, text="Stop", font=("Verdana", 16, "bold"), bg="#05b511", fg="white",
       padx=15, pady=5, command=stop_timer).pack(side=LEFT, padx=15)

Button(timer_button_frame, text="Reset", font=("Verdana", 16, "bold"), bg="#2c2cff", fg="white", padx=15, pady=5, command=reset_timer).pack(side=LEFT, padx=15)



# ================= STOPWATCH FRAME =================
stopwatch_frame = Frame(frame_container, bg="#1a1a2e")
Label(stopwatch_frame, text="⏱ Stopwatch", font=("Comic Sans MS", 32, "bold"), fg="#eefa0c", bg="#1a1a2e").pack(pady=20)

stopwatch_display = Label(stopwatch_frame, text="00:00", font=("Helvetica", 28, "bold"), fg="#56d3fc", bg="#1a1a2e")
stopwatch_display.pack(pady=10)

stopwatch_running = False
stopwatch_seconds = 0

def update_stopwatch():
    global stopwatch_seconds
    if stopwatch_running:
        mins, secs = divmod(stopwatch_seconds, 60)
        stopwatch_display.config(text=f"{mins:02d}:{secs:02d}")
        stopwatch_seconds += 1
        root.after(1000, update_stopwatch)

def start_stopwatch():
    global stopwatch_running
    if not stopwatch_running:
        stopwatch_running = True
        update_stopwatch()

def stop_stopwatch():
    global stopwatch_running
    stopwatch_running = False

def reset_stopwatch():
    global stopwatch_running, stopwatch_seconds
    stopwatch_running = False
    stopwatch_seconds = 0
    stopwatch_display.config(text="00:00")

btn_frame = Frame(stopwatch_frame, bg="#1a1a2e")
btn_frame.pack(pady=10)
Button(btn_frame, text="Start", font=("Verdana", 16, "bold"), bg="#0bd40b", fg="white", command=start_stopwatch).pack(side=LEFT, padx=10)
Button(btn_frame, text="Stop", font=("Verdana", 16, "bold"), bg="#f01707", fg="white", command=stop_stopwatch).pack(side=LEFT, padx=10)
Button(btn_frame, text="Reset", font=("Verdana", 16, "bold"), bg="#fa00f6", fg="white", command=reset_stopwatch).pack(side=LEFT, padx=10)

# ================= VIEW SWITCH FUNCTION =================
def show_frame(frame):
    frame.tkraise()

for frame in (clock_frame, alarm_frame, timer_frame, stopwatch_frame):
    frame.place(in_=frame_container, x=0, y=0, relwidth=1, relheight=1)

show_frame(clock_frame)

root.mainloop()
