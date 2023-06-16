#!/usr/bin/python3
# -*- coding: utf8

import argparse
import yaml
import logging
import logging.config
import traceback
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
# TODO: ¿Extender estructura del diccionario al config.yml?
# TODO: Iterar sobre la estructura del diccionario e invocar input_a_text o input_a_number,
#       en función del tipo de dato que esté definido en el diccionario
__base_dict_df = {  # Nombre del archivo - artículo descargado
                    'Nombre de archivo': 'string',
                    # Título del artículo
                    'Título': 'string',
                    # Autor(es) del artículo
                    'Autor(es)': 'string',
                    # Indica si es un estudio primario
                    'Estudio primario': 'boolean',
                    # Indica si su análisis está pendiente
                    'Pendiente analizar': 'boolean',
                    # Repositorio donde fue hallado el artículo
                    'Medio de publicación': 'string',
                    # Año de publicación
                    'Año de publicación': 'int32',
                    # Fecha de fichaje
                    'Fecha de fichaje': 'datetime64[ns]',
                    # Abstract
                    'Abstract': 'string',
                    # Palabras clave del artículo
                    'Palabras clave': 'string',
                    # Trabajos de otros autores mencionados en la publicación que podrían
                    #    ser útiles para ampliar el tema
                    'Referencias a otros artículos': 'string',
                    # Aspectos metodológicos o conceptuales angulares para la investigación
                    'Fortalezas': 'string',
                    # Aspectos que no están bien desarrollados o no resultan claros
                    'Debilidades': 'string',
                    # Posibles líneas de trabajo para la tesis
                    'Oportunidades': 'string'
                 }


def input_a_date(message: str) -> str:
    message = ' > ' + message + ':\n    '
    bad_input_msg = "Se aceptan solo caracteres imprimibles!\n"
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isprintable, replies))  # valid_response


def input_a_boolean(message: str) -> bool:
    message = ' > ' + message + '(y/n):\n    '
    done = False
    ans = ''
    while not done:
        ans = input(message)
        if ans.lower() in ["y", "n"]:
            done = True
        else:
            print("Se acepta solo Y o N!\n")
    if ans == "y":
        return True
    return False


def input_a_text(message: str) -> str:
    message = ' > ' + message + ':\n    '
    bad_input_msg = "Se aceptan solo caracteres imprimibles!\n"
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isprintable, replies))  # valid_response


def input_a_number(message: str) -> str:
    message = ' > ' + message + ':\n    '
    bad_input_msg = "El dato debe ser numérico!\n"
    prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
    replies = map(input, prompts)
    return next(filter(str.isdigit, replies))  # valid_response


def index_an_article() -> dict:
    new_dict = dict.fromkeys(__base_dict_df.keys())
    for item in __base_dict_df.items():
        item_type = item[1]
        item_name = item[0]
        if item_type == 'string':
            new_dict[item[0]] = input_a_text(item_name)
        elif item_type == 'int32':
            new_dict[item[0]] = input_a_number(item_name)
        elif item_type == 'boolean':
            new_dict[item[0]] = input_a_boolean(item_name)
        elif item_type == 'datetime64[ns]':
            new_dict[item[0]] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif item_type == 'automatic':
            new_dict[item[0]] = ''
        else:
            new_dict[item[0]] = input_a_text(item_name)
    return new_dict


def load_dataframe(filename) -> pd.DataFrame:
    fichas = pd.read_csv(filename, index_col=False)
    fichas = fichas.fillna('')
    return fichas.astype(__base_dict_df)


def get_index_card(args) -> int:
    """
        get_index_card
    """
    if os.path.isfile('fichas.csv'):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        for i in range(0, len(fichas.index)):
            #TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
            print('----------------------------------------------------')
            print(f'              FICHA SELECCIONADA - INDEX {i}')
            print('----------------------------------------------------')
            for item in __base_dict_df.items():
                item_name = item[0]
                print(f' > {item_name}:\n    {fichas[item_name].values[i]}')
    else:
        print("No hay ninguna ficha cargada")
    return 0


