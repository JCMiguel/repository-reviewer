from .base_page import *
from tkinter import ttk
import pandas as pd

grouping_column_title = 'Found in'


def get_categories_dict(df:pd.DataFrame) -> {}:
    categories = df[grouping_column_title].astype('category')
    cat_counts = categories.value_counts()
    category_mapper = {}
    for idx, category in enumerate(categories.unique()):
        category_mapper[category] = {'id':   -(idx + 1),
                                     'count': cat_counts[category]}
    return category_mapper

def load_dataframe(filename:str) -> pd.DataFrame:
    df = pd.read_csv( filename, sep=',', index_col='ID')
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


    def on_init(self):
        pass

    def on_showing(self):
        self.show_results()

    def on_hiding(self):
        pass

    def on_resume(self):
        pass


    def show_results(self, df:pd.DataFrame=None):
        if (df is not None):
            ResultsPage.Load( df )
        if (ResultsPage.dFrame is None):
            ResultsPage.Load(filename="results/table_articles.csv")
        self.titles = self.process_titles()
        self.create_treeview()


    def process_titles(self) -> [str]:
        all_titles = ResultsPage.dFrame.columns.to_list()
        try:
            pop_idx = all_titles.index(grouping_column_title)
            all_titles.pop(pop_idx)
        except ValueError as ve:
            raise ValueError("ResultsPage.dFrame has no title {} to group articles"
                            .format(grouping_column_title))
        return all_titles # except grouping_column_title


    def create_treeview(self):
        # Scrollbar
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        # Treeview
        self.treeview = ttk.Treeview(
            self,
            selectmode="browse",
            yscrollcommand=scrollbar.set,
            columns=tuple([enum[0]+1 for enum in enumerate(self.titles)]),  # (1, 2),
            height=10,
        )
        self.treeview.pack(expand=True, fill="both")
        scrollbar.config(command=self.treeview.yview)
        self.config_treeview()
        self.load_treeview( ResultsPage.dFrame )


    def config_treeview(self):
        num_columns = len(self.titles)
        total_width = 1000
        main_width = int(total_width * 0.75)
        other_width = int((total_width-main_width)/num_columns)
        # Treeview columns config and headings set.
        self.treeview.column(0, stretch=True,  anchor="w", width=main_width)
        self.treeview.heading("#0", text=self.titles[0], anchor="center")

        for num_col in range(1, num_columns):
            self.treeview.column(num_col, stretch=False,  anchor="w", width=other_width)
            self.treeview.heading(num_col, text=self.titles[num_col], anchor="center")
        else:
            self.treeview.column(num_col+1, stretch=False,  anchor="w", width=other_width)
            self.treeview.heading(num_col+1, text="Additional info", anchor="center")


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
