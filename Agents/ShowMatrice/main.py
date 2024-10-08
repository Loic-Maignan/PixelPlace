#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs

MatriceOld = None

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
    show_matrice(matrice,taille)

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

    igs.agent_set_name("ShowMatrice")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("Matrice", igs.STRING_T, None)
    igs.observe_input("Matrice", matrice_callback, None)

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))

    
    input("")
    igs.stop()