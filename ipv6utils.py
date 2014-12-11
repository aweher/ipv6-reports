#!/usr/bin/env python
import re
def extraerprefijos(archivo='feeds/ipv6.txt'):
    ''' Extrae los datos de la tabla de BGP de un archivo de texto que contiene la salida
        del comando 'show bgp ipv6 unicast' en un dispositivo Cisco'''
    
    re_validation = r'^\s*([VvIiNn])'
    re_status = r'^\s*[VvIiNn]?([sdhrSmbfxac\*][\>]?[iI]?)'
    re_prefix = r'([0-9A-Fa-f\:]{3,39}\/[0-9]{1,3})'
    re_nexthop = r'[0-9A-Fa-f\:]{3,39}\/[0-9]{1,3}\s+([0-9A-Fa-f\:]{3,39})'
    re_aspath = r'.*0 (.*) [i\?]\s*$'
    re_origin = r'.*([i\?])\s*$'
    with open(archivo,'r') as tabla:
        lineas = tabla.readlines()
        a = 0
        prefijos=[]
        for linea in lineas:
            if a == 0:
                validation=""
                status=""
                prefix=""
                aspath=""
                origin=""
            busq = re.search(re_validation,linea.strip())
            if busq:
                validation = busq.group()
            busq = re.search(re_status,linea.strip())
            if busq:
                status = busq.group(1)
                a += 1
            busq = re.search(re_prefix,linea.strip())
            if busq:
                prefix = busq.group()
                a += 1
            busq = re.search(re_nexthop,linea.strip())
            if busq:
                nexthop = busq.group(1)
            busq = re.search(re_aspath,linea.strip())
            if busq:
                aspath = busq.group(1)
                a += 1
            busq = re.search(re_origin,linea.strip())
            if busq:
                origin = busq.group(1)
                a += 1
            if (a > 3):
                prefijos+=[{'validation':validation, "status":status, "prefix":prefix, "nexthop":nexthop, "aspath":aspath, "origin":origin}]
                a = 0     
        return(prefijos)
    
def buscar(busqueda, valor, store=dict()):
    '''Devuelve una lista de todos los registros que contienen busqueda==valor en un diccionario'''
    assert valor is not None
    return [d for d in store if d[busqueda].lower() == valor.lower()]