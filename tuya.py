#!/opt/bin/python3
 
__author__ = "Nervalo88" #initially Yann LEROUX - https://github.com/BreizhCat/domoticz-tuya
# Patched due to latest tuya API change
# Added support for shutters
__version__ = "0.0.1"

import requests
import hmac
import hashlib
import json
from time import time
import sys

class tuya_api:
    def __init__(self):
        self._isLogged  = False
        self._encode   = 'HMAC-SHA256'

        self.debug     = True
        self.url_api   = "https://openapi.tuyaeu.com"
        self.full_path = ""#"/usr/local/domoticz/var/scripts/domo-tuya/"

        with open(self.full_path + 'code.json') as param_data:
            data = json.load(param_data)
            self.client_id = data['client_id']
            self.secret    = data['app_id']
            self.devices   = data['devices']

    def _debug(self, text):
        if self.debug:
            print(text)

    def _getInfo(self):
        print('Timestamp: '+str(self.timestamp))
        print('Signature:'+self.signature)
        print('Token:' + self.token)

    def _getSignature(self, token = False):
        self._debug('Get sign...')
        self.timestamp = int(time()*1000)
        if token:
            message = self.client_id + self.token + str(self.timestamp)   
        else:
            message = self.client_id + str(self.timestamp)

        self.signature = hmac.new(bytes(self.secret , 'latin-1'), msg = bytes(message, 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()

    def login(self):
        self._debug('Login...')

        self._getSignature()           
        
        header = {
            'client_id'  : self.client_id,
            'sign'       : self.signature,
            't'          : str(self.timestamp),
            'sign_method': 'HMAC-SHA256'
        }

        res = requests.get(self.url_api + '/v1.0/token?grant_type=1', headers=header)

        if res.ok: 
            result = json.loads(res.content)
            if result['success']:
                self.token = result['result']['access_token']
                self._isLogged = True
            else:
                print('Authentification Error: ' + result['msg'])
        else:
            print("HTTP %i - %s, Message %s" % (res.status_code, res.reason, res.text))
    
    def switchLed(self, id, value):
        if not self._isLogged:
            return

        self._debug("Switch a LED...")
        self._getSignature(True)
        
        header = {
            'client_id'    : self.client_id,
            'access_token' : self.token,
            'sign'         : self.signature,
            't'            : str(self.timestamp),
            'sign_method'  : self._encode,
            'Content-Type' :'application/json'
        }
        
        data = '{\n\t\"commands\":[\n\t\t{\n\t\t\t\"code\": \"switch_led\",\n\t\t\t\"value\":'+value+'\n\t\t}\n\t]\n}' 
        
        res = requests.post(self.url_api + '/v1.0/devices/' + id + '/commands', headers=header, data = data)
        if res.ok:
            result = json.loads(res.content)
            if result['success']:
                self._debug('Device ' + id + 'status set to ' + value)
            else:
                print('Execution Error: ' + result['msg'])   
        else:
            print("HTTP %i - %s, Message %s" % (res.status_code, res.reason, res.text))

    def moveShutter(self, id, value):
        ### Values open | close | stop  (added "" into the command)
        if not self._isLogged:
            return

        self._debug("move a shutter...")
        self._getSignature(True)
        
        header = {
            'client_id'    : self.client_id,
            'access_token' : self.token,
            'sign'         : self.signature,
            't'            : str(self.timestamp),
            'sign_method'  : self._encode,
            'Content-Type' :'application/json'
        }
        
        data = '{\n\t\"commands\":[\n\t\t{\n\t\t\t\"code\": \"control\",\n\t\t\t\"value\":\"'+value+'\"\n\t\t}\n\t]\n}' 
        
        res = requests.post(self.url_api + '/v1.0/devices/' + id + '/commands', headers=header, data = data)
        if res.ok:
            result = json.loads(res.content)
            if result['success']:
                self._debug('Device ' + id + 'status set to ' + value)
            else:
                print('Execution Error: ' + result['msg'])   
        else:
            print("HTTP %i - %s, Message %s" % (res.status_code, res.reason, res.text))

    def getStatus(self, id):
        if not self._isLogged:
            return

        self._debug("Get Statuts...")
        self._getSignature(True)        
       
        header = {
            'client_id'    : self.client_id,
            'access_token' : self.token,
            'sign'         : self.signature,
            't'            : str(self.timestamp),
            'sign_method'  : self._encode,
        }

        res = requests.get(self.url_api + '/v1.0/devices/'+ id+ '/status', headers=header)

        if res.ok: 
            result = json.loads(res.content)
            self._debug(result)
            if result['success']:
                return result['result'][0]['value']
            else:
                print('Authentification Error: ' + result['msg'])
        else:
            print("HTTP %i - %s, Message %s" % (res.status_code, res.reason, res.text))

    def help(self):
        print('Options available')
        print('-----------------')
        print('tuya.py --status <ID>')
        print('tuya.py --switchLed <ID> <True|False>')
        print('tuya.py --toggleLed <ID>\n')  
        print("-----DEVICES-----")
        for device in self.devices.keys():
            print(device)
        

if __name__ == '__main__':
    tuya = tuya_api()

    if len(sys.argv) <= 1:
        print("not enough arguments")
        tuya.help()
        exit()
        
    else:
        device = tuya.devices.get(sys.argv[2])
        if device == None :
            device = sys.argv[2]
        print(device)

        tuya.login()
        if sys.argv[1] == '--status':
            print(tuya.getStatus(device))

        elif sys.argv[1] == '--switchLed':
            tuya.switchLed(device, sys.argv[3])

        elif sys.argv[1] == '--shutter':
            tuya.moveShutter(device, sys.argv[3])

        elif sys.argv[1] == '--toggleLed':
            if tuya.getStatus(device):
                tuya.switchLed(device, "false")
            else:
                tuya.switchLed(device, "true")
        else: 
            print("wrong argument")
            tuya.help()
