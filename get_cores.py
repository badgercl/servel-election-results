#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
import json
from time import sleep
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getAll():
	d = []
	j = get_data(0,'all')
	for r in j:
		d.append(getCircSenatoriales(r))
	return d

def getCircSenatoriales(c):
	j = get_data(c['c'],'senatorial')
	c['senatoriales'] = []
	for r in j:
		c['senatoriales'].append(getDistritos(r))
	return c

def getDistritos(s):
	j = get_data(s['c'], 'distritro')
	s['distritos'] = []
	for r in j:
		s['distritos'].append( getComunas(r) ) 
	return s

def getComunas(d):
	j = get_data(d['c'], 'comuna')
	d['comunas'] = []
	for r in j:
		d['comunas'].append( getConteo(r) )
	return d
'''
def getCircElectorales(c):
	j = get_data(c['c'], 'electoral')
	c['electoral'] = []
	for r in j:
		c['electoral'].append( getLocales(r) )
	return c

def getLocales(c):
	j = get_data(c['c'], 'local')
	c['mesas'] = []
	for r in j:
		c['mesas'].append(getMesas(r))
	return c

def getMesas(l):
	j = get_data(l['c'], 'mesa')
	l['conteo'] = []
	for r in j:
		l['conteo'].append(getConteo(r))
	return l
'''
def getConteo(m):
	j = get_data(m['c'], 'conteo_core')
        m['conteo'] = j;
        return m

def get_url(i,t):
	if t == 'all': url = "http://www.servelelecciones.cl/data/elecciones_presidente/filters/regiones/all.json"
	elif t == 'senatorial': url = "http://www.servelelecciones.cl/data/elecciones_presidente/filters/circ_senatorial/byregion/{}.json".format(i)
	elif t == 'distritro': url = "http://www.servelelecciones.cl/data/elecciones_presidente/filters/distritos/bycirc_senatorial/{}.json".format(i)
	elif t == 'comuna':url = "http://www.servelelecciones.cl/data/elecciones_presidente/filters/comunas/bydistrito/{}.json".format(i)
        elif t == 'conteo_core':url = "http://www.servelelecciones.cl/data/elecciones_cores/computo/comunas/{}.json".format(i)
	return url

def get_data(i, t):
	url = ""
	path = "./data/{}_{}.json".format(t,i)
	if os.path.isfile( path ) :
		print("cache: {}".format(path))
		f = open ( path )
		res = json.loads(f.read())
		f.close()
		return res
	else:
		sleep(1)
		url = get_url(i,t)
		print("req: {}".format(url))
		r = requests.get(url)
		j = json.loads(r.text)
		save(path, r.text)
		return j

def save(path,txt):
	f = open(path, 'w')
	f.write(txt)
	f.close()

res = getAll()

f = open('servel2017_core.json', 'w')
f.write(json.dumps(res))
f.close()

