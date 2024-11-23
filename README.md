# PixelPlace

## Pré-requis
Le projet a été testé et utilisé uniquement sur un environnement Windows avec Python 3.12.

---

## Installation

### 1) Créer un environnement Python
1. **Autoriser les environnements dans PowerShell** :  
   ```powershell
   Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
   ```
2. **Installer `venv`** :  
   ```powershell
   pip install virtualenv
   ```
3. **Créer un environnement Python 3.12** :  
   ```powershell
   python -m venv EnvPixelPlace
   ```
4. **Activer l'environnement** :  
   ```powershell
   .\EnvPixelPlace\Scripts\activate
   ```
5. **Naviguer vers le dossier principal** :  
   ```powershell
   cd .\PixelPlace\
   ```
6. **Installer les bibliothèques nécessaires** :  
   ```powershell
   python -m pip install -r requirements.txt
   ```

---

### 2) Lancer PixelPlace
1. **Démarrer le projet ingescape** : 
    - Ouvrez avec l'application **Circle** le projet `PixelPlace.igssystem`
    - Connecter le aux réseaux de votre choix
2. **Démarrer le programme principal** :  
   ```powershell
   python .\Host.py
   ```
3. Le système prendra **10 secondes** pour se lancer. Cela ouvrira **3 terminaux**, y compris celui de `whiteboard`.
4. Connecter le `whiteboard` au même réseaux que celui du projet **Circle**.

---

### 3) Lancer l'interface utilisateur
1. Sur un PC connecté au **même réseau** que le PixelPlace Host, démarrer le programme client :  
   ```powershell
   python .\Client.py
   ```

### Fonctionnalités de PixelPlace

#### 1. Whiteboard (Menu Administrateur)
Le **Whiteboard** est exclusivement destiné aux administrateurs. Il permet :  
- De visualiser les actions des utilisateurs en temps réel.  
- De voir l’image collaborative créée par les utilisateurs dans son intégralité.

---

#### 2. Interface Utilisateur
Les utilisateurs disposent d'une interface intuitive qui offre les fonctionnalités suivantes :  

1. **Mode sombre** :  
   - Un bouton situé en haut à droite permet de passer en mode sombre.

2. **Changement de nom d'utilisateur** :  
   - Un champ en haut à gauche permet de modifier son nom.

3. **Placement de pixels** :  
   - Les utilisateurs peuvent placer un pixel coloré toutes les **10 secondes**.  
   - Un **compte à rebours** est affiché en haut à droite pour indiquer le temps restant avant le prochain placement.

4. **Sélection de couleur** :  
   - Cliquez sur une couleur dans la palette située en bas de l’écran pour changer la couleur du pixel à placer.

5. **Zoom** :  
   - Utilisez la molette de la souris pour zoomer ou dézoomer sur le dessin collaboratif.  
   **Attention** : Le zoom et le dézoom recentrent toujours la caméra en haut à gauche.

6. **Déplacement dans le dessin collaboratif** :  
   - Maintenez le **clic gauche** enfoncé et déplacez la souris pour naviguer dans le dessin.

7. **Gestion des messages** :  
   - **Réception des messages** : Les nouveaux messages apparaissent dans le cadre à gauche. Les anciens messages peuvent être consultés en utilisant la molette de la souris dans ce cadre.  
   - **Envoi de messages** : Une boîte de dialogue située en bas à gauche permet de rédiger et d’envoyer des messages.

8. **Affichage d’un exemple de dessin** :  
   - Chargez une image à partir d’un lien ou d’un chemin local pour l’utiliser comme référence pour le dessin collaboratif.
