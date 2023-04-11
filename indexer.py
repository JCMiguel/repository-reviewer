#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import logging
import logging.config
import traceback
import numpy as np
import pandas as pd
from itertools import chain, repeat
from datetime import datetime
import os
import sys


# Variables globales de comportamiento
__debug_flag = False
# Este diccionario tiene dos funciones importantísimas
#  1. Sirve como plantilla de ficha en todos los métodos del CRUD
#  2. Sirve para especificar, cuando se levanta el .csv, qué tipo de dato tiene cada columna
# Cualquier cambio que haya que hacer en las fichas, debe hacerse también en este diccionario
# TODO: Migrar estructura del diccionario al config.yml
# TODO: Iterar sobre la estructura del diccionario e invocar input_a_text o input_a_number,
#       en función del tipo de dato que esté definido en el diccionario
__base_dict_df = {'file': 'string',             # Nombre del archivo - artículo descargado
                  'title':'string',             # Título del artículo
                  'author':'string',            # Autor(es) del artículo
                  'repo':'string',              # Repositorio donde fue hallado el artículo
                  'year':'int32',               # Año de publicación
                  'date':'datetime64[ns]',      # Fecha de fichaje
                  'abstract':'string',          # Abstract
                  'keywords':'string',          # Palabras clave del artículo 
                  'refs':'string',                  
                  'pros':'string',
                  'cons':'string',
                  'opps':'string'}

def input_a_date(message:str) -> str:
    bad_input_msg = "Se aceptan solo caracteres imprimibles!\n" + message
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isprintable, replies)) #valid_response

def input_a_text(message:str) -> str:
    bad_input_msg = "Se aceptan solo caracteres imprimibles!\n" + message
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isprintable, replies)) #valid_response

def input_a_number(message:str) -> int:
    bad_input_msg = "El dato debe ser numérico!\n" + message
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isdigit, replies)) #valid_response

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
                print(' > Fecha de fichaje:\n    '+ str(ficha['date'].values[i]))
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
    new_dict['file']        = input_a_text(' > Nombre de archivo:\n    ')
    new_dict['title']       = input_a_text(' > Título:\n    ')
    new_dict['author']      = input_a_text(' > Autor(es):\n    ')
    new_dict['repo']        = input_a_text(' > Medio de publicación:\n    ')
    new_dict['year']        = input_a_number(' > Año de publicación:\n    ')
    new_dict['date']        = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dict['abstract']    = input_a_text(' > Abstract:\n    ')
    new_dict['keywords']    = input_a_text(' > Palabras clave:\n    ').lower()
    new_dict['refs']        = input_a_text(' > Referencias importantes a otros archivos:\n    ')
    new_dict['pros']        = input_a_text(' > Fortalezas:\n    ')
    new_dict['cons']        = input_a_text(' > Debilidades:\n    ')
    new_dict['opps']        = input_a_text(' > Oportunidades:\n    ')

    if(os.path.isfile('fichas.csv')):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        new_ficha = pd.DataFrame(new_dict, index=[fichas.index[-1]+1])
        frames = [fichas, new_ficha]
        fichas = pd.concat(frames)
    else:
        fichas = pd.DataFrame(new_dict, index=[0])
        fichas.astype(__base_dict_df)
    
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

    print("Fin de ejecución")
    exit(0)

if __name__ == "__main__" :
    sys.exit(main())
