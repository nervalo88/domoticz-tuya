# Domoticz Tuya, *by nervalo88*

Fork depuis https://github.com/BreizhCat/domoticz-tuya

- retrait du contenu documentaire initial (pour eviter un doublon)
- remplacement des ID par des mot-cles depuis `code.json` fonctionnel
- support de commandes de volets roulants 

## Usage

### Ligne de commande

- `tuya.py --status <ID>'` obtenir le statut de l'appareil
- `tuya.py --switchLed <ID> <True|False>'` commander une lampe
- `tuya.py --toggleLed <ID>\n'` permuter l'etat d'une lampe
- `tuya.py --shutter <ID> <open|close|stop>'` commander une lampe

### TODO : Script python DZvent

## Configuration
1. Creer un compte sur https://iot.tuya.com
2. Dans la catégorie __cloud__ -->  **Create Cloud Project** 
3. Dans le projet nouvellement crée
⋅⋅* Choisir le datacenter correspondant à votre zone (Central Europe)
⋅⋅* Devices
⋅⋅* Link Tuya App Account
⋅⋅* Add App Account
Depuis l'application mobile scannez le QR code affiché
4. renseigner `code.json` avec les infos de *Overvvew - Authorization Key* :
⋅⋅* `"client_id":` Access ID/Client ID
⋅⋅* `"app_id":` Access Secret/Client Secret
