from .base_page import *
import pandas as pd

class IndexerPage(BasePageFrame):

    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)
        label = ctk.CTkLabel(self, text="This is Indexer Page")
        label.pack(side="top", fill="x", pady=10)
        button = ctk.CTkButton(self, text="Go to the start page",
                           command=self.dummy_action)
        button.pack()
        self.preview_article = None

    def dummy_action(self):
        print("dummy function wip")
        pass


    def on_init(self):
        pass

    def on_showing(self):
        if self.preview_article is not None:
            print(self.preview_article)

    def on_hiding(self):
        pass

    def on_resume(self):
        pass

    def set_contextual(self, data):
        if isinstance(data, pd.Series):
            self.preview_article = data
