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
1. **Démarrer le programme principal** :  
   ```powershell
   python .\Host.py
   ```
2. Le système prendra **10 secondes** pour se lancer. Cela ouvrira **3 terminaux**, y compris celui de `whiteboard`.
3. Connecter le terminal `whiteboard` à un réseau.

---

### 3) Lancer l'interface utilisateur
1. Sur un PC connecté au **même réseau** que le PixelPlace Host, démarrer le programme client :  
   ```powershell
   python .\Client.py
   ```

---

N'hésitez pas à adapter les instructions en fonction de vos besoins spécifiques ou à ajouter des sections supplémentaires si nécessaire. 😊