from .base_page import *
from .misc import execute
from datetime import datetime
from engine.querier import querier


class QuerierPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)


    def on_init(self):
        pass

    def on_showing(self):
        pass

    def on_hiding(self):
        pass

    def on_resume(self):
        pass


        # create tabview
        # TODO: Este flag es solo para que el código se adapte más fácil durante pruebas. A futuro hay que sacarlo...
        __use_tabs_debug = False
        view = None
        second_tab = view
        if __use_tabs_debug:
            print(parent.cget("width"))
            self.tabview = ctk.CTkTabview(self, width=parent.cget("width"))
            self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="ew")
            self.tabview.add("Búsqueda básica")
            self.tabview.add("Búsqueda avanzada")
            self.tabview.tab("Búsqueda básica").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
            self.tabview.tab("Búsqueda avanzada").grid_columnconfigure(0, weight=1)
            view = self.tabview.tab("Búsqueda básica")
            second_tab = self.tabview.tab("Búsqueda avanzada")
        else:
            view = self

        # Tab - Búsqueda básica
        self.querier_tab_title_lbl = ctk.CTkLabel(view, text="Title", anchor="w",
                                                  font=ctk.CTkFont(weight="bold"))
        self.querier_tab_title_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_title = ctk.CTkEntry(view, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_title.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_abs_lbl = ctk.CTkLabel(view, text="Abstract", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_abs_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_abs = ctk.CTkEntry(view, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_abs.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_key_lbl = ctk.CTkLabel(view, text="Keywords", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_key_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_key = ctk.CTkEntry(view, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_key.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_content_lbl = ctk.CTkLabel(view, text="Content", anchor="w",
                                                    font=ctk.CTkFont(weight="bold"))
        self.querier_tab_content_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_content = ctk.CTkEntry(view,
                                                      placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_content.pack(side="top", padx=20,  pady=5, fill="x")

        self.querier_tab_search_btn = ctk.CTkButton(view, text="Search!",
                                                    command=self.querier_tab_search_btn_event)
        self.querier_tab_search_btn.pack(side="top", padx=20, pady=5)

        if __use_tabs_debug:
            self.querier_tab_content_lbl = ctk.CTkLabel(second_tab, text="Query", anchor="w",
                                                        font=ctk.CTkFont(weight="bold"))
            self.querier_tab_content_lbl.pack(side="top", anchor="w", padx=20, pady=0)
            self.querier_tab_entry_content = ctk.CTkEntry(second_tab,
                                                          placeholder_text="Inserte texto aquí")
            self.querier_tab_entry_content.pack(side="top", padx=20, pady=5, fill="both")

            self.querier_tab_search_btn = ctk.CTkButton(second_tab, text="Search!",
                                                        command=self.querier_tab_search_btn_event)
            self.querier_tab_search_btn.pack(side="top", padx=20, pady=5)



    def querier_tab_search_btn_event(self):
        # TODO: Work In Progress
        texto = ""
        texto += f'Title({self.querier_tab_entry_title.get()}) - '
        texto += f'Abs({self.querier_tab_entry_abs.get()}) - '
        texto += f'Key({self.querier_tab_entry_key.get()}) - '
        texto += f'Content({self.querier_tab_entry_content.get()})'
        # HACK: If search is empty then show help. Just a demo of subproces run
        if texto != 'Title() - Abs() - Key() - Content()':
            # execute("python querier.py -h")
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Buscando...\n')
            # TODO: FIXME: al invocar esta función, la pantalla se queda congelada hasta finalizar la búsqueda
            querier(debug=True,
                    query="",
                    content=self.querier_tab_entry_content.get(),
                    title=self.querier_tab_entry_title.get(),
                    abstract=self.querier_tab_entry_abs.get(),
                    keywords=self.querier_tab_entry_key.get())
            # querier(debug: bool, query: str, content: str, from_year: str, title: str, arguments = None)
        else:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Campos de búsqueda vacíos\n')

