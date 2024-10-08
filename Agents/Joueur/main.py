#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Name version 1.0

import sys
import ingescape as igs

taille=100

message = ""

COULEURS = {"r": "red", "g": "green", "b": "blue", "w":"white"}

TOUCHES = ["1","2","3","4","5","6","7","8","9","0",",","backspace","enter","r","g","b","w"]

def input_callback(iop_type, name, value_type, value, my_data):
    global message
    if value in TOUCHES:
        if value == "backspace":
            message = message[:-1]
        elif value == "enter":
            ligne,colonne,couleur = message.split(",")
            position = int(ligne)*taille + int(colonne)
            igs.output_set_string("Position/Couleur", str(position) + "," + couleur)
            message = ""
        elif value in COULEURS:
            message += COULEURS[value]
        else:
            message += value
        igs.info(f"Input {name} written")
        igs.output_set_impulsion("clear")
        igs.service_call("Whiteboard", "chat", message, "")
        

        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name("Joueur")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))
    
    igs.input_create("Key", igs.STRING_T, None)
    igs.observe_input("Key", input_callback, None)
    
    igs.output_create("Position/Couleur", igs.STRING_T, None)
    igs.output_create("clear", igs.IMPULSION_T, None)

    input('')
    
    igs.stop()