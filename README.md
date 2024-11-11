# PixelPlace

Sous powershell:
autoriser env: Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
utiliser pip : python -m pip ...

python -m venv EnvPixelPlace
source EnvPixelPlace/Scripts/activate
pip install -r requirment.txt

cd PixelPlace
python launch.py Agent1 Agent2

exemple : python launch.py GetKey None

launch lance powershell donc ne marche pas sous linux

TODO

Client Joueur : - (FAIT) garder la position de l'image / - (FAIT) appel du service welbye au demmarage et a l'arret de l'agent (ajout du bouton fermer)

Tchat : - cration d'un agent tchat / - recupération de tout les tchat envoyé au whiteboard / -

Le curseur blanc en dark mode
ecrire une explication de l'application a droite du canva puis essayer d'inserer un autre canva ou l'utilisateur pour mettre une image afin de pouvoir la recopier