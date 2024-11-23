#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from PIL import Image
import os
import pygetwindow as gw
from io import BytesIO
import random

Colors = [
    "#6d0019",
    "#bb0038",
    "#ff4500",
    "#ffaa00",
    "#fcd730",
    "#fff8b6",
    "#00a46a",
    "#02cc7b",
    "#7bef52",
    "#01766d",
    "#009faa",
    "#02cbbf",
    "#2650a6",
    "#3591ec",
    "#50e9f6",
    "#4639c1",
    "#6c5dff",
    "#96b2fa",
    "#801da2",
    "#b749c0",
    "#e6aafc",
    "#dd107d",
    "#fe3881",
    "#ff98ab",
    "#6d482e",
    "#9a6927",
    "#ffb270",
    "#525252",
    "#898e91",
    "#d4d7d8",
]

MatriceOld = None
SizeMatrice = None
SizePixel = None
NbImg = 0
WindowW = 0
WindowH = 0
FileName = ""
AgentName = "ShowMatrice"
device = None
ListPlayers = []
ListColors = []


def hex_to_rgb(hex_value):
    # Supprimer le symbole '#' si présent
    hex_value = hex_value.lstrip("#")

    # Extraire les composants rouges, verts et bleus
    r = int(hex_value[0:2], 16)  # Composant rouge
    g = int(hex_value[2:4], 16)  # Composant vert
    b = int(hex_value[4:6], 16)  # Composant bleu

    return (r, g, b)


def tchat(
    sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data
):
    arg = (arguments[0], arguments[1], ListColors[ListPlayers.index(sender_agent_uuid)])
    for player in ListPlayers:
        print(arg)
        igs.service_call(player, "Chat", arg, "")


def send_IMG(player):
    img = Image.open(FileName)
    buffer = BytesIO()  # Crée un buffer en mémoire
    img.save(buffer, format="PNG")  # Sauvegarde l'image dans le buffer au format PNG
    # Récupérer les octets de l'image
    img_bytes = buffer.getvalue()
    # Exemple : Utiliser les octets pour un traitement supplémentaire
    igs.service_call(
        player, "Mise_a_jour_matrice", (img_bytes, SizeMatrice, SizePixel), ""
    )
    # Optionnel : Fermer le buffer
    buffer.close()


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    if event == igs.AGENT_KNOWS_US:
        if uuid[-4:] == name:
            ListPlayers.append(uuid)
            ListColors.append(Colors[random.randint(0, len(Colors) - 1)])
            send_IMG(uuid)
        if "Whiteboard" == name:
            igs.output_set_impulsion("Init_Whiteboard")
            igs.output_set_impulsion("Start_Timer")
        if "Tableau" == name:
            igs.output_set_int("Init_Tableau", 100)
    if event == igs.AGENT_EXITED:
        if "Whiteboard" == name:
            igs.output_set_impulsion("Start_Timer")

    elif event == igs.AGENT_EXITED:
        if uuid in ListPlayers:
            ListPlayers.remove(uuid)


def clear_callback(iop_type, name, value_type, value, my_data):
    global NbImg
    igs.service_call("Whiteboard", "clear", (), "")
    igs.output_set_impulsion("Init_Whiteboard")
    igs.output_set_int("Init_Tableau", 100)

    for fichier in os.listdir("Img/"):
        chemin_fichier = os.path.join("Img/", fichier)
        if os.path.isfile(chemin_fichier):
            try:
                os.remove(chemin_fichier)
            except:
                pass
    MatriceOld = None
    NbImg = 0


def get_specific_window_size(window_title):
    windows = gw.getWindowsWithTitle(window_title)

    if not windows:
        return None

    window = windows[0]

    width, height = window.width, window.height

    if width < 1300:
        width = int(width / 2.5)
    else:
        width = int(width / 2)
    if height < 1200:
        height = int(height / 1.5)
    else:
        height = int(height / 1.2)

    return (width, height)


def checkSize_callback(iop_type, name, value_type, value, my_data):
    global WindowH, WindowW
    w, h = get_specific_window_size("Whiteboard")
    if WindowW != w or WindowH != h:
        WindowH = h
        WindowW = w
        create_IMG()


def matrice_callback(iop_type, name, value_type, value, my_data):
    global SizeMatrice, MatriceOld
    value = str(value).split(";")
    SizeMatrice = int(value[0])
    value = value[1].split(",")
    ligne = []
    matrice = []
    i = 0
    for val in value:
        i += 1
        ligne.append(val)
        if i == SizeMatrice:
            matrice.append(ligne)
            i = 0
            ligne = []
    MatriceOld = matrice
    create_IMG()


def show_Img(fileName):
    arguments_list = ("file:///" + os.path.abspath(fileName), WindowW / 3, 0.0)
    igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")


def create_IMG():
    global NbImg, FileName, SizePixel

    if MatriceOld == None:
        show_Img(FileName)
    else:
        SizePixel = int(WindowH / SizeMatrice)
        border_size = 1
        image_ligne = len(MatriceOld[0]) * (SizePixel) + border_size * 2
        image_colone = len(MatriceOld) * (SizePixel) + border_size * 2

        img = Image.new("RGB", (image_ligne, image_colone), (0, 0, 0))

        for row_idx, row in enumerate(MatriceOld):
            for col_idx, color in enumerate(row):
                rgb_color = hex_to_rgb(color)
                start_x = col_idx * (SizePixel) + border_size
                start_y = row_idx * (SizePixel) + border_size
                for i in range(SizePixel):
                    for j in range(SizePixel):
                        img.putpixel((start_x + i, start_y + j), rgb_color)
        FileName = "Img/matrice" + str(NbImg) + ".png"
        img.save(FileName)
        for player in ListPlayers:
            send_IMG(player)

        arguments_list = NbImg - 1
        igs.service_call("Whiteboard", "remove", arguments_list, "")
        NbImg += 1

        show_Img(FileName)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py AgentName network_device port")
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
            igs.info(
                "using %s as default network device (this is the only one available)"
                % str(device)
            )
        elif len(list_devices) == 2 and (
            list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"
        ):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print(
                "using %s as de fault network device (this is the only one available that is not the loopback)"
                % str(device)
            )
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error(
                    "No network device passed as command line parameter and several are available."
                )
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
            exit(1)

    for fichier in os.listdir("Img/"):
        chemin_fichier = os.path.join("Img/", fichier)
        if os.path.isfile(chemin_fichier):
            try:
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

    igs.output_create("Init_Tableau", igs.INTEGER_T, None)
    igs.output_create("Init_Whiteboard", igs.IMPULSION_T, None)
    igs.output_create("Start_Timer", igs.IMPULSION_T, None)

    igs.service_init("Chat", tchat, None)
    igs.service_arg_add("Chat", "nom", igs.STRING_T)
    igs.service_arg_add("Chat", "message", igs.STRING_T)
    igs.observe_input("CheckSize", checkSize_callback, None)
    igs.observe_input("Matrice", matrice_callback, None)
    igs.observe_input("Clear", clear_callback, None)
    igs.observe_agent_events(on_agent_event_callback, None)

    igs.start_with_device(device, int(sys.argv[2]))

    input("")
    igs.stop()
