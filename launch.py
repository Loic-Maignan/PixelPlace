import subprocess
import sys

if __name__ == "__main__":
    agents = []
    for i in range(0,len(sys.argv)):
        if i != 0:
            agents.append(sys.argv[i])
    for agent in agents:
        commande = "cd ./Agents/" + agent + "/ ; python ./main.py Wi-Fi 5670"
        subprocess.run(['powershell', '-Command', f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"'])



