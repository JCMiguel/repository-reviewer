from .base_page import *

# [HACK]: BORRAR ESTA CLASE QUE ESTÁ SOLO PARA PROBAR, LUEGO INTEGRAR CON HISTORY
class History: 
    def Get_by_matching(value):
        print(f"Get_by_matching({value}):")
    def Get_by_id(value):
        print(f"Get_by_id({value}):")
    def Get_by_filter(value):
        print(f"Get_by_filter({value}):")
    def Get_by_index(value):
        print(f"Get_by_index({value}):")
    def Get_previous(value):
        print(f"Get_previous({value}):")


class HistoryPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)
        self.configure_fields()


    def configure_fields(self):
        pad_x = 125
        # Title
        lbl_title = ctk.CTkLabel(self, text="Recuperación de búsquedas históricas",
                                             anchor="w", font=ctk.CTkFont(weight="bold"))
        lbl_title.grid(row=0, column=0, padx=pad_x, pady=(10, 0), sticky="w")
        # Entry
        self.entry_title = ctk.CTkEntry(self, placeholder_text="Inserte texto aquí",
                                                width=300)
        self.entry_title.grid(row=1, column=0, padx=pad_x, pady=(10, 0), sticky="w")
        # Radio Buttons
        self.option = self.configure_radiobuttons(0, 1, 50)
        # Search Button
        button_results = ctk.CTkButton(self, text="Recuperar", command=self.retrive_action)
        button_results.grid(row=3, column=0, padx=pad_x, pady=(10, 0), sticky="w")


    def retrive_action(self):
        print("Se presionó el botón de recuperación de registros y el valor es...", self.option.get(), self.entry_title.get())
        method = getattr(History, self.option.get())
        retrived_data = method( self.entry_title.get() )
        self.show_results_page( retrived_data )


    def configure_radiobuttons(self, start_row, start_col, pad_x):
        strvar = ctk.StringVar(self, "History.Get_by_matching")
        rbtns = []
        rbtns.append(ctk.CTkRadioButton(self, variable=strvar, value="Get_by_matching", text="Coincidencia textual"))
        rbtns.append(ctk.CTkRadioButton(self, variable=strvar, value="Get_previous", text="Búsquedas anteriores"))
        rbtns.append(ctk.CTkRadioButton(self, variable=strvar, value="Get_by_id", text="Indentificación temporal"))
        rbtns.append(ctk.CTkRadioButton(self, variable=strvar, value="Get_by_index", text="Índice desde el inicio"))
        rbtns.append(ctk.CTkRadioButton(self, variable=strvar, value="Get_by_filter", text="Rango de fechas"))
        for i, radiobutton in enumerate(rbtns):
            radiobutton.grid(row=start_row + i, column=start_col, padx=pad_x, pady=(10, 0), sticky="w")
        return strvar


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

    def show_results_page(self, arg):
        self.controller.show_frame('ResultsPage', arg)