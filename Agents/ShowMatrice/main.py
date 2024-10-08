#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from PIL import Image
import os


color_mapping = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
}

MatriceOld = None
cpt  = 0
FileName = ""

def clear_callback(iop_type, name, value_type, value, my_data):
    global FileName
    if FileName == "":
        FileName = "init.png"
    arguments_list = ()
    arguments_list = ("file:///" + os.path.abspath(FileName),100.0,0.0)
    igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")

def matrice_callback(iop_type, name, value_type, value, my_data):
    value = str(value).split(";")
    taille = int(value[0])
    value = value[1].split(",")
    ligne = []
    matrice = []
    i = 0
    for val in value:
        i += 1
        ligne.append(val)
        if i == taille:
            matrice.append(ligne)
            i = 0
            ligne = []
    createIMG(matrice,taille)
    #show_matrice(matrice,taille)

def createIMG(matrice,tailleMatrice):
    global cpt,FileName
    taillePixelX = int(500/tailleMatrice)
    taillePixelY = int(300/tailleMatrice)
    border_size = 1
    image_ligne = len(matrice[0]) * (taillePixelX + border_size) + border_size
    image_colone = len(matrice) * (taillePixelY + border_size) + border_size

    img = Image.new('RGB', (image_ligne, image_colone), (0, 0, 0)) 

    for row_idx, row in enumerate(matrice):
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
    arguments_list = ("file:///" + os.path.abspath(FileName),100.0,0.0)
    igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")


def show_matrice(matrice,tailleMatrice):
    global MatriceOld
    if MatriceOld == None:
        taillePixelX = 500/tailleMatrice
        taillePixelY = 300/tailleMatrice
        for i,ligne in enumerate(matrice):
            posy = 100 +taillePixelY*i
            for j,colone in enumerate(ligne):
                posx = 100 + taillePixelX*j
                arguments_list = ("rectangle",posx,posy,taillePixelX,taillePixelY,colone,"black",max(float(taillePixelX/100),0.5))
                igs.service_call("Whiteboard", "addShape", arguments_list, "")
    elif MatriceOld != matrice:
            for i,ligne in enumerate(matrice):
                for j,colone in enumerate(ligne):
                    if MatriceOld[i][j] != colone:
                        arguments_list = (i*tailleMatrice+j,"fill",colone)
                        igs.service_call("Whiteboard", "setStringProperty", arguments_list, "")
    MatriceOld = matrice

        
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
    igs.observe_input("Matrice", matrice_callback, None)
    igs.observe_input("Clear", clear_callback, None)

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))

    
    input("")
    igs.stop()