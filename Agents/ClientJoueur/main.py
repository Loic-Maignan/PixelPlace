#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  new
#  Created by Ingenuity i/o on 2024/10/18
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys

import tkinter as tk
from PIL import Image, ImageTk  # Importation nécessaire pour gérer les images

from new import *

taille = 100

port = 5670
agent_name = "Joueur1"
device = None
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_io_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, New)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, New)
        # add code here if needed
    except:
        print(traceback.format_exc())

if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = New()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            def quitter(event=None):
                window.quit()

            # Fonction pour gérer la sélection de la couleur
            def choisir_couleur(event):
                x = event.x
                y = event.y
                couleur_selectionnee = couleur_canvas.itemcget(couleur_canvas.find_closest(x, y), "fill")
                print(f"Couleur choisie: {couleur_selectionnee}")
                couleur_var.set(couleur_selectionnee)
            
            def valider():
                x = x_entry.get()
                y = y_entry.get()
                couleur = couleur_var.get()
                print(f"Coordonnées: x={x}, y={y}, couleur={couleur}")
                x_entry.delete(0, tk.END)
                y_entry.delete(0, tk.END)
                message = f"Coordonnées: x={x}, y={y}, couleur={couleur}"
                igs.service_call("Whiteboard", "chat", message, "")
                position = int(x)*taille + int(y)
                print(f"Position: {position}")
                arguments = (str(position), couleur)
                igs.service_call("Tableau", "ajouter", arguments,"")
            
            def changer_name(event):
                user = user_var.get()
                igs.agent_set_name(user)
                igs.service_call("Whiteboard", "chat", f"Changement de nom: {user}", "")
                user_var.set(user)

            # Création de la fenêtre principale en plein écran
            window = tk.Tk()
            window.title("Sélection de couleur")
            window.attributes('-fullscreen', True)
            window.bind("<Escape>", quitter)  # Permet de quitter avec la touche Échap
            window.update()

            # Obtenir la taille actuelle de l'écran
            wx = window.winfo_width()
            wy = window.winfo_height()

            # Calcul des proportions par rapport à une résolution de base
            proportion_x = wx / 1536
            proportion_y = wy / 864

            # Fonction pour ajuster les dimensions selon les proportions
            def ajuster_taille(taille_base, proportion):
                return int(taille_base * proportion)
            
            # Titre principal centré
            titre_text = "WHITEBOARD"
            titre_label = tk.Label(window, text=titre_text, font=("Comic Sans MS", ajuster_taille(20, proportion_x)))

            # Calcul pour centrer le titre horizontalement
            titre_width = ajuster_taille(20 * len(titre_text), proportion_x)  # Largeur estimée du texte
            titre_label.place(x=(wx - titre_width) / 2, y=ajuster_taille(1, proportion_y))
            
            user_text = "Utilisateur: "
            user_label = tk.Label(window, text=user_text, font=("Arial", ajuster_taille(16, proportion_y)))
            user_label.place(x=ajuster_taille(1, proportion_x), y=ajuster_taille(1, proportion_y))
            
            user_var = tk.StringVar(value="Joueur1")
            user_entry = tk.Entry(window, width=ajuster_taille(10, proportion_x), font=("Arial", ajuster_taille(16, proportion_y)), textvariable=user_var)
            user_entry.place(x=ajuster_taille(100, proportion_x), y=ajuster_taille(1, proportion_y))
            
            user_entry.bind("<Return>", changer_name)

            # Grand Canvas pour l'image ou le dessin
            image_canvas = tk.Canvas(window, bg="white", width=ajuster_taille(730, proportion_x), height=ajuster_taille(730, proportion_y))
            image_canvas.place(x=ajuster_taille(1, proportion_x), y=ajuster_taille(50, proportion_y))

            # Charger l'image PNG
            nom_image = "matrice6.png"
            image_originale = Image.open(nom_image)  # Image de la grille
            image_originale_width, image_originale_height = image_originale.size


            # Redimensionner l'image pour l'adapter au Canvas
            image_taille = 730
            image_redimensionnee = image_originale.resize((ajuster_taille(image_taille,proportion_x), ajuster_taille(image_taille,proportion_y)), Image.LANCZOS)  # Ajusté à la taille de la fenêtre
            image_canvas_image = ImageTk.PhotoImage(image_redimensionnee)
            image_canvas.create_image(2, 2, anchor="nw", image=image_canvas_image)

            # Taille des cases de la grille dans l'image originale
            taille_case = image_taille / taille  # 100x100 cases dans l'image

            def obtenir_case_grille(event):
                # Coordonnées du clic sur le canvas
                x = event.x
                y = event.y

                print(f"on a x : {x} on a taille case = {taille_case} donc on est colonne : {x // taille_case}")

                # Calcul des indices de la case (ligne, colonne) dans l'image originale
                case_y = int(x // taille_case)  # Indice de la colonne
                case_x = int(y // taille_case)  # Indice de la ligne

                print(f"Case cliquée - colonne: {case_x}, ligne: {case_y}")
                print(f"X : {x},y : {y}")
                couleur = couleur_var.get()
                print(f"Coordonnées: x={case_x}, y={case_y}, couleur={couleur}")
                message = f"Coordonnées: x={str(case_x)}, y={str(case_y)}, couleur={couleur}"
                igs.service_call("Whiteboard", "chat", message, "")
                position = int(case_x)*taille + int(case_y)
                print(f"Position: {position}")
                arguments = (str(position), couleur)
                igs.service_call("Tableau", "ajouter", arguments,"")
                
                

            # Associer l'événement clic au Canvas
            image_canvas.bind("<Button-1>", obtenir_case_grille)
            previsu = None
            
            # Fonction déclenchée lorsque la souris passe au-dessus du canvas
            def survol_canvas(event):
                global previsu
                try : 
                    image_canvas.delete(previsu)
                except:
                    pass
                x = event.x
                y = event.y
                case_y = int(x // taille_case)
                case_x = int(y // taille_case)
                print(f"Survol - Coordonnées: x={x}, y={y}, case x : {case_x}, case y : {case_y}")
                couleur = couleur_var.get()
                previsu_tmp = image_canvas.create_rectangle(case_y*taille_case+2, case_x*taille_case+2, case_y*taille_case+taille_case+2, case_x*taille_case+taille_case+2, fill=couleur, outline="")
                previsu = previsu_tmp
                
            
            image_canvas.bind("<Motion>", survol_canvas)
            
            # Liste de couleurs à afficher sur le Canvas
            couleurs = ["black", "grey", "#C0C0C0", "white", "red", "#800000", "yellow", "#808000", 
                        "green", "#008000", "#00FFFF", "#008080", "blue", "#000080", "pink", "violet"]
            # Petit Canvas pour la sélection de la couleur
            taille_carré = 40
            couleur_canvas = tk.Canvas(window, bg="white", width=ajuster_taille(len(couleurs)*taille_carré, proportion_x), height=ajuster_taille(taille_carré, proportion_y))
            couleur_canvas.place(x=ajuster_taille(1, proportion_x), y=ajuster_taille(800, proportion_y))
            
            # Création des carrés de couleur dans le petit Canvas
            carré_taille = ajuster_taille(taille_carré, proportion_x)
            for i, couleur in enumerate(couleurs):
                x1 = i * carré_taille
                x2 = x1 + carré_taille
                y1 = 0
                y2 = ajuster_taille(taille_carré, proportion_y)
                couleur_canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="")

            # Ajout d'un événement pour capturer le clic sur le nuancier
            couleur_canvas.bind("<Button-1>", choisir_couleur)

            # Variable pour stocker la couleur sélectionnée
            couleur_var = tk.StringVar(value="noir")

            # Coordonnées X et Y
            x_label = tk.Label(window, text="x :", font=("Arial", ajuster_taille(16, proportion_y)))
            x_label.place(x=ajuster_taille(650, proportion_x), y=ajuster_taille(810, proportion_y))

            x_entry = tk.Entry(window, width=ajuster_taille(10, proportion_x), font=("Arial", ajuster_taille(16, proportion_y)))
            x_entry.place(x=ajuster_taille(680, proportion_x), y=ajuster_taille(810, proportion_y))

            y_label = tk.Label(window, text="y :", font=("Arial", ajuster_taille(16, proportion_y)))
            y_label.place(x=ajuster_taille(800, proportion_x), y=ajuster_taille(810, proportion_y))

            y_entry = tk.Entry(window, width=ajuster_taille(10, proportion_x), font=("Arial", ajuster_taille(16, proportion_y)))
            y_entry.place(x=ajuster_taille(830, proportion_x), y=ajuster_taille(810, proportion_y))

            couleur_label = tk.Label(window, text="Couleur :", font=("Arial", ajuster_taille(16, proportion_y)))
            couleur_label.place(x=ajuster_taille(1050, proportion_x), y=ajuster_taille(810, proportion_y))
            
            couleur_label2 = tk.Label(window, textvariable=couleur_var, font=("Arial", ajuster_taille(16, proportion_y)))
            couleur_label2.place(x=ajuster_taille(1140, proportion_x), y=ajuster_taille(810, proportion_y))
            # Bouton Valider
            valider_button = tk.Button(window, text="VALIDER", width=ajuster_taille(18, proportion_x), font=("Arial", ajuster_taille(16, proportion_y)), command=valider)
            valider_button.place(x=ajuster_taille(1290, proportion_x), y=ajuster_taille(810, proportion_y))

            # Lancement de la boucle principale
            window.mainloop()

    if igs.is_started():
        igs.stop()
