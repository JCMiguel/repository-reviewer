import customtkinter as ctk
from abc import ABC, abstractmethod

class BasePageFrame(ctk.CTkFrame, ABC):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

    @abstractmethod
    def on_init(self):
        pass

    @abstractmethod
    def on_showing(self):
        pass

    @abstractmethod
    def on_hiding(self):
        pass

    @abstractmethod
    def set_contextual(self, data):
        pass
    