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
        self.querier_content_lbl = ctk.CTkLabel(second_tab, text="Query", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_content_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_content_lbl = ctk.CTkTextbox(second_tab,
                                                  height=226, activate_scrollbars=True,
                                                  border_color="dark grey", border_width=2)
        self.querier_content_lbl.pack(side="top", padx=20, pady=5, fill="both")

        # Common (out of tabs)
        self.querier_search_btn = ctk.CTkButton(self, text="Search!",
                                                command=self.search_btn_event)
        self.querier_search_btn.pack(side="top", padx=20, pady=10)

    def search_btn_event(self):
        texto = ""
        texto += f'Title({self.querier_entry_title.get()}) - '
        texto += f'Abs({self.querier_entry_abs.get()}) - '
        texto += f'Key({self.querier_entry_key.get()}) - '
        texto += f'Content({self.querier_entry_content.get()})'
        if texto != 'Title() - Abs() - Key() - Content()':
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Buscando...\n')
            # TODO: FIXME: al invocar esta función, la pantalla se queda congelada hasta finalizar la búsqueda
            querier_args = build_querier_dictionary(query="",
                                                    content=self.querier_entry_content.get(),
                                                    title=self.querier_entry_title.get(),
                                                    abstract=self.querier_entry_abs.get(),
                                                    keywords=self.querier_entry_key.get())
            querier = Querier(querier_args)
            querier.configure()
            querier.search(debug=True)
        else:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Campos de búsqueda vacíos\n')

