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
