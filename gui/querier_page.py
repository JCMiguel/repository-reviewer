import customtkinter as ctk
from misc import execute
from datetime import datetime


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
            execute("python querier.py -h")
        else:
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - BUSCAAAARRR\n{texto}\n')
        #print("BUSCAARRR!!!!")

