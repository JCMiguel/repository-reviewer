#!/usr/bin/python3
# -*- coding: utf8

from historic.search import Search

class History:

    def __init__(self):
        raise NotImplemented("Revisar los atributos necesarios para inicializar la clase")

    def Add(self, search:Search):
        raise NotImplemented("Recibe un registro de busqueda y lo guarda en el historial")

    def Get(self, id):
        raise NotImplemented("Recuperar un registro con el tiempo de la busqueda -hhmmss u otros")

    def Get(self, index):
        raise NotImplemented("Recuperar un registro con el indice que indica cuantas busquedas atras se ha realizado")

    def Get(self, str_match):
        raise NotImplemented("Recuperar un registro con un string que matchee el contenido del registro")