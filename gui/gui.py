import subprocess
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
        for F in (QuerierPage, IndexerPage, HistoryPage):
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
        self.log_frame.grid(row=1, column=0, sticky="nsew", pady=(10,0))

        # Sidebar
        # FIXME: Intente encapsularlo pero no me gusta como quedo. Hm....
        # El problema es que esto crea variables atributo que despues se usan en el propio init. No se como resolverlo
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.create_sidebar(self.sidebar_frame)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

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
        #if self.status == False:
        #    print(f'status is {self.status}')
        #    self.checkbox_slider_frame.destroy()
        #    self.slider_progressbar_frame._draw()
        #    self.status = True
        #else:
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


class QuerierPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        # label = ctk.CTkLabel(self, text="This is the Querier Page")
        # label.pack(side="top", fill="x", pady=10)

        # button1 = ctk.CTkButton(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button2 = ctk.CTkButton(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()

        # Tab Querier
        self.querier_tab_title_lbl = ctk.CTkLabel(self, text="Title", anchor="w",
                                                  font=ctk.CTkFont(weight="bold"))
        self.querier_tab_title_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_title = ctk.CTkEntry(self, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_title.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_abs_lbl = ctk.CTkLabel(self, text="Abstract", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_abs_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_abs = ctk.CTkEntry(self, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_abs.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_key_lbl = ctk.CTkLabel(self, text="Keywords", anchor="w",
                                                font=ctk.CTkFont(weight="bold"))
        self.querier_tab_key_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_key = ctk.CTkEntry(self, placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_key.pack(side="top", padx=20, pady=5, fill="x")

        self.querier_tab_content_lbl = ctk.CTkLabel(self, text="Content", anchor="w",
                                                    font=ctk.CTkFont(weight="bold"))
        self.querier_tab_content_lbl.pack(side="top", anchor="w", padx=20, pady=0)
        self.querier_tab_entry_content = ctk.CTkEntry(self,
                                                      placeholder_text="Inserte texto aquí")
        self.querier_tab_entry_content.pack(side="top", padx=20,  pady=5, fill="x")
        # Entry boxes

        self.querier_tab_search_btn = ctk.CTkButton(self, text="Search!",
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
        if texto == 'Title() - Abs() - Key() - Content()':
            excecute("python querier.py -h")
        else:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - BUSCAAAARRR\n{texto}\n')
        #print("BUSCAARRR!!!!")


class IndexerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        label = ctk.CTkLabel(self, text="This is Indexer Page")
        label.pack(side="top", fill="x", pady=10)
        button = ctk.CTkButton(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class HistoryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        label = ctk.CTkLabel(self, text="This is History Page")
        label.pack(side="top", fill="x", pady=10)
        button = ctk.CTkButton(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class LogsFrame(ctk.CTkFrame):
    PADX = 20
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.logs_lbl = ctk.CTkLabel(self, text="Results and logs", anchor="w", font=ctk.CTkFont(weight="bold"))
        self.logs_lbl.pack(side="top", padx=LogsFrame.PADX, pady=(10,0))
        self.logs_box = ctk.CTkTextbox(self, width=2000, height=150, activate_scrollbars=True)
        self.logs_box.pack(side="top", padx=LogsFrame.PADX, pady=(10, 20))
        self.logs_box.configure(state="disabled")
        self.show_logs_checkbox = None
        self.stdout_redirector = StdoutRedirector(self.logs_box)

    def Get_enabling_checkBox(self, parent) -> ctk.CTkCheckBox:
        if (self.show_logs_checkbox is None):
            self.show_logs_checkbox = ctk.CTkCheckBox(parent, text="Show results and logs", command=self._checkbox_event)
        if bool(self.grid_info()): # This method led to know if the widget is visible now and so then syncronise the checkbox
            self.show_logs_checkbox.select()
        return self.show_logs_checkbox

    def _checkbox_event(self):
        value = self.show_logs_checkbox.get()
        # Redirect the standar output between default stdout and self.logs_box
        self.stdout_redirector.enable( value )
        # Handle visibility on the front
        self.grid() if value else self.grid_remove()
        print("_checkbox_event( view_enabled={} )".format(value))


import sys
from typing import TextIO
class StdoutRedirector(TextIO):
    def __init__(self,text_widget:ctk.CTkTextbox):
        self._text_space = text_widget
        #self._text_space.tag_config(tagName='ERROR', background="black", foreground="red")
        self._default_stdout = None
        self.enable()

    def write(self, string):
            # FIXME: Next line would be preffered to keep config after writing but get next incoherent exception
            #        ValueError: 'state' is not a supported argument. Look at the documentation for supported arguments.
            # prev_state = self._text_space.cget("state")
            self._text_space.configure(state="normal")
            #try:
            #    # FIXME: No aplica el tag. De todas formas este codigo no se lo deseo ni a mi peor enemigo, hay que mejorar esta abominacion
            #    start_idx = string.index(bcolors.FAIL)
            #    string = string.replace(bcolors.FAIL,"")
            #    end_idx = string.index(bcolors.ENDC)
            #    string = string.replace(bcolors.ENDC,"")
            #    self._text_space.insert('end', string)
            #    self._text_space.tag_add(tagName='ERROR', index1=int(start_idx), index2=int(end_idx))
            #except:
            #    pass
            self._text_space.insert('end', string)
            self._text_space.see('end')
            #self._text_space.configure(prev_state)
            self._text_space.configure(state="disabled")

    def enable(self, on:bool=True):
        if on:
            self._default_stdout = sys.stdout
            sys.stdout = self
        else:
            sys.stdout = self._default_stdout
        self._enabled = on

    def disable(self):
        self.enable(False)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def excecute(cmd) -> int:
    #proc = subprocess.Popen( "python querier.py -h".split(), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print( proc.stdout.read() )
    proc = subprocess.Popen( cmd.split(), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    out, err = proc.communicate()
    if len(out) > 0: print( out )
    if len(err) > 0: print( bcolors.FAIL + err + bcolors.ENDC ) # print in red
    return proc.returncode



if __name__ == "__main__":
    app = App()
    app.mainloop()