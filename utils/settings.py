import os
import json
import sys


class Funcs(object):
  def readFile(self, f):
    with open(f, encoding='utf-8') as _f:
      return _f.read()

  def getConfig(self, d, k):
    if os.path.exists(GlobalVars().path + 'config.json'):
      config = json.loads(self.readFile(GlobalVars().path + 'config.json'))
      return config[d][k]
    else:
      print('[ERROR] No se ha podido leer el archivo de configuración')
      sys.exit()

class GlobalVars(object):
  @property
  def path(self):
    return '' #Ruta absoluta para el bot cuando es utilizado como "daemon proccess"

  @property
  def token(self):
    return Funcs().getConfig('dualipa', 'token') #Token para el BOT

  @property
  def root_role(self):
    return Funcs().getConfig('dualipa', 'rootRole') #Nombre del rango administrativo superior del servidor

  @property
  def prefix(self):
    return Funcs().getConfig('dualipa', 'prefix') #Prefijo para los comandos de DualipaBOT

  @property
  def cogs(self):
    return Funcs().getConfig('dualipa', 'cogs') #Sub-módulos del bot
