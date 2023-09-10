from .base_page import *


class HistoryPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)

        label = ctk.CTkLabel(self, text="This is History Page")
        label.pack(side="top", fill="x", pady=10)
        button = ctk.CTkButton(self, text="Go to the start page",
                           command=self.dummy_action)
        button.pack()
        button_results = ctk.CTkButton(self, text="Get last results",
                                       command=self.show_results_page)
        button_results.pack()


    def on_init(self):
        pass

    def on_showing(self):
        pass

    def on_hiding(self):
        pass

    def on_resume(self):
        pass


    def dummy_action(self):
        print("dummy function wip")
        pass

    def show_results_page(self):
        self.controller.show_frame('ResultsPage')