# Usage

### Ligne de commande
  
- `tuya.py --status <ID>'` obtenir le statut de l'appareil
- `tuya.py --switchLed <ID> <True|False>'` commander une lampe
- `tuya.py --toggleLed <ID>\n'` permuter l'etat d'une lampe
- `tuya.py --shutter <ID> <open|close|stop>'` commander un volet roulant

### Integration sous Domoticz



## Configuration
1. Creer un compte sur https://iot.tuya.com
2. Dans la catégorie __cloud__ -->  **Create Cloud Project** 
3. Dans le projet nouvellement crée
  - Choisir le datacenter correspondant à votre zone (Central Europe)
  - Devices
  - Link Tuya App Account
  - Add App Account
Depuis l'application mobile scannez le QR code affiché
4. renommer `code.json.model` en `code.json`
5. renseigner `code.json` avec les infos de *Overvvew - Authorization Key* :
  -  `"client_id":` Access ID/Client ID
  -  `"app_id":` Access Secret/Client Secret

# Projet originel
Fork depuis [BreizhCat/domoticz-tuya](https://github.com/BreizhCat/domoticz-tuya)

- retrait du contenu documentaire initial (pour eviter un doublon)
- remplacement des ID par des mot-cles depuis `code.json` fonctionnel
- support de commandes de volets roulants 

*impossible (dans mon cas) de faire fonctionner les projets de plus grande ampleur tels que `tuyaha` ou [Xenomes/Domoticz-TUYA-Plugin](https://github.com/Xenomes/Domoticz-TUYA-Plugin), problèmes rencontrès des l'authentification, ces projets ne semblent pas compatibles avec les volets roulants (non testé)*

# ARCHIVE
### Integration sous Domoticz
Nous envisagions d'utiliser le script `script_device_curtain.lua` pour interagir avec Domoticz, qui doit se trouver sous `/home/<user>/domoticz/scripts/lua`. 
```sh
cd /home/<user>/domoticz/scripts/lua 
git clone https://github.com/nervalo88/domoticz-tuya.git
ln ./domoticz-tuya/script_device_curtain.lua script_device_curtain.lua 
```
Pas necessaire, un *selecteur virtuel* sous Domoticz permet d'appeller diverses commandes