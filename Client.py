import subprocess

if __name__ == "__main__":
    agents = ["ClientJoueur"]
    for agent in agents:
        commande = "cd ./Agents/" + agent + "/ ; python ./main.py Ethernet 5670"
        subprocess.run(
            [
                "powershell",
                "-Command",
                f'Start-Process powershell -ArgumentList "-NoExit", "{commande}"',
            ]
        )
