import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Repository Reviewer")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar
        # FIXME: Intente encapsularlo pero no me gusta como quedo. Hm....
        # El problema es que esto crea variables atributo que despues se usan en el propio init. No se como resolverlo
        self.create_sidebar()

        # Tabs
        self.create_tabs()

        # set default values
        self.sidebar_button_2.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def create_sidebar(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Stages",
                                                 font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Querier",
                                                        command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Quality check",
                                                        command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Indexer",
                                                        command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="History",
                                                        command=self.sidebar_button_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

    def create_tabs(self):
        # create tabview
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Querier")
        self.tabview.add("Home")
        self.tabview.add("Quality Check")
        self.tabview.add("Indexer")
        self.tabview.tab("Home").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Querier").grid_columnconfigure(0, weight=0)
        self.tabview.tab("Querier").grid_columnconfigure(1, weight=1)

        # Tab Home

        # Tab Querier
        # Labels
        self.querier_tab_title_lbl = ctk.CTkLabel(self.tabview.tab("Querier"), text="Title", anchor="w",
                                                  font=ctk.CTkFont(weight="bold"))
        self.querier_tab_title_lbl.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.querier_tab_abs_lbl = ctk.CTkLabel(self.tabview.tab("Querier"), text="Abstract", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_abs_lbl.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.querier_tab_key_lbl = ctk.CTkLabel(self.tabview.tab("Querier"), text="Keywords", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_key_lbl.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.querier_tab_content_lbl = ctk.CTkLabel(self.tabview.tab("Querier"), text="Content", anchor="w",
                                                    font=ctk.CTkFont(weight="bold"))
        self.querier_tab_content_lbl.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        # Entry boxes
        self.querier_tab_entry_title = ctk.CTkEntry(self.tabview.tab("Querier"), placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_title.grid(row=0, column=1, padx=20, columnspan=2, pady=10, sticky="nsew")
        self.querier_tab_entry_abs = ctk.CTkEntry(self.tabview.tab("Querier"), placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_abs.grid(row=1, column=1, padx=20, columnspan=2, pady=10, sticky="nsew")
        self.querier_tab_entry_key = ctk.CTkEntry(self.tabview.tab("Querier"), placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_key.grid(row=2, column=1, padx=20, columnspan=2, pady=10, sticky="nsew")
        self.querier_tab_entry_content = ctk.CTkEntry(self.tabview.tab("Querier"), placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_content.grid(row=3, column=1, padx=20, columnspan=2, pady=10, sticky="nsew")
        self.querier_tab_search_btn = ctk.CTkButton(self.tabview.tab("Querier"), text="Search!",
                                                    command=self.querier_tab_search_btn_event)
        self.querier_tab_search_btn.grid(row=4, column=1, padx=20, pady=10)
        # Results and logs
        self.querier_tab_logs_lbl = ctk.CTkLabel(self.tabview.tab("Querier"), text="Results and logs", anchor="center",
                                                 font=ctk.CTkFont(weight="bold"))
        self.querier_tab_logs_lbl.grid(row=6, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox = ctk.CTkTextbox(self.tabview.tab("Querier"), width=250)
        self.textbox.grid(row=6, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="disabled")

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        # FIXME: Esto es solo un botón de juguete para probar funcionalidades
        print("sidebar_button click")

    def querier_tab_search_btn_event(self):
        # TODO: Work In Progress
        self.textbox.configure(state="normal")
        texto = ""
        texto += f'Title({self.querier_tab_entry_title.get()}) - '
        texto += f'Abs({self.querier_tab_entry_abs.get()}) - '
        texto += f'Key({self.querier_tab_entry_key.get()}) - '
        texto += f'Content({self.querier_tab_entry_content.get()})'
        self.textbox.insert("end", f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - BUSCAAAARRR\n{texto}\n')
        self.textbox.configure(state="disabled")
        print("BUSCAARRR!!!!")


if __name__ == "__main__":
    app = App()
    app.mainloop()