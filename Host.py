import subprocess
import sys
import time

if __name__ == "__main__":
    agents = ["ShowMatrice","Tableau"]
    commande = "cd ./Whiteboard/Whiteboard ; ./Whiteboard.exe"
    subprocess.run(['powershell', '-Command', f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"'])
    time.sleep(10)
    for agent in agents:
        commande = "cd ./Agents/" + agent + "/ ; python ./main.py Ethernet 5670"
        subprocess.run(['powershell', '-Command', f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"'])
    



