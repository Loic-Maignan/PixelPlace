#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from PIL import Image
import os
import pygetwindow as gw
from io import BytesIO
import random

color_mapping = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
}

couleurs = ["#6d0019","#bb0038","#ff4500","#ffaa00","#fcd730","#fff8b6","#00a46a","#02cc7b",
                        "#7bef52","#01766d","#009faa","#02cbbf","#2650a6","#3591ec","#50e9f6","#4639c1",
                        "#6c5dff","#96b2fa","#801da2","#b749c0","#e6aafc","#dd107d","#fe3881","#ff98ab",
                        "#6d482e","#9a6927","#ffb270","#000000","#525252","#898e91","#d4d7d8","#ffffff"]

MatriceOld = None
Taille = None
cpt  = 0
WindowW = 0
WindowH = 0
FileName = ""
agent_name = "ShowMatrice"
device = None
ListJoueurs = []
ListCouleur = []

def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")

def hex_to_rgb(hex_value):
    # Supprimer le symbole '#' si présent
    hex_value = hex_value.lstrip('#')
    
    # Extraire les composants rouges, verts et bleus
    r = int(hex_value[0:2], 16)  # Composant rouge
    g = int(hex_value[2:4], 16)  # Composant vert
    b = int(hex_value[4:6], 16)  # Composant bleu
    
    return (r, g, b)
def Chat(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    arg = (arguments[0],arguments[1],ListCouleur[ListJoueurs.index(sender_agent_uuid)])
    for joueur in ListJoueurs:
        print(arg)
        igs.service_call(joueur, "Chat", arg, "")
    

def on_agent_event_callback(event, uuid, name, event_data, my_data):
    if event == igs.AGENT_ENTERED:
        if uuid[-4:] == name:
            ListJoueurs.append(uuid)
            ListCouleur.append(couleurs[random.randint(0,len(couleurs)-1)])
    elif event == igs.AGENT_EXITED:
        if uuid in ListJoueurs:
            ListJoueurs.remove(uuid)
     
def clear_callback(iop_type, name, value_type, value, my_data):
    global cpt
    igs.service_call("Whiteboard", "clear", (), "")

    for fichier in os.listdir("Img/"):
        chemin_fichier = os.path.join("Img/", fichier)
        if os.path.isfile(chemin_fichier):
            try : 
                os.remove(chemin_fichier)
            except:
                pass
    MatriceOld = None
    cpt = 0

def get_specific_window_size(window_title):
    windows = gw.getWindowsWithTitle(window_title)
    
    if not windows:
        return None
    
    window = windows[0]
    
    width, height = window.width, window.height

    if width < 1300:
        width = int(width/2.5)
    else:
        width = int(width/2)
    if height < 1200 :
        height = int(height/1.5)
    else:
        height = int(height/1.2)
    
    return (width, height)
def checkSize_callback(iop_type, name, value_type, value, my_data):
    global WindowH, WindowW
    w, h = get_specific_window_size("Whiteboard")
    if WindowW != w or WindowH != h:
        WindowH = h
        WindowW = w
        create_IMG()


def matrice_callback(iop_type, name, value_type, value, my_data):
    global Taille,MatriceOld
    value = str(value).split(";")
    Taille = int(value[0])
    value = value[1].split(",")
    ligne = []
    matrice = []
    i = 0
    for val in value:
        i += 1
        ligne.append(val)
        if i == Taille:
            matrice.append(ligne)
            i = 0
            ligne = []
    MatriceOld = matrice
    create_IMG()

def show_Img(fileName):
    arguments_list = ("file:///" + os.path.abspath(fileName),WindowW/3,0.0)
    igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")

def create_IMG():
    global cpt, FileName

    if MatriceOld == None:
        show_Img(FileName)
    else:
        taillePixel = int(WindowH/Taille)
        border_size = 1
        image_ligne = len(MatriceOld[0]) * (taillePixel) + border_size*2
        image_colone = len(MatriceOld) * (taillePixel) + border_size*2

        img = Image.new('RGB', (image_ligne, image_colone), (0, 0, 0)) 

        for row_idx, row in enumerate(MatriceOld):
            for col_idx, color in enumerate(row):
                try :
                    rgb_color = hex_to_rgb(color)
                except:
                    rgb_color = color_mapping[color]
                start_x = col_idx * (taillePixel) + border_size
                start_y = row_idx * (taillePixel) + border_size
                for i in range(taillePixel):
                    for j in range(taillePixel):
                        img.putpixel((start_x + i, start_y + j), rgb_color)
        FileName = "Img/matrice" + str(cpt) + ".png"
        img.save(FileName)
        # Convertir l'image en chaîne d'octets
        buffer = BytesIO()  # Crée un buffer en mémoire
        img.save(buffer, format='PNG')  # Sauvegarde l'image dans le buffer au format PNG

        # Récupérer les octets de l'image
        image_bytes = buffer.getvalue()

        # Exemple : Utiliser les octets pour un traitement supplémentaire
        for joueur in ListJoueurs:
            igs.service_call(joueur, "Mise_a_jour_matrice", image_bytes,"")

        # Optionnel : Fermer le buffer
        buffer.close()
        
        arguments_list = (cpt-1)
        igs.service_call("Whiteboard", "remove", arguments_list, "")
        cpt += 1

        show_Img(FileName)

        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)
    
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
        
        

    for fichier in os.listdir("Img/"):
        chemin_fichier = os.path.join("Img/", fichier)
        if os.path.isfile(chemin_fichier):
            try : 
                os.remove(chemin_fichier)
            except:
                pass

    igs.agent_set_name("ShowMatrice")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("Matrice", igs.STRING_T, None)
    igs.input_create("Clear", igs.IMPULSION_T, None)
    igs.input_create("CheckSize", igs.IMPULSION_T, None)
    igs.input_create("Clear", igs.IMPULSION_T, None)
    igs.service_init("Chat", Chat, None)
    igs.service_arg_add("Chat", "nom", igs.STRING_T)
    igs.service_arg_add("Chat", "message", igs.STRING_T)
    igs.observe_input("CheckSize", checkSize_callback, None)
    igs.observe_input("Matrice", matrice_callback, None)
    igs.observe_input("Clear", clear_callback, None)
    igs.observe_agent_events(on_agent_event_callback, None)

    
    igs.start_with_device(device, int(sys.argv[2]))
    
    input("")
    igs.stop()