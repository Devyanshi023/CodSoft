import tkinter as tk
import random

options = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0

def response(user_choice):
    user_choice = user_choice.lower()
    if user_choice in options:
        computer_choice = random.choice(options)
        return computer_choice
    else:
        return "Invalid choice"

def win(user_choice, computer_choice):
    global player_score, computer_score
    if (user_choice == "rock" and computer_choice == "scissors") or (user_choice == "scissors" and computer_choice == "paper") or (user_choice == "paper" and computer_choice == "rock"):
        player_score += 1
        return "User won"
    elif (user_choice == "scissors" and computer_choice == "rock") or (user_choice == "paper" and computer_choice == "scissors") or (user_choice == "rock" and computer_choice == "paper"):
        computer_score += 1
        return "Computer won"
    elif (user_choice == computer_choice):
        return "It's a tie!"
    else:
        return "Invalid choice"

def update_score():
    player_score_label.config(text="Player: " + str(player_score))
    computer_score_label.config(text="Computer: " + str(computer_score))

def play_game():
    
    user_choice = user_choice_var.get().lower()
    computer_choice = response(user_choice)
    result = win(user_choice, computer_choice)
    result_var.set(result)
    computer_choice_var.set(computer_choice)
    update_score()

def fb():
    feedback = feedback_var.get().lower()
    if feedback == "yes":
        feedback_label.config(text="Thank you!")
    elif feedback == "no":
        feedback_label.config(text="We are Sorry!")

def clear():
    user_choice_entry.delete(0, tk.END)
    computer_choice_label.delete(0, tk.END)
    result_label.delete(0, tk.END)

def reset_game():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    update_score()
    result_var.set("")
    computer_choice_var.set("")
    user_choice_var.set("")
    feedback_var.set("")
    feedback_label.config(text="")


root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("450x600")

head_label = tk.Label(root, text="Rock Paper Scissors game", font=("Helvetica", 14, "bold"))
head_label.grid(row=0, column=0, columnspan= 5, pady=15)

instructions_label = tk.Label(root, text="Instructions", font=("Helvetica", 12, "bold"))
instructions_label.grid(row=1, column=0, columnspan= 5, pady=15)

cond1_label = tk.Label(root, text="Rock vs Paper >>>> Paper wins", font=("Helvetica", 10, "bold"))
cond1_label.grid(row=2, column=0, columnspan= 5, pady=5)

cond2_label = tk.Label(root, text="Rock vs Scissors >>>> Rock wins", font=("Helvetica", 10, "bold"))
cond2_label.grid(row=3, column=0, columnspan= 5, pady=5)

cond3_label = tk.Label(root, text="Paper vs Scissors >>>> Scissors win", font=("Helvetica", 10, "bold"))
cond3_label.grid(row=4, column=0, columnspan= 5, pady=5)

user_choice_var = tk.StringVar()
user_choice_head = tk.Label(root, text="Player")
user_choice_head.grid(row=5, column=0, sticky=tk.E)

user_choice_entry = tk.Entry(root, textvariable=user_choice_var)
user_choice_entry.grid(row=5, column=1, padx=10, pady= 10)

computer_choice_var = tk.StringVar()
computer_choice_head = tk.Label(root, text="Computer")
computer_choice_head.grid(row=6, column=0, sticky=tk.E)

computer_choice_label = tk.Entry(root, textvariable=computer_choice_var)
computer_choice_label.grid(row=6, column=1, padx=10, pady= 10)

result_var = tk.StringVar()  
result_head = tk.Label(root, text="Result")
result_head.grid(row=7, column=0, sticky=tk.E)

result_label = tk.Entry(root, textvariable=result_var)
result_label.grid(row=7, column=1, pady=10)

enter_button = tk.Button(root, text="Enter answer", command=play_game)
enter_button.grid(row=8, column=0, pady=10)

clear_button = tk.Button(root, text="Play again", command=clear)
clear_button.grid(row=8, column=1, pady=10)

reset_button = tk.Button(root, text="New Game", command=reset_game)
reset_button.grid(row=8, column=2, pady=10)

scoreboard_label = tk.Label(root, text="Scoreboard", font=("Helvetica", 16))
scoreboard_label.grid(row=9, column=0, columnspan=3, pady=10)

player_score_label = tk.Label(root, text="Player: " + str(player_score), font=("Helvetica", 12))
player_score_label.grid(row=10, column=0, columnspan=3)

computer_score_label = tk.Label(root, text="Computer: " + str(computer_score), font=("Helvetica", 12))
computer_score_label.grid(row=11, column=0, columnspan=3)

feedback_var = tk.StringVar()

fb_label = tk.Label(root, text="Do you like this game?", font=("Helvetica", 10, "bold"))
fb_label.grid(row=12, column=0, columnspan= 5, pady=5)

feedback_head = tk.Label(root, text="Feedback ( yes / no )")
feedback_head.grid(row=13, column=0, sticky=tk.E)

feedback_entry = tk.Entry(root, textvariable=feedback_var)
feedback_entry.grid(row=13, column=1, pady=5)

submit_button = tk.Button(root, text="Submit", command= fb)
submit_button.grid(row=14, column=1, pady=5)

feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
feedback_label.grid(row=15, column=1, pady=5)

root.mainloop()
