#!/usr/bin/python3
# -*- coding: utf8

from engine.base import BasicEngine
import pandas as pd
from itertools import chain, repeat
from datetime import datetime
import os


class Indexer(BasicEngine):
    """
        Una clase destinada a hacer el fichaje de artículos
    """
    def __init__(self):
        super().__init__()

    """
        Métodos privados de la clase Indexer
    """
    def __input_a_date(self, message: str) -> str:
        message = ' > ' + message + ':\n    '
        bad_input_msg = "Se aceptan solo caracteres imprimibles!\n"
        prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
        replies = map(input, prompts)
        return next(filter(str.isprintable, replies))  # valid_response

    def __input_a_boolean(self, message: str) -> bool:
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

    def __input_a_text(self, message: str) -> str:
        message = ' > ' + message + ':\n    '
        bad_input_msg = "Se aceptan solo caracteres imprimibles!\n"
        prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
        replies = map(input, prompts)
        return next(filter(str.isprintable, replies))  # valid_response

    def __input_a_number(self, message: str) -> str:
        message = ' > ' + message + ':\n    '
        bad_input_msg = "El dato debe ser numérico!\n"
        prompts = chain([message], repeat('\n'.join([bad_input_msg, message])))
        replies = map(input, prompts)
        return next(filter(str.isdigit, replies))  # valid_response

    def __index_an_article(self) -> dict:
        new_dict = dict.fromkeys(self._base_dict_df.keys())
        for item in self._base_dict_df.items():
            item_type = item[1]
            item_name = item[0]
            if item_type == 'string':
                new_dict[item[0]] = self.__input_a_text(item_name)
            elif item_type == 'int32':
                new_dict[item[0]] = self.__input_a_number(item_name)
            elif item_type == 'boolean':
                new_dict[item[0]] = self.__input_a_boolean(item_name)
            elif item_type == 'datetime64[ns]':
                new_dict[item[0]] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif item_type == 'automatic':
                new_dict[item[0]] = ''
            else:
                new_dict[item[0]] = self.__input_a_text(item_name)
        return new_dict

    def __load_dataframe(self, filename: str) -> pd.DataFrame:
        fichas = pd.read_csv(filename, index_col=False)
        fichas = fichas.fillna('')
        return fichas.astype(self._base_dict_df)

    def __match_with_filter(self, args: dict, ficha: pd.DataFrame, index: int) -> bool:
        match_flag = False
        if 'all' in args.keys() and args['all'] is not None:
            match_flag = True
        elif 'index' in args.keys() and args['index'] is not None:
            if args['index'] == str(ficha.index.values[0]):
                match_flag = True
        elif 'filename' in args.keys() and args['filename'] is not None:
            # FIXME: Esta línea rompe el encapsulamiento de _base_dict_df
            # FIXME: 'Nombre de archivo' debería ser dinámico.
            if args['filename'] in str(ficha['Nombre de archivo'].values):
                match_flag = True
        else:
            match_flag = False
        return match_flag

    """
        Métodos públicos de la clase Indexer
    """
    def get_index_card(self, args) -> int:
        """
            get_index_card
        """
        # print(f'args: {args}')
        if os.path.isfile('fichas.csv'):
            # Abro el csv con pandas
            fichas = self.__load_dataframe('fichas.csv')
            for i in range(0, len(fichas.index)):
                # TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
                if self.__match_with_filter(vars(args), fichas.iloc[[i]], i):
                    print('----------------------------------------------------')
                    print(f'              FICHA SELECCIONADA - INDEX {i}')
                    print('----------------------------------------------------')
                    for item in self._base_dict_df.items():
                        item_name = item[0]
                        value = fichas[item_name].values[i]
                        if len(str(value)) > 0:
                            print(f' > {item_name}:\n    {value}')
        else:
            print("No hay ninguna ficha cargada")
        return 0

    def edit_index_card(self, args) -> int:
        """
            get_index_card
        """
        if os.path.isfile('fichas.csv'):
            # Abro el csv con pandas
            fichas = self.__load_dataframe('fichas.csv')
            print('----------------------------------------------------')
            print('              FICHA A EDITAR')
            print('----------------------------------------------------')
            # TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
            for item in self._base_dict_df.items():
                item_name = item[0]
                print(f' > {item_name}:\n    {fichas[item_name].values[args.index]}')
            if self.__input_a_boolean("¿Está seguro que desea editar esta ficha?"):
                new_dict = self.__index_an_article()
                edited_ficha = pd.DataFrame(new_dict, index=[args.index])
                edited_ficha.astype(self._base_dict_df)
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

    def delete_index_card(self, args) -> int:
        """
            get_index_card
        """
        if os.path.isfile('fichas.csv'):
            # Abro el csv con pandas
            fichas = self.__load_dataframe('fichas.csv')
            print('----------------------------------------------------')
            print('              FICHA A EDITAR')
            print('----------------------------------------------------')
            # TODO: Pendiente agregar un filtro acá en función de algún argumento de ejecución
            for item in self._base_dict_df.items():
                item_name = item[0]
                print(f' > {item_name}:\n    {fichas[item_name].values[args.index]}')
            if self.__input_a_boolean("¿Está seguro que desea eliminar esta ficha?"):
                fichas = fichas.drop(labels=args.index, axis=0)
                fichas.to_csv('fichas.csv', encoding='utf-8', index=False)
            else:
                print("Cancelando borrado")
        else:
            print("No hay ninguna ficha cargada")
        return 0

    def save_index_card(self, args) -> int:
        """
            set_index_card
        """
        print('········· Generación de nueva ficha ·········')
        print('Ingrese los datos pedidos a continuación')
        new_dict = self.__index_an_article()

        if os.path.isfile('fichas.csv'):
            # Abro el csv con pandas
            fichas = self.__load_dataframe('fichas.csv')
            # FIXME: Esta línea rompe si el archivo existe pero no tiene contenido.
            new_ficha = pd.DataFrame(new_dict, index=[len(fichas) + 1])
            frames = [fichas, new_ficha]
            fichas = pd.concat(frames)
        else:
            fichas = pd.DataFrame(new_dict, index=[0])
            fichas.astype(self._base_dict_df)

        fichas.to_csv('fichas.csv', encoding='utf-8', index=False)
        return 0
