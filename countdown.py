import tkinter as tk
from PIL import Image, ImageTk

# constants
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 10
reps = 0
timer = None
COFFEE = "#A78989"
is_running = False
remaining_time = 0

def start_next_session():
    global reps, is_running, remaining_time
    reps += 1
    is_running = True

    if reps % 8 == 0:
        countdown_time = LONG_BREAK_MIN * 60
        canvas.itemconfig(title_text, text="Long Break")
    elif reps % 2 == 0:
        countdown_time = SHORT_BREAK_MIN * 60
        canvas.itemconfig(title_text, text="Short Break")
    else:
        countdown_time = WORK_MIN * 60
        canvas.itemconfig(title_text, text="Pomodoro")

    update_marks()
    remaining_time = countdown_time
    count_down(remaining_time)

def count_down(count):
    global timer, remaining_time
    remaining_time = count
    if not is_running:
        return
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        remaining_time = 0
        start_next_session()

def toggle_timer():
    global is_running, remaining_time
    if not is_running:
        is_running = True
        start_button.config(text="Pause")
        if remaining_time > 0:
            count_down(remaining_time)
        else:
            start_next_session()
    else:
        is_running = False
        start_button.config(text="Start")
        if timer:
            window.after_cancel(timer)

def reset_timer():
    global timer, is_running, reps, remaining_time
    if timer:
        window.after_cancel(timer)
    reps = 0
    is_running = False
    remaining_time = 0
    canvas.itemconfig(title_text, text="Pomodoro")
    canvas.itemconfig(timer_text, text="00:00")
    canvas.itemconfig(mark_text, text="")
    start_button.config(text="Start")

def update_marks():
    marks = " \u2022 " * (reps // 2)
    canvas.itemconfig(mark_text, text=marks.strip())

# UI setup
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("800x600")

original_bg_image = Image.open("landscape.png")
bg_photo = ImageTk.PhotoImage(original_bg_image.resize((800, 600)))

canvas = tk.Canvas(window, width=800, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_image_item = canvas.create_image(0, 0, image=bg_photo, anchor="nw")

title_text = canvas.create_text(400, 100, text="Pomodoro", font=("Courier New", 28))
mark_text = canvas.create_text(400, 140, text="", font=("Courier New", 20), fill="black")
timer_text = canvas.create_text(400, 200, text="00:00", font=("Courier New", 28))

start_button = tk.Button(window, text="Start", command=toggle_timer, font=("Courier New", 12), bg=COFFEE, width=6, height=1)
canvas.create_window(360, 350, window=start_button)

reset_button = tk.Button(window, text="Reset", command=reset_timer, font=("Courier New", 12), bg=COFFEE, width=6, height=1)
canvas.create_window(440, 350, window=reset_button)

window.mainloop()
