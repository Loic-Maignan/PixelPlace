#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  GetKey version 1.0

import sys
import ingescape as igs
import keyboard

def key_event(e):
    print(f"Touche appuyée: {e.name}")
    igs.output_set_string("Key", e.name)
    if e.name == 'esc':
        print("Quitter le programme")
        keyboard.unhook_all()
        

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name("GetKey")
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))


    igs.output_create("Key", igs.STRING_T, None)

    igs.start_with_device(sys.argv[1], int(sys.argv[2]))

    keyboard.hook(key_event)
    keyboard.wait('esc')
    igs.stop()
        

