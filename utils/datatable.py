from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''

<DataTable>:
    id: main_view
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None, 250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

<CustLabel@Label>
    bcolor: (1, 1, 1, .8)
    canvas.before:
        Color: 
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos

''')


class DataTable(BoxLayout):
    def __init__(self, table='', **kwargs):
        super().__init__(**kwargs)

        products = table

        product_titles = [key for key in products.keys()]
        total_products = len(products[product_titles[0]])
        self.columns = len(product_titles)

        table_data = []
        for title in product_titles:
            table_data.append({'text': str(title), 'size_hint_y': None, 'height': 50, 'bcolor': (.06, .45, .45, 1)})

        for prod in range(total_products):
            for title in product_titles:
                table_data.append({'text': str(products[title][prod]), 'size_hint_y': None, 'height': 30, 'bcolor': (.06, .25, .25, 1)})

        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data
    
    
# class DataTableApp(App):
#     def build(self):
#         return DataTable()


# if __name__=="__main__":
#     DataTableApp().run()