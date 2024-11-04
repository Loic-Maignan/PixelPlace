#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Name version 1.0

import sys
import ingescape as igs

TAILLE = 100
tableau = ["#FFFFFF" for i in range(TAILLE*TAILLE)] 
agent_name = "Tableau"
device = None

def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")



def size_callback(iop_type, name, value_type, value, my_data):
    global TAILLE, tableau
    TAILLE = value
    tableau = ["#FFFFFF" for i in range(TAILLE*TAILLE)] 
    msg = str(TAILLE) + ";"
    for i in tableau:
        msg += str(i) + ","
    print(msg)
    igs.output_set_string("Matrice", msg)

    

def ajouter(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
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

    igs.agent_set_name("Tableau")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))
    
    igs.service_init("ajouter", ajouter, None)
    igs.service_arg_add("ajouter", "position", igs.STRING_T)
    igs.service_arg_add("ajouter", "couleur", igs.STRING_T)

    
    igs.input_create("Size", igs.INTEGER_T, None)
    igs.observe_input("Size", size_callback, None)
    
    igs.output_create("Matrice", igs.STRING_T, None)

    igs.start_with_device(device, int(sys.argv[2]))
    input('')

    igs.stop()