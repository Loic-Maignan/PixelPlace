import subprocess
import sys

if __name__ == "__main__":
    agents = ["ShowMatrice","Tableau"]
    for agent in agents:
        commande = "cd ./Agents/" + agent + "/ ; python ./main.py Ethernet 5670"
        subprocess.run(['powershell', '-Command', f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"'])
    commande = "cd ./Whiteboard/Whiteboard ; ./Whiteboard.exe"
    subprocess.run(['powershell', '-Command', f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"'])



