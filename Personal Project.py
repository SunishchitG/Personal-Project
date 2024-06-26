from tkinter import *
import random
import time

sentences = open('sentences.txt', 'r').read().split('\n')
prev_line = ""
user_line = ""
end_of_typing = False
starting_time = 0
beginning_time = 0
all_speeds = []
reset_timer = 0;

def assign_a_line(arr_sentences):
    global prev_line
    line = random.choice(arr_sentences)
    if prev_line == line:
        line = random.choice(arr_sentences)
    prev_line = line
    return line

def start_calculating(event):
    global starting_time, beginning_time, reset_timer
    global end_of_typing, user_line, text_to_display
    if end_of_typing:
        print('Cannot Type Further')
        return
    if starting_time == 0:
        starting_time = time.time()

    if beginning_time == 0:
        beginning_time = time.time()

    if event.keysym == "BackSpace":
        user_line = user_line[0: len(user_line)-1]
        starting_time = time.time()
        return

    else:
        user_line += event.char
        end_time = time.time()
        gap = end_time - starting_time
        if gap > 5:
            ending_msg = 'You took too long. End of typing period. Click on Reset button to start again'
            sentence.config(fg='yellow')
            typing_area.config(highlightcolor='red', highlightbackground='red')
            sentence.config(text=ending_msg)
            return

        text_len = len(user_line)
        if text_len == len(text_to_display):
            end_of_typing = True
            is_accu = check_accuracy(user_line, text_to_display)
            seconds_elapsed = end_time - beginning_time
            chars_per_second = round(text_len / seconds_elapsed)
            words_per_minute = chars_per_second * (60 / 5)
            show_result(is_accu, words_per_minute)
            all_speeds.append(words_per_minute)
            reset_timer = window.after(2000, reset_app)

    starting_time = time.time()


def check_accuracy(user_line_, app_line):
    if user_line_ == app_line:
        return True
    else:
        return False


def show_result(boolean, wpm):
    if boolean:
        typing_area.config(highlightcolor='green', highlightbackground='green')
        sentence.config(text=f" Speed: {wpm} wpm WITHOUT ERRORS", fg='green')
    else:
        typing_area.config(highlightcolor='red', highlightbackground='red')
        sentence.config(text=f" Speed: {wpm} wpm WITH ERRORS", fg='red')


def reset_app():
    global end_of_typing, starting_time, user_line, reset_timer
    global prev_line, text_to_display, beginning_time

    window.after_cancel(reset_timer)
    starting_time = 0
    beginning_time = 0
    reset_timer = 0
    end_of_typing = False
    user_line = ""
    prev_line = ""
    text_to_display = assign_a_line(sentences)
    sentence.config(text=text_to_display, fg=FG2)
    typing_area.delete('1.0', 'end')
    typing_area.config(highlightcolor=FG, highlightbackground=FG)


def show_overall_speed():
    global reset_timer
    window.after_cancel(reset_timer)
    if len(all_speeds) != 0:
        sum_ = sum(all_speeds)
        avg = sum_/len(all_speeds)
        sentence.config(text=f"{int(avg)} wpm", fg='yellow')
    else:
        sentence.config(text="Nothing to Show yet", fg='yellow')

BG = "#041C32"
FG = "#ECB365"
FG2 = "#FF8F56"
FG3 = "#F3A871"

FONT_FAMILY1 = 'Calibri'
FONT_FAMILY2 = 'Helvetica'

FONT_SIZE1 = 14
FONT_SIZE2 = 18
FONT_SIZE3 = 24

FONT_STYLE1 = 'normal'
FONT_STYLE2 = 'italic'

PARA_FONT = (FONT_FAMILY1, FONT_SIZE1, FONT_STYLE1)
PARA_FONT2 = (FONT_FAMILY1, 12, FONT_STYLE2)
HEAD_FONT = (FONT_FAMILY2, FONT_SIZE3, FONT_STYLE2)
HEAD2_FONT = (FONT_FAMILY2, FONT_SIZE2, FONT_STYLE1)

heading = "GET YOUR TYPING SPEED TESTED"
text_to_display = assign_a_line(sentences)
instructions = """

"""

window = Tk()
window.title('Welcome to Typing Speed Calculator!')
window.config(bg=BG, pady=10, padx=50)

heading = Label(text=heading, font=HEAD_FONT, bg=BG, fg=FG, padx=10, pady=10)
sentence = Label(text=text_to_display, font=HEAD2_FONT, bg=BG, fg=FG2, pady=10, padx=10, wraplength=800)
instruction = Label(text=instructions, font=PARA_FONT2, fg=FG, bg=BG)

typing_area = Text(font=PARA_FONT, bg=BG, fg=FG, width=80, height=10, wrap='w',
                   highlightcolor=FG, highlightthickness=4, highlightbackground=FG,
                   padx=5, pady=5)
typing_area.bind('<KeyPress>', start_calculating)

reset_btn = Button(text='Reset Application', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=reset_app)
overall_btn = Button(text='Show Average Speed', fg=FG, bg=BG, font=PARA_FONT,
                   highlightbackground=FG, highlightcolor=FG, highlightthickness=0, border=3,
                   command=show_overall_speed)

heading.grid(row=0, column=0, columnspan=2)
sentence.grid(row=1, column=0, columnspan=2)
instruction.grid(row=2, column=0, columnspan=2)
typing_area.grid(row=3, column=0, columnspan=2)
reset_btn.grid(row=4, column=0, sticky='ew')
overall_btn.grid(row=4, column=1, sticky='ew')

window.mainloop()