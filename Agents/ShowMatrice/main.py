#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from PIL import Image
import os
import pygetwindow as gw

color_mapping = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
}

MatriceOld = None
Taille = None
cpt  = 0
WindowW = 0
WindowH = 0
FileName = ""



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


def clear_callback(iop_type, name, value_type, value, my_data):
    show_Img(FileName)

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
    print(matrice)
    create_IMG()

def show_Img(fileName):
    arguments_list = ("file:///" + os.path.abspath(fileName),WindowW/3,0.0)
    igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")

def create_IMG():
    global cpt, FileName

    if MatriceOld == None:
        show_Img(FileName)
    else:
        taillePixelX = int(WindowW/Taille)
        taillePixelY = int(WindowH/Taille)
        border_size = 1
        image_ligne = len(MatriceOld[0]) * (taillePixelX + border_size) + border_size
        image_colone = len(MatriceOld) * (taillePixelY + border_size) + border_size

        img = Image.new('RGB', (image_ligne, image_colone), (0, 0, 0)) 

        for row_idx, row in enumerate(MatriceOld):
            for col_idx, color in enumerate(row):
                rgb_color = color_mapping[color]
                start_x = col_idx * (taillePixelX + border_size) + border_size
                start_y = row_idx * (taillePixelY + border_size) + border_size
                for i in range(taillePixelX):
                    for j in range(taillePixelY):
                        img.putpixel((start_x + i, start_y + j), rgb_color)
        FileName = "Img/matrice" + str(cpt) + ".png"
        img.save(FileName)
        cpt += 1

        arguments_list = ()
        igs.service_call("Whiteboard", "clear", arguments_list, "")
        show_Img(FileName)

        


        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    for fichier in os.listdir("Img/"):
        chemin_fichier = os.path.join("Img/", fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)

    igs.agent_set_name("ShowMatrice")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("Matrice", igs.STRING_T, None)
    igs.input_create("Clear", igs.IMPULSION_T, None)
    igs.input_create("CheckSize", igs.IMPULSION_T, None)
    igs.observe_input("CheckSize", checkSize_callback, None)
    igs.observe_input("Matrice", matrice_callback, None)
    igs.observe_input("Clear", clear_callback, None)

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))

    
    input("")
    igs.stop()