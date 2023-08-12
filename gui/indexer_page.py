import customtkinter as ctk


class IndexerPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        label = ctk.CTkLabel(self, text="This is Indexer Page")
        label.pack(side="top", fill="x", pady=10)
        button = ctk.CTkButton(self, text="Go to the start page",
                           command=self.dummy_action)
        button.pack()

    def dummy_action(self):
        print("dummy function wip")
        pass

