from repos.abc_def import RESULT_SEPARATOR
from .base_page import *
from tkinter import ttk
import pandas as pd

grouping_column_title = 'Repositorio'


def get_categories_dict(df:pd.DataFrame) -> {}:
    categories = df[grouping_column_title].astype('category')
    cat_counts = categories.value_counts()
    category_mapper = {}
    for idx, category in enumerate(categories.unique()):
        category_mapper[category] = {'id':   -(idx + 1),
                                     'count': cat_counts[category]}
    return category_mapper

def load_dataframe(filename:str) -> pd.DataFrame:
    df = pd.read_csv( filename, sep=RESULT_SEPARATOR, index_col='ID')
    df = df.fillna('')
    return df


class ResultsPage(BasePageFrame):

    dFrame = None

    def Load(df:pd.DataFrame=None, filename:str=""):
        if (df is None) or isinstance(df,pd.DataFrame) == False:
            df = load_dataframe( filename )
        ResultsPage.dFrame = df


    def __init__(self, parent, controller):
        BasePageFrame.__init__(self, parent, controller)
        self.scrollbar = None

    def on_init(self):
        pass

    def on_showing(self):
        self.show_results()

    def on_hiding(self):
        print("ResultsPage.on_hiding() --> self.treeview = None")
        self.treeview.forget()

    def on_resume(self):
        pass
    
    def set_contextual(self, data):
        if isinstance(data, pd.DataFrame):
            ResultsPage.Load( data )
        elif isinstance(data, str):
            ResultsPage.Load( filename=data )


    def show_results(self):
        self.titles = self.process_titles()
        self.create_treeview()


    def process_titles(self) -> [str]:
        all_titles = ResultsPage.dFrame.columns.to_list()
        try:
            pop_idx = all_titles.index(grouping_column_title)
            all_titles.pop(pop_idx)
        except ValueError as ve:
            print("List 'all_titles':", all_titles)
            raise ValueError("ResultsPage.dFrame has no title {} to group articles"
                            .format(grouping_column_title))
        return all_titles # except grouping_column_title


    def create_treeview(self):
        # Scrollbar
        if self.scrollbar is None:
            self.scrollbar = ttk.Scrollbar(self)
            self.scrollbar.pack(side="right", fill="y")
        # Treeview
        self.treeview = ttk.Treeview(
            self,
            selectmode="browse",
            yscrollcommand=self.scrollbar.set,
            columns=tuple([enum[0]+1 for enum in enumerate(self.titles)]),  # (1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.treeview.yview)
        self.config_treeview()
        self.load_treeview( ResultsPage.dFrame )


    def config_treeview(self):
        """ Treeview columns config and headings set """
        num_columns = len(self.titles)
        total_width = 1000
        main_width = int(total_width * 0.75)
        other_width = int((total_width-main_width)/num_columns)
        # First column with particular its particular main configuration
        self.treeview.column(0, stretch=True,  anchor="w", width=main_width)
        self.treeview.heading("#0", text=self.titles[0], anchor="center")
        # Next columns with their data
        for num_col in range(1, num_columns):
            self.treeview.column(num_col, stretch=False,  anchor="w", width=other_width)
            self.treeview.heading(num_col, text=self.titles[num_col], anchor="center")
        else:
            # And additional column for showing extra information
            self.treeview.column(num_col+1, stretch=False,  anchor="w", width=other_width)
            self.treeview.heading(num_col+1, text="Additional info", anchor="center")
        # Event bindings
        self.treeview.bind("<Double-1>", self.on_double_click)


    def load_treeview(self, df:pd.DataFrame):
        identifier_ = get_categories_dict(df)
        # Load repositories groups as containers/parents
        for parent in identifier_:
            extra_data = ['-'] * (len(self.titles) - 1) \
                       + ["Results: {}".format(identifier_[parent].get('count'))]
            self.treeview.insert("", "end",
                                 iid=identifier_[parent].get('id'),
                                 text=parent, values=extra_data)
        # Load articles relating them with their parent repo
        for idx in df.index:
            article_value_list = df.loc[idx].to_list()
            found_in_repo = article_value_list[1]
            self.treeview.insert(parent=identifier_[found_in_repo].get('id'),
                                 index="end",
                                 iid=idx,
                                 text=article_value_list[0],  # Title
                                 values=article_value_list[2:])
        # else: self.treeview.see( idx )


    def on_double_click(self, event):
        item_id = self.treeview.selection()[0]
        article = ResultsPage.dFrame.loc[ int(item_id) ]
        print("you clicked on", str(item_id))
        self.controller.show_frame('IndexerPage', article)
