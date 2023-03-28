#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import logging
import logging.config
import traceback
import numpy as np
import pandas as pd
import os
import sys

# Variables globales de comportamiento
__debug_flag = False
# Este diccionario tiene dos funciones importantísimas
#  1. Sirve como plantilla de ficha en todos los métodos del CRUD
#  2. Sirve para especificar, cuando se levanta el .csv, qué tipo de dato tiene cada columna
# Cualquier cambio que haya que hacer en las fichas, debe hacerse también en este diccionario
__base_dict_df = {'file': 'string',
                  'title':'string',
                  'author':'string',
                  'repo':'string',
                  'year':'int32',
                  'date':'datetime64[ns]',
                  'abstract':'string',
                  'keywords':'string',
                  'refs':'string',
                  'pros':'string',
                  'cons':'string',
                  'opps':'string'}


def load_dataframe(filename) -> pd.DataFrame:
    fichas = pd.read_csv(filename, index_col=0)
    fichas = fichas.fillna('')
    return fichas.astype(__base_dict_df)

def get_index_card(args) -> int:
    '''
        get_index_card
    '''
    print('TODO: Get Index Card')

    if(os.path.isfile('fichas.csv')):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        ficha = fichas.loc[fichas['file'] == args.filename]

        #print(ficha)
        #print(ficha.dtypes)
        if ficha is not None:
            for i in range(0,len(fichas.index)-1):
                print('----------------------------------------------------')
                print('              FICHA SELECCIONADA')
                print('----------------------------------------------------')
                print(' > Nombre de archivo:\n    '+ ficha['file'].values[i])
                print(' > Título:\n    '+ ficha['title'].values[i])
                print(' > Autor(es):\n    '+ ficha['author'].values[i])
                print(' > Medio de publicación:\n    '+ ficha['repo'].values[i])
                print(' > Año de publicación:\n    '+ str(ficha['year'].values[i]))
                print(' > Fecha de búsqueda:\n    '+ str(ficha['date'].values[i]))
                print(' > Abstract:\n    '+ ficha['abstract'].values[i])
                print(' > Palabras clave:\n    '+ ficha['keywords'].values[i])
                print(' > Referencias importantes:\n    '+ ficha['refs'].values[i])
                print(' > Fortalezas:\n    '+ ficha['pros'].values[i])
                print(' > Debilidades:\n    '+ ficha['cons'].values[i])
                print(' > Oportunidades:\n    '+ ficha['opps'].values[i])
                print('----------------------------------------------------')
        else:
            print(' [!] Ficha no encontrada')
    else:
        print("No hay ninguna ficha cargada")
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
    print('········· Generación de nueva ficha ·········')
    print('Ingrese los datos pedidos a continuación')
    new_dict = dict.fromkeys(__base_dict_df.keys())
    #TODO: Validar datos ingresados por el usuario
    new_dict['file']        = input(' > Nombre de archivo:\n    ')
    new_dict['title']       = input(' > Título:\n    ')
    new_dict['author']      = input(' > Autor(es):\n    ')
    new_dict['repo']        = input(' > Medio de publicación:\n    ')
    new_dict['year']        = input(' > Año de publicación:\n    ')
    new_dict['date']        = input(' > Fecha de búsqueda:\n    ')
    new_dict['abstract']    = input(' > Abstract:\n    ')
    new_dict['keywords']    = input(' > Palabras clave:\n    ')
    new_dict['refs']        = input(' > Referencias importantes:\n    ')
    new_dict['pros']        = input(' > Fortalezas:\n    ')
    new_dict['cons']        = input(' > Debilidades:\n    ')
    new_dict['opps']        = input(' > Oportunidades:\n    ')

    if(os.path.isfile('fichas.csv')):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        new_ficha = pd.DataFrame(new_dict, index=[fichas.index[-1]+1])
        frames = [fichas, new_ficha]

        #print('DEBUG')
        #print(fichas)
        #print('----------------------------------------------------')
        #print(new_ficha)

        fichas = pd.concat(frames)
    else:
        fichas = pd.DataFrame(new_dict, index=[0])
    
    fichas.to_csv('fichas.csv', encoding='utf-8')
    return 0


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def main() -> int:
    # Create the arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', required=False)
    sp = parser.add_subparsers()

    # GET
    get_parser  = sp.add_parser('get')
    get_parser.add_argument('filename', metavar='filename', type=str)
    get_parser.set_defaults(func=get_index_card)

    # SAVE
    save_parser = sp.add_parser('save')
    save_parser.add_argument('--to', dest='dest', type=str, required=False)
    save_parser.set_defaults(func=save_index_card)

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
