#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import traceback
from repos import *

# Create the arguments parser
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest='debug', action='store_true', required=False)
parser.add_argument('--title', dest='title', type=str, required=False)
parser.add_argument('--abstract', dest='abstract', type=str, required=False)
parser.add_argument('--from-year', dest='fromYear', type=str, required=False)
parser.add_argument('--to-year', dest='toYear', type=str, required=False)
parser.add_argument('default_query', metavar='query', type=str)


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def holaMundo(name='Mysterious Someone'):
    print("Hola " + name + " :)")


if __name__ == "__main__" :
    args = parser.parse_args()
    
    '''
    TODO: Migrar esto a una función que parseé los argumentos.
    if not args.title:
        holaMundo()
    else:
        holaMundo(args.title)
    '''
    if args.debug:
        print("El debug esta habilitado")
        __debug_flag = True
    else:
        __debug_flag = False


    print("Cargando archivo de configuración")
    cfg = read_yaml("config.yml") # TODO: Pendiente hacer chequeo de errores
    #TODO: validar errores en el config.yml. hay que asegurar que exista todo lo necesario.
    # Ejemplo: url, params, apikey, etc.
    # Y que exista una clase llamada como en el config.yml

    print("Cargando clases de repositorios")
    #repos = [ 'ieee', 'scopus' ]
    #print(globals())
    for repo in cfg['repos'].keys():
        try:
            # La línea siguiente invoca a la clase dentro del package.
            # Ejemplo: invoca al constructor ieee() de repos.ieee_def
            if cfg['repos'][repo]['enabled'] is True:
                id = getattr(globals()[repo + '_def'], repo)(cfg['repos'][repo], cfg['params'], __debug_flag)
                if id is not None:
                    id.say_hello()
                    id.add_query_param(args.default_query)
                    id.add_query_param(args.fromYear,'from_year')
                    id.add_query_param(args.title,'title')
                    id.search()
                    del id
        except Exception:
            traceback.print_exc()
    #del repos

    print("Fin de ejecución")