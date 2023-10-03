import pandas as pd
from tkinter import ttk
from .base_page import *
from historic.history import History, DataSearch
from datetime import datetime as dt

class HistoryPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)
        self.configure_fields()
        self.titles = []
    # 230915001,23092323

    def show_results_page(self, event):
        item = self.treeview.identify('item', event.x, event.y)
        print("you clicked on", item)
        results_fn = DataSearch.format_filename( str(item) )
        print("file: ", results_fn)
        self.controller.show_frame('ResultsPage', results_fn )


    def show_history_report(self, arg):
        print( arg )
        self.titles = self.process_titles( arg )
        print("ARG: ", arg )
        self.create_treeview( arg )


    def configure_fields(self):
        pad_x_L = 150
        pad_x_R = 0
        # Title
        lbl_title = ctk.CTkLabel(self, text="Registro Histórico",
                                             anchor="w", font=ctk.CTkFont(weight="bold"))
        lbl_title.grid(row=0, columnspan=2, padx=(100, 0), pady=20, sticky="ew")
        lbl_title.configure(anchor="center")
        lbl_subtitle = ctk.CTkLabel(self, text="Recuperación de búsquedas previas",
                                             anchor="w", font=ctk.CTkFont(weight="normal"))
        lbl_subtitle.grid(row=1, column=0, padx=(pad_x_L, pad_x_R), pady=(10, 0), sticky="w")
        # Entry
        self.entry_title = ctk.CTkEntry(self, placeholder_text="Inserte texto aquí",
                                                width=300)
        self.entry_title.grid(row=3, column=0, padx=(pad_x_L, pad_x_R), pady=(10, 0), sticky="w")
        self.entry_title.insert(0,"230915001,23092323") # HACK: puesto para probar rapidamente
        # Radio Buttons
        self.option = self.configure_radiobuttons(start_row=1, start_col=1, pad_x_left=100)
        # Search Button
        button_results = ctk.CTkButton(self, text="Recuperar", command=self.retrive_action)
        button_results.grid(row=5, column=0, padx=(pad_x_L, pad_x_R), pady=(10, 0), sticky="w")
        # Treeview
        self.scrollbar = None
        self.treeview = None


    def configure_radiobuttons(self, start_row, start_col, pad_x_left):
        method_description_options = [
            ("Get_by_matching", "Coincidencia textual"),
            ("Get_previous",    "Búsquedas anteriores"),
            ("Get_by_id",       "Indentificación temporal"),
            ("Get_by_index",    "Índice desde el inicio"),
            ("Get_by_date",     "Rango de fechas")
        ]
        # Default option init pointing to the first method name
        string_var = ctk.StringVar(self, method_description_options[4][0]) # HACK: puesto para probar rapidamente. Volver al [0]
        rbtns = []
        for idx, value_text_ops in enumerate(method_description_options):
            method_name, desc = value_text_ops
            rbtns.append(ctk.CTkRadioButton(self, variable=string_var,
                                            value=method_name, text=desc))
            rbtns[idx].grid(row=start_row + idx, column=start_col,
                            padx=(pad_x_left, 10), pady=(10, 0), sticky="w")
        return string_var


    def process_titles(self, df:pd.DataFrame) -> [str]:
        skipped_titles = ["Search Params"]
        all_titles = [df.index.name] + df.columns.to_list()
        try:
            for title in skipped_titles:
                pop_idx = all_titles.index(title)
                all_titles.pop(pop_idx)
        except ValueError as ve:
            print("List 'all_titles':", all_titles)
            raise ValueError("Target dataFrame has no title {} to group articles"
                            .format(skipped_titles))
        return all_titles # except skipped_titles


    def create_treeview(self, df:pd.DataFrame):
        # Scrollbar
        #if self.scrollbar is None:
        #    self.scrollbar = ttk.Scrollbar(self)
        #    self.scrollbar.grid(sticky="e")
        # Treeview
        n_cols = tuple([enum[0]+1 for enum in enumerate(self.titles)])
        print("N_COLS ", n_cols)
        self.treeview = ttk.Treeview(
            self,
            selectmode="browse",
            #yscrollcommand=self.scrollbar.set,
            columns= (1, 2, 3, 4, 5, 6, 7, 8, 9),
            height=10
        )
        #self.treeview.pack(expand=True, fill="both")
        self.treeview.grid(row=6, columnspan=2, padx=20, pady=10, sticky="ew")
        #self.scrollbar.config(command=self.treeview.yview)
        self.config_treeview()
        self.load_treeview( df )


    def config_treeview(self):
        """ Treeview columns config and headings set """
        num_columns = len(self.titles)
        total_width = 620
        main_width = int(total_width * 0.05)
        other_width = int((total_width-main_width)/num_columns-1)
        # First column with particular its particular main configuration
        #self.treeview.column(0, anchor="w", stretch=ctk.NO, minwidth=main_width, width=main_width)
        #self.treeview.heading(0, text=self.titles[0])#, anchor="center")
        self.treeview.column(0, anchor=ctk.CENTER, stretch=ctk.NO, width=100)
        self.treeview.heading(0, text=self.titles[0])
        # Next columns with their data
        print("Config tree: ", end='')
        for num_col in range(1, num_columns):
            print( num_col, end=' ')
            self.treeview.column(num_col, anchor=ctk.CENTER, stretch=ctk.NO, width=70)
            #self.treeview.column(num_col, anchor="w", stretch=ctk.NO, minwidth=other_width, width=other_width)
            self.treeview.heading(num_col, text=self.titles[num_col])
        # Event bindings
        self.treeview.bind("<Double-1>", self.show_results_page)

    def load_treeview(self, df:pd.DataFrame):
        # Load articles relating them with their parent repo
        print("loading treeview con...\n", df)
        for idx in df.index:
            article_value_list = df.loc[idx].to_list()
            date = dt.strptime(str(idx), "%y%m%d%H%M%S")
            print( date, article_value_list)
            #found_in_repo = article_value_list[1]
            self.treeview.insert(parent="", index="end", iid=idx,
                                 text=dt.strftime(date, "%Y-%m-%d  %H:%M:%S"),
                                 values=article_value_list)

    def retrive_action(self):
        print("Se presionó el botón de recuperación de registros y el valor es...", self.option.get(), self.entry_title.get())
        method_name = self.option.get()
        history_method = getattr(History, method_name)
        value_search = self.entry_title.get().strip()
        try:
            retrived_data = history_method( value_search )
        except TypeError as type_e:
            print(type_e)
            retrived_data = history_method( int(value_search) )
        self.show_history_report( retrived_data )


    def on_init(self):
        pass

    def on_showing(self):
        pass

    def on_hiding(self):
        print("Byeee desde history_page")
        pass

    def on_resume(self):
        pass
    
    def set_contextual(self, data):
        pass

