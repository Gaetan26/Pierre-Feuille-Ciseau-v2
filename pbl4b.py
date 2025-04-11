# -*- coding: utf-8 -*-
from random import randint
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import pygame, time
from threading import Thread

pygame.init()
pygame.mixer.init()

# Fenêtre principale
fenetre = tk.Tk()
fenetre.geometry('375x450')
fenetre.title("Pierre, Papier, Ciseaux")

# Scores globaux
humanPoint = 0
computerPoint = 0
running = False

def running_false():
    global running
    running = False
    fenetre.destroy()

def music():
    global humanPoint, computerPoint, running
    songs = {
        'winning': 'winning-218995.mp3',
        'losing': 'game-over-160612.mp3',
        'gaming': 'the-return-of-the-8-bit-era-301292.mp3',
    }

    pygame.mixer.music.load(songs["gaming"])
    pygame.mixer.music.play()

    while running:
        if humanPoint == 15:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(songs["winning"])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            return None
        
        elif computerPoint == 15:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(songs["losing"])
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            return None

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    
    pygame.mixer.music.stop()
    return None

def gameScreen(player_name):
    global humanPoint, computerPoint, running
    humanPoint = 0
    computerPoint = 0
    global dd, versus, rock, paper, scissors, well
    global rounds_since_last_well
    rounds_since_last_well = 0  # Nombre de tours depuis la dernière utilisation du puits

    for child in fenetre.winfo_children():
        child.destroy()

    def raiseScore(computer, human):
        global humanPoint, computerPoint
        if computer == 1 and human == 2:
            humanPoint += 1
        elif computer == 2 and human == 1:
            computerPoint += 1
        elif computer == 1 and human == 3:
            computerPoint += 1
        elif computer == 3 and human == 1:
            humanPoint += 1
        elif computer == 3 and human == 2:
            computerPoint += 1
        elif computer == 2 and human == 3:
            humanPoint += 1
        elif computer == 1 and human == 4:
            humanPoint += 2
        elif computer == 3 and human == 4:
            humanPoint += 2
        elif computer == 2 and human == 4:
            computerPoint += 2

        if humanPoint >= 15:
            tk.messagebox.showinfo("Victoire", f"{player_name} a gagné ! 🎉")
            gameScreen(player_name)
        elif computerPoint >= 15:
            tk.messagebox.showinfo("Défaite", "La machine a gagné ! 🤖")
            gameScreen(player_name)

    def update_well_button():
        if rounds_since_last_well >= 4:
            well_button.config(state=tk.NORMAL)
        else:
            well_button.config(state=tk.DISABLED)

    def play(human):
        global rounds_since_last_well
        computer = randint(1, 3)
        if computer == 1:
            lab3.configure(image=rock)
        elif computer == 2:
            lab3.configure(image=paper)
        else:
            lab3.configure(image=scissors)

        raiseScore(computer, human)
        humanScore.configure(text=str(humanPoint))
        computerScore.configure(text=str(computerPoint))

        if human != 4:  # Toute action SAUF puits
            rounds_since_last_well += 1
        else:
            rounds_since_last_well = 0  # Réinitialise après usage du puits

        update_well_button()

    def play_rock():
        lab1.configure(image=rock)
        play(1)

    def play_paper():
        lab1.configure(image=paper)
        play(2)

    def play_scissors():
        lab1.configure(image=scissors)
        play(3)

    def play_well():
        lab1.configure(image=well)
        play(4)

    # Chargement des images redimensionnées
    imagesize = (112, 112)
    dd = ImageTk.PhotoImage(Image.open('dd.png').resize(imagesize))
    versus = ImageTk.PhotoImage(Image.open('versus.gif').resize(imagesize))
    rock = ImageTk.PhotoImage(Image.open('rock.png').resize(imagesize))
    paper = ImageTk.PhotoImage(Image.open('paper.png').resize(imagesize))
    scissors = ImageTk.PhotoImage(Image.open('cisor.png').resize(imagesize))
    well = ImageTk.PhotoImage(Image.open('well.png').resize(imagesize))

    # Interface
    tk.Label(fenetre, text=player_name + " :", font=("Helvetica", 16)).grid(row=0, column=0)
    tk.Label(fenetre, text="Machine :", font=("Helvetica", 16)).grid(row=0, column=2)
    tk.Label(fenetre, text="Pour jouer, cliquez sur une des icônes ci-dessous.").grid(row=3, columnspan=3, pady=5)

    humanScore = tk.Label(fenetre, text="0", font=("Helvetica", 16))
    humanScore.grid(row=1, column=0)
    tk.Label(fenetre, text="versus", font=("Helvetica", 16)).grid(row=1, column=1)
    computerScore = tk.Label(fenetre, text="0", font=("Helvetica", 16))
    computerScore.grid(row=1, column=2)

    lab1 = tk.Label(fenetre, image=dd)
    lab1.grid(row=2, column=0)

    tk.Label(fenetre, image=versus).grid(row=2, column=1)

    lab3 = tk.Label(fenetre, image=dd)
    lab3.grid(row=2, column=2)

    tk.Button(fenetre, image=rock, command=play_rock, relief="groove").grid(row=4, column=0)
    tk.Button(fenetre, image=paper, command=play_paper, relief="groove").grid(row=4, column=1)
    tk.Button(fenetre, image=scissors, command=play_scissors, relief="groove").grid(row=4, column=2)

    well_button = tk.Button(fenetre, image=well, command=play_well, state=tk.DISABLED)
    well_button.grid(row=5, column=1)

    tk.Button(fenetre, text='Quitter', command=running_false).grid(row=5, column=2, pady=10, ipadx=22)

    running = True
    Thread(target=music).start()
    update_well_button()  # Vérifie au démarrage

# Accueil
player_name_var = tk.StringVar()
tk.Label(fenetre, text="Entrez votre nom :").pack(pady=10)
name_entry = tk.Entry(fenetre, textvariable=player_name_var)
name_entry.pack()
tk.Button(fenetre, text="Click me!", command=lambda: gameScreen(player_name_var.get())).pack(pady=20)
tk.Label(fenetre,text="").pack()

# Boucle principale
fenetre.protocol("WM_DELETE_WINDOW", running_false)
fenetre.mainloop()