def edit_index_card(args) -> int:
    """
        get_index_card
    """
    if os.path.isfile('fichas.csv'):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        print('----------------------------------------------------')
        print('              FICHA A EDITAR')
        print('----------------------------------------------------')
        #TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
        for item in __base_dict_df.items():
            item_name = item[0]
            print(f' > {item_name}:\n    {fichas[item_name].values[args.index]}')
        if input_a_boolean("¿Está seguro que desea editar esta ficha?") == True:
            new_dict = index_an_article()
            edited_ficha = pd.DataFrame(new_dict, index=[args.index])
            edited_ficha.astype(__base_dict_df)
            print(fichas)
            print(edited_ficha)
            fichas.loc[edited_ficha.index, :] = edited_ficha[:]
            print(fichas)
            fichas.to_csv('fichas.csv', encoding='utf-8', index=False)
        else:
            print("Cancelando edición")
    else:
        print("No hay ninguna ficha cargada")
    return 0


def delete_index_card(args) -> int:
    """
        get_index_card
    """
    if os.path.isfile('fichas.csv'):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        print('----------------------------------------------------')
        print('              FICHA A EDITAR')
        print('----------------------------------------------------')
        #TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
        for item in __base_dict_df.items():
            item_name = item[0]
            print(f' > {item_name}:\n    {fichas[item_name].values[args.index]}')
        if input_a_boolean("¿Está seguro que desea eliminar esta ficha?") == True:
            fichas = fichas.drop(labels=args.index, axis=0)
            fichas.to_csv('fichas.csv', encoding='utf-8', index=False)
        else:
            print("Cancelando borrado")
    else:
        print("No hay ninguna ficha cargada")
    return 0


def save_index_card(args) -> int:
    """
        set_index_card
    """
    print('········· Generación de nueva ficha ·········')
    print('Ingrese los datos pedidos a continuación')
    new_dict = index_an_article()

    if os.path.isfile('fichas.csv'):
        # Abro el csv con pandas
        fichas = load_dataframe('fichas.csv')
        # FIXME: Esta línea rompe si el archivo existe pero no tiene contenido.
        new_ficha = pd.DataFrame(new_dict, index=[fichas.index[-1] + 1])
        frames = [fichas, new_ficha]
        fichas = pd.concat(frames)
    else:
        fichas = pd.DataFrame(new_dict, index=[0])
        fichas.astype(__base_dict_df)

    fichas.to_csv('fichas.csv', encoding='utf-8', index=False)
    return 0


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def main() -> int:
    #print("Cargando archivo de configuración")
    #cfg = read_yaml("config/indexer_config.yml")

    # Create the arguments parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', required=False)
    sp = parser.add_subparsers()

    # GET
    get_parser = sp.add_parser('get')
    get_parser.add_argument('filename', metavar='filename', type=str)
    get_parser.set_defaults(func=get_index_card)

    # SAVE
    save_parser = sp.add_parser('save')
    save_parser.add_argument('--to', dest='dest', type=str, required=False)
    save_parser.set_defaults(func=save_index_card)

    # EDIT
    edit_parser = sp.add_parser('edit')
    edit_parser.add_argument('index', metavar='index', type=int)
    edit_parser.set_defaults(func=edit_index_card)

    # DELETE
    delete_parser = sp.add_parser('delete')
    delete_parser.add_argument('index', metavar='index', type=int)
    delete_parser.set_defaults(func=delete_index_card)

    args = parser.parse_args()
    data = args.func(args)
    #print('DATA =' + str(data))

    # FIXME: Debería borrar esto porque fue una prueba
    # # Cargamos el diccionario
    # logging.config.dictConfig((cfg['params'])['logs'])
    # # Creamos el logger definido en el archivo de configuración
    # logger = logging.getLogger('Logger_Example')

    if args.debug:
        print("El debug esta habilitado")
        __debug_flag = True
    else:
        __debug_flag = False

    __success_flag = False

    print("Fin de ejecución")
    exit(0)


if __name__ == "__main__":
    sys.exit(main())
