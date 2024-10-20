#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Name version 1.0

import sys
import ingescape as igs

TAILLE = 100
tableau = ["white" for i in range(TAILLE*TAILLE)] 

def input_callback(iop_type, name, value_type, value, my_data):
    igs.info(f"Input {name} of type {value_type} has been written with value '{value}' and user data '{my_data}'")
    position,couleur = value.split(',')
    tableau[int(position)] = couleur
    message = str(TAILLE) + ";"
    for i in tableau:
        message += str(i) + ","
        
    igs.output_set_string("Matrice", message)
    

def ajouter(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    print(arguments)
    print(f"Service {service_name} was called by {sender_agent_name} ({sender_agent_uuid}) with arguments : {''.join(f'arg={argument} ' for argument in arguments)}",my_data,token)
    igs.info(f"Service {service_name} was called by {sender_agent_name} ({sender_agent_uuid}) with arguments : {''.join(f'arg={argument} ' for argument in arguments)}")
    position = arguments[0]
    couleur = arguments[1]
    tableau[int(position)] = couleur
    message = str(TAILLE) + ";"
    for i in tableau:
        message += str(i) + ","
    igs.output_set_string("Matrice", message)
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name("Tableau")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))
    
    igs.service_init("ajouter", ajouter, None)
    igs.service_arg_add("ajouter", "position", igs.STRING_T)
    igs.service_arg_add("ajouter", "couleur", igs.STRING_T)

    
    igs.input_create("Position/Couleur", igs.STRING_T, None)
    igs.observe_input("Position/Couleur", input_callback, None)
    
    igs.output_create("Matrice", igs.STRING_T, None)

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))
    input('')

    igs.stop()