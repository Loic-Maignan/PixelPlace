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
import io

from new import *

taille = 100
posx_canvas = 0
posy_canvas = 0

port = 5670
agent_name = "ClientJoueur"
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
      
def Mise_a_jour_matrice(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    print(arguments)
    print(f"Service {service_name} was called by {sender_agent_name} ({sender_agent_uuid}) with arguments : {''.join(f'arg={argument} ' for argument in arguments)}",my_data,token)
    igs.info(f"Service {service_name} was called by {sender_agent_name} ({sender_agent_uuid}) with arguments : {''.join(f'arg={argument} ' for argument in arguments)}")
    image = arguments[0]
    nouvelle_photo(image)

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
    
    igs.service_init("Mise_a_jour_matrice", Mise_a_jour_matrice, agent)
    igs.service_arg_add("Mise_a_jour_matrice", "matrice", igs.DATA_T)

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

            def nouvelle_photo(image):
                global image_redimensionnee, image_canvas_image, scale_factor, taille_case, image_id, image_recu
                image_stream = io.BytesIO(image)
                image_recu = Image.open(image_stream)  # Image de la grille
                # Taille de l'image après zoom
                new_width = int(image_taille * scale_factor)
                new_height = int(image_taille * scale_factor)

                # Redimensionner l'image
                image_redimensionnee = image_recu.resize((new_width, new_height), Image.LANCZOS)
                image_canvas_image = ImageTk.PhotoImage(image_redimensionnee)

                # Supprimer l'image actuelle du canvas et la remplacer par l'image zoomée
                image_canvas.delete(image_id)
                image_id_tmp = image_canvas.create_image(2, 2, anchor="nw", image=image_canvas_image)

                # Ajuster la taille des cases
                taille_case = new_width / 100

                # Redéfinir la région de scroll
                image_canvas.config(scrollregion=image_canvas.bbox("all"))
                image_id = image_id_tmp
                
            # Fonction pour gérer la sélection de la couleur
            def choisir_couleur(event):
                x = event.x
                y = event.y
                couleur_selectionnee = couleur_canvas.itemcget(couleur_canvas.find_closest(x, y), "fill")
                print(f"Couleur choisie: {couleur_selectionnee}")
                couleur_var.set(couleur_selectionnee)
            
            def changer_name(event):
                user = user_var.get()
                igs.agent_set_name(user)
                igs.service_call("Whiteboard", "chat", f"Changement de nom: {user}", "")
                user_var.set(user)
                image_canvas.focus_set()

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
            titre_text = "PixelPlace"
            titre_label = tk.Label(window, text=titre_text, font=("Comic Sans MS", ajuster_taille(20, proportion_x)))

            # Calcul pour centrer le titre horizontalement
            titre_width = ajuster_taille(12 * len(titre_text), proportion_x)  # Largeur estimée du texte
            titre_label.place(x=(wx - titre_width) / 2, y=ajuster_taille(1, proportion_y))
            
            user_text = "Utilisateur: "
            user_label = tk.Label(window, text=user_text, font=("Arial", ajuster_taille(16, proportion_y)))
            user_label.place(x=ajuster_taille(1, proportion_x), y=ajuster_taille(10, proportion_y))
            
            user_var = tk.StringVar(value=str(igs.agent_uuid()[-4:]))
            user_entry = tk.Entry(window, width=ajuster_taille(10, proportion_x), font=("Arial", ajuster_taille(16, proportion_y)), textvariable=user_var)
            user_entry.place(x=ajuster_taille(110, proportion_x), y=ajuster_taille(10, proportion_y))
            
            user_entry.bind("<Return>", changer_name)
            
            timer_text = "Timer: "
            timer_label = tk.Label(window, text=timer_text, font=("Arial", ajuster_taille(16, proportion_y)))
            timer_label.place(x=ajuster_taille(1200, proportion_x), y=ajuster_taille(1, proportion_y))
            
            timer_var = tk.StringVar(value="00:00")
            timer_label2 = tk.Label(window, font=("Arial", ajuster_taille(16, proportion_y)), textvariable=timer_var)
            timer_label2.place(x=ajuster_taille(1270, proportion_x), y=ajuster_taille(1, proportion_y))

            # Grand Canvas pour l'image ou le dessin
            image_canvas = tk.Canvas(window, bg="white", width=ajuster_taille(730, proportion_x), height=ajuster_taille(730, proportion_y))
            image_canvas.place(x=ajuster_taille((wx-ajuster_taille(730, proportion_x))/2, proportion_x), y=ajuster_taille(50, proportion_y))

            # Charger l'image PNG
            image_recu = None
            nom_image = "init.png"
            image_originale = Image.open(nom_image)  # Image de la grille
            image_originale_width, image_originale_height = image_originale.size


            # Redimensionner l'image pour l'adapter au Canvas
            image_taille = 730 
            image_redimensionnee = image_originale.resize((ajuster_taille(image_taille,proportion_x), ajuster_taille(image_taille,proportion_y)), Image.LANCZOS)  # Ajusté à la taille de la fenêtre
            image_canvas_image = ImageTk.PhotoImage(image_redimensionnee)
            image_id = image_canvas.create_image(2, 2, anchor="nw", image=image_canvas_image)

            # Taille des cases de la grille dans l'image originale
            taille_case = image_taille / taille  # 100x100 cases dans l'image
            scale_factor = 1.0  # Facteur de zoom initial
            
            
            
            # Variables pour le déplacement
            drag_data = {"x": 0, "y": 0, "item": None}
            timer = 0
            
            def appel_image():
                image = igs.service_call("Tableau", "demande_image", "", "")
                print(image)
                window.after(1000, appel_image)
                
            window.after(1000, appel_image)
            def updateClock():
                global timer
                timer-=1
                timer_var.set(f"00:{timer}")
                if timer > 0:
                    window.after(1000, updateClock)
                

            def obtenir_case_grille(event):
                # Coordonnées du clic sur le canvas
                x = event.x
                y = event.y

                print(f"on a x : {x} on a taille case = {taille_case} donc on est colonne : {x // taille_case}")
                
                position = image_canvas.coords(image_id)  # Renvoie une liste [x, y]
                x, y = -(position[0])+x, -(position[1])+y

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
                
            def zoom(event):
                """Zoomer à l'endroit de la souris en utilisant la molette."""
                global image_redimensionnee, image_canvas_image, scale_factor, taille_case, image_id
                
                # Facteur de zoom : zoom in (1.1) ou zoom out (0.9)
                scale = 1.1 if event.delta > 0 else 0.9
                scale_factor *= scale
                if scale_factor < 1:
                    scale_factor = 1
                if scale_factor > 2:
                    scale_factor = 2
                zoom_var.set(f'{scale_factor:.1f}')
                # Obtenir la position actuelle de la souris
                x = image_canvas.canvasx(event.x)
                y = image_canvas.canvasy(event.y)

                # Taille de l'image après zoom
                new_width = int(image_taille * scale_factor)
                new_height = int(image_taille * scale_factor)

                # Redimensionner l'image
                image_redimensionnee = image_recu.resize((new_width, new_height), Image.LANCZOS)
                image_canvas_image = ImageTk.PhotoImage(image_redimensionnee)

                # Supprimer l'image actuelle du canvas et la remplacer par l'image zoomée
                image_canvas.delete(image_id)
                image_id_tmp = image_canvas.create_image(2, 2, anchor="nw", image=image_canvas_image)

                # Ajuster la taille des cases
                taille_case = new_width / 100

                # Redéfinir la région de scroll
                image_canvas.config(scrollregion=image_canvas.bbox("all"))
                image_id = image_id_tmp

            mouvement = False
            # Déplacement de l'image avec la souris
            def commencer_drag(event):
                """Début du drag"""
                drag_data["item"] = image_id
                drag_data["x"] = event.x
                drag_data["y"] = event.y

            def drag_image(event):
                """Déplacer l'image lors du drag"""
                global mouvement
                dx = event.x - drag_data["x"]
                dy = event.y - drag_data["y"]
                if dx != 0 and dy != 0:
                    mouvement = True

                position = image_canvas.coords(image_id)  # Renvoie une liste [x, y]
                x, y = position[0], position[1]

                if x <= 732 - taille_case*taille  and dx < 0 :
                    dx =0
                if y <= 732 - taille_case*taille and dy < 0 :
                    dy = 0
                if y >= 2 and dy > 0 :
                    dy = 0
                if x >= 2 and dx > 0 :
                    dx = 0
                # Déplacer l'image dans le canvas
                image_canvas.move(drag_data["item"], dx, dy)
                
                # Mettre à jour les coordonnées de la souris pour le prochain mouvement
                drag_data["x"] = event.x
                drag_data["y"] = event.y

            def finir_drag(event):
                """Fin du drag"""
                global mouvement, timer
                if mouvement == False:
                    if timer == 0 :
                        timer = 11
                        window.after(1000, updateClock)
                        obtenir_case_grille(event)

                drag_data["item"] = None
                drag_data["x"] = 0
                drag_data["y"] = 0
                mouvement = False
            
            # Associer l'événement clic au Canvas            
            image_canvas.bind("<ButtonPress-1>", commencer_drag)
            image_canvas.bind("<B1-Motion>", drag_image)
            image_canvas.bind("<ButtonRelease-1>", finir_drag)

            image_canvas.bind("<Control-MouseWheel>", zoom)
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
                position = image_canvas.coords(image_id)  # Renvoie une liste [x, y]
                x, y = -(position[0])+x, -(position[1])+y
                y_var.set(str(int(y // taille_case)))
                x_var.set(str(int(x // taille_case)))
                if int(y // taille_case) < 0 :
                    y_var.set("0")
                if int(x // taille_case) < 0 :
                    x_var.set("0")
                if int(y // taille_case) > 99 :
                    y_var.set("99")
                if int(x // taille_case) > 99 :
                    x_var.set("99")
                    
                
                print(f"Survol - Coordonnées: x={x}, y={y}, case x : {case_x}, case y : {case_y}")
                couleur = couleur_var.get()
                previsu_tmp = image_canvas.create_rectangle(case_y*taille_case+2, case_x*taille_case+2, case_y*taille_case+taille_case+2, case_x*taille_case+taille_case+2, fill=couleur, outline="")
                previsu = previsu_tmp
                
            
            image_canvas.bind("<Motion>", survol_canvas)
            
            # Liste de couleurs à afficher sur le Canvas
            couleurs = ["#FFFFFF", "#C0C0C0", "#808080", "#000000", "#FF99CC", "#FF0000", "#FF6600", "#CC6600", 
                        "#FFFF00", "#00FF00", "#33CC33", "#00FFFF", "#3333FF", "#0000FF", "#FF00FF", "#800080"]
            
            # Petit Canvas pour la sélection de la couleur
            taille_carré = 40
            couleur_canvas = tk.Canvas(window, bg="white", width=ajuster_taille(len(couleurs)*taille_carré, proportion_x), height=ajuster_taille(taille_carré, proportion_y))
            couleur_canvas.place(x=ajuster_taille((wx-ajuster_taille(len(couleurs)*taille_carré, proportion_x)) / 2, proportion_x), y=ajuster_taille(800, proportion_y))
            
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
            couleur_var = tk.StringVar(value="#000000")

            # Coordonnées X et Y
            x_label = tk.Label(window, text="x :", font=("Arial", ajuster_taille(16, proportion_y)))
            x_label.place(x=ajuster_taille(300, proportion_x), y=ajuster_taille(10, proportion_y))

            x_var = tk.StringVar(value="0")
            x_label_var = tk.Label(window,textvariable=x_var, font=("Arial", ajuster_taille(16, proportion_y)))
            x_label_var.place(x=ajuster_taille(330, proportion_x), y=ajuster_taille(10, proportion_y))

            y_label = tk.Label(window, text="y :", font=("Arial", ajuster_taille(16, proportion_y)))
            y_label.place(x=ajuster_taille(390, proportion_x), y=ajuster_taille(10, proportion_y))

            y_var = tk.StringVar(value="0")
            y_label_var = tk.Label(window,textvariable=y_var , font=("Arial", ajuster_taille(16, proportion_y)))
            y_label_var.place(x=ajuster_taille(420, proportion_x), y=ajuster_taille(10, proportion_y))

            zoom_label = tk.Label(window, text="zoom :", font=("Arial", ajuster_taille(16, proportion_y)))
            zoom_label.place(x=ajuster_taille(480, proportion_x), y=ajuster_taille(10, proportion_y))

            zoom_var = tk.StringVar(value="1.0")
            zoom_label_var = tk.Label(window,textvariable=zoom_var , font=("Arial", ajuster_taille(16, proportion_y)))
            zoom_label_var.place(x=ajuster_taille(580, proportion_x), y=ajuster_taille(10, proportion_y))

            # Lancement de la boucle principale
            window.mainloop()

    if igs.is_started():
        igs.stop()
