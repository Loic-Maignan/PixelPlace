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

ShowMatrice : - virer le clear / - creer une liste des noms de clientjoueurs / - ajout du service pour changer le nom des clientjoueur / - creer un seul service welbye si l'uuid est present dans la liste il le supprime sinon il l'ajoute si une client vient d'arriver lui envoyer l'image / - generer une image avec ligne blanche

Tchat : - cration d'un agent tchat / - recupération de tout les tchat envoyé au whiteboard / - 