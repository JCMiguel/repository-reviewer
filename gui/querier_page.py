import customtkinter as ctk
from tkinter import messagebox
import json

import engine
from .base_page import *
from .misc import execute
from datetime import datetime
from engine.querier import *


class QuerierPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)
        self.create_tabview( parent )

    def on_init(self):
        pass

    def on_showing(self):
        pass

    def on_hiding(self):
        pass

    def on_resume(self):
        pass  

    def set_contextual(self, data):
        pass

    def create_tabview(self, parent):
        def_txt = "Inserte texto aquí"
        view = None
        second_tab = view
        self.tabview = ctk.CTkTabview(self, width=parent.cget("width"))
        self.tabview.pack(side="top", padx=20, pady=10, fill="x")
        self.tabview.add("Búsqueda básica")
        self.tabview.add("Búsqueda avanzada")
        self.tabview.tab("Búsqueda básica")
        self.tabview.tab("Búsqueda avanzada")
        view = self.tabview.tab("Búsqueda básica")
        second_tab = self.tabview.tab("Búsqueda avanzada")

        # Tab - Búsqueda básica
        self.querier_title_lbl = ctk.CTkLabel(view, text="Title", anchor="w",
                                              font=ctk.CTkFont(weight="bold"))
        self.querier_title_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_entry_title = ctk.CTkEntry(view, placeholder_text=def_txt)
        self.querier_entry_title.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_abs_lbl = ctk.CTkLabel(view, text="Abstract", anchor="w",
                                            font=ctk.CTkFont(weight="bold"))
        self.querier_abs_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_entry_abs = ctk.CTkEntry(view, placeholder_text=def_txt)
        self.querier_entry_abs.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_key_lbl = ctk.CTkLabel(view, text="Keywords", anchor="w",
                                            font=ctk.CTkFont(weight="bold"))
        self.querier_key_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_entry_key = ctk.CTkEntry(view, placeholder_text=def_txt)
        self.querier_entry_key.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_content_lbl = ctk.CTkLabel(view, text="Content", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_content_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_entry_content = ctk.CTkEntry(view, placeholder_text=def_txt)
        self.querier_entry_content.pack(side="top", padx=20,  pady=5, fill="x")

        # Tab - Búsqueda avanzada
        self.querier_query_lbl = ctk.CTkLabel(second_tab, text="Query", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_query_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_entry_query = ctk.CTkEntry(second_tab, placeholder_text=def_txt)
                                 # ctk.CTkTextbox(second_tab,
                                 # [TODO]         height=226, activate_scrollbars=True,
                                 #                border_color="dark grey", border_width=2)
        self.querier_entry_query.pack(side="top", padx=20, pady=5, fill="both")

        # Common (out of tabs)
        self.querier_search_btn = ctk.CTkButton(self, text="Search!",
                                                command=self.search_btn_event)
        self.querier_search_btn.pack(side="top", padx=20, pady=10)


    def search_btn_event(self):
        # TODO: Work In Progress
        texto = ""
        texto += f'Title({self.querier_entry_title.get()}) - '
        texto += f'Abs({self.querier_entry_abs.get()}) - '
        texto += f'Key({self.querier_entry_key.get()}) - '
        texto += f'Content({self.querier_entry_content.get()}) - '
        texto += f'Query({self.querier_entry_query.get()})'
        if texto != 'Title() - Abs() - Key() - Content() - Query()':
            print(f'{this_time()} - Buscando...\n')
            # TODO: FIXME: al invocar esta función, la pantalla se queda congelada hasta finalizar la búsqueda
            querier_args = build_querier_dictionary(query=self.querier_entry_query.get(),
                                                    content=self.querier_entry_content.get(),
                                                    title=self.querier_entry_title.get(),
                                                    abstract=self.querier_entry_abs.get(),
                                                    keywords=self.querier_entry_key.get())
            querier = Querier(querier_args)
            querier.configure()
            try:
                querier.search(debug=True)
            except json.decoder.JSONDecodeError as jsonE:
                messagebox.showerror(title="Error en query de búsqueda avanzada",
                                     message=f"{this_time()} - Detalle:\n{jsonE.msg}")
                print( this_time(), "- No se ha podido interpretar la query de búsqueda avanzada\nDetalle:", jsonE.msg )
            # querier(debug: bool, query: str, content: str, from_year: str, title: str, arguments = None)
        else:
            print(f'{this_time()} - Campos de búsqueda vacíos\n')
            messagebox.showerror(title="Error", message="Campos de búsqueda vacíos")


def this_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")