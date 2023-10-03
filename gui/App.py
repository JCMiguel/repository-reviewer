import customtkinter as ctk

from .results_page import ResultsPage
from .history_page import HistoryPage
from .indexer_page import IndexerPage
from .log_frame import LogsFrame
from .querier_page import QuerierPage

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Repository Reviewer")
        self.geometry(f"{1100}x{680}")
        self.status = False

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Pages
        # NOTE: ver https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

        container = ctk.CTkFrame(self)
        # container.pack(expand=True)
        container.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (QuerierPage, IndexerPage, HistoryPage, ResultsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("QuerierPage")

        # Results and logs
        self.log_frame = LogsFrame(parent=container, controller=self)
        self.log_frame.grid(row=1, column=0, sticky="s", pady=(20, 0))

        # Sidebar
        # FIXME: Intente encapsularlo pero no me gusta como quedo. Hm....
        # El problema es que esto crea variables atributo que despues se usan en el propio init. No se como resolverlo
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.create_sidebar(self.sidebar_frame)

    def show_frame(self, page_name, contextual_data=None):
        '''Show a frame for the given page name'''
        if hasattr(self, 'last_frame'):
            self.last_frame.on_hiding()
        on_top_frame = self.frames[page_name]
        on_top_frame.tkraise()
        if contextual_data is not None:
            on_top_frame.set_contextual( contextual_data )
        on_top_frame.on_showing()
        self.last_frame = on_top_frame

    def create_sidebar(self, sidebar_frame: ctk.CTkFrame):
        # create sidebar frame with widgets
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.grid_rowconfigure(5, weight=1)
        logo_label = ctk.CTkLabel(sidebar_frame, text="Stages",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        sidebar_button_1 = ctk.CTkButton(sidebar_frame, text="Querier",
                                         command=self.sidebar_querier_button_event)
        sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        sidebar_button_2 = ctk.CTkButton(sidebar_frame, text="Quality check",
                                         command=self.sidebar_dummy_button_event)
        sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        sidebar_button_3 = ctk.CTkButton(sidebar_frame, text="Indexer",
                                         command=self.sidebar_indexer_button_event)
        sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        sidebar_button_4 = ctk.CTkButton(sidebar_frame, text="History",
                                         command=self.sidebar_history_button_event)
        sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        show_logs_checkbox = self.log_frame.Get_enabling_checkBox(sidebar_frame)
        show_logs_checkbox.grid(row=5, column=0, padx=20, pady=(15, 0))

        appearance_mode_label = ctk.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = ctk.CTkOptionMenu(sidebar_frame,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        scaling_label = ctk.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = ctk.CTkOptionMenu(sidebar_frame,
                                                values=["80%", "90%", "100%", "110%", "120%"],
                                                command=self.change_scaling_event)
        scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # set default values
        sidebar_button_2.configure(state="disabled")
        appearance_mode_optionemenu.set("System")
        scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_dummy_button_event(self):
        print("dummy function wip")
        pass

    def sidebar_querier_button_event(self):
        # FIXME: Esto es solo un botón de juguete para probar funcionalidades
        print("QUERIER BUTOOTN click")
        self.show_frame("QuerierPage")
        # if self.status == False:
        #    print(f'status is {self.status}')
        #    self.checkbox_slider_frame.destroy()
        #    self.slider_progressbar_frame._draw()
        #    self.status = True
        # else:
        #    print(f'status is {self.status}')
        #    self.slider_progressbar_frame.destroy()
        #    self.status = False

    def sidebar_indexer_button_event(self):
        # FIXME: Esto es solo un botón de juguete para probar funcionalidades
        print("INDEXER BUTOOTN click")
        self.show_frame("IndexerPage")

    def sidebar_history_button_event(self):
        # FIXME: Esto es solo un botón de juguete para probar funcionalidades
        print("HISTORY BUTOOTN click")
        self.show_frame("HistoryPage")
