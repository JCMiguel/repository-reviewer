#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import logging
import logging.config
import traceback
import sys

# Variables globales de comportamiento
__debug_flag = False

def get_index_card(args) -> int:
    '''
        get_index_card
    '''
    print('TODO: Get Index Card')
    return 0

def edit_index_card(args) -> int:
    '''
        get_index_card
    '''
    print('TODO: Edit Index Card')
    return 0

def delete_index_card(args) -> int:
    '''
        get_index_card
    '''
    print('TODO: Delete Index Card')
    return 0

def save_index_card(args) -> int:
    '''
        set_index_card
    '''
    print('TODO: Save Index Card')
    return 0

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def main() -> int:
    # Create the arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', required=False)
    sp = parser.add_subparsers()
    get_parser  = sp.add_parser('get')
    get_parser.add_argument('data', metavar='data', type=str)
    get_parser.set_defaults(func=get_index_card)

    save_parser = sp.add_parser('save')
    save_parser.add_argument('--to', dest='dest', type=str, required=False)
    save_parser.set_defaults(func=save_index_card)

    #parser.add_argument('mode', choices=['get','save','edit','delete','list'])
    #parser.add_argument('--to', dest='dest', type=str, required=False)
    #parser.add_argument('data', metavar='data', type=str)


    args = parser.parse_args()
    data = args.func(args)
    print('DATA =' + str(data))
    
    print("Cargando archivo de configuración")
    cfg = read_yaml("config/indexer_config.yml") # TODO: Pendiente hacer chequeo de errores

    # FIXME: Deberia borrar esto porque fue una prueba
    # # Cargamos el diccionario
    #logging.config.dictConfig((cfg['params'])['logs'])
    # # Creamos el logger definido en el archivo de configuraci�n
    #logger = logging.getLogger('Logger_Example')

    if args.debug:
        print("El debug esta habilitado")
        __debug_flag = True
    else:
        __debug_flag = False

    __success_flag = False
    #if args.mode == 'get':
    #    print('TODO: Get Index Card')
    #elif args.mode == 'save':
    #    print('TODO: Save Index Card')
    #elif args.mode == 'edit':
    #    print('TODO: Edit Index Card')
    #elif args.mode == 'delete':
    #    print('TODO: Delete Index Card')
    #elif args.mode == 'list':
    #    print('TODO: List all index cards')
    #else:
    #    print('ERROR: modo no permitido')

    print("Fin de ejecución")
    exit(0)

if __name__ == "__main__" :
    sys.exit(main())
