from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder


import re
from pymongo import MongoClient

Builder.load_file('till_operator/till_operator.kv')

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient("mongodb+srv://Inam:inam123@devconnector.acy6n.mongodb.net/dev_connector?retryWrites=true&w=majority") 
        self.db = client['POS']
        self.stocks = self.db['stocks_table']


        self.cart = []
        self.qty = []
        self.total = 0.00
    
    def logout(self):
        self.parent.parent.current = 'scrn_si'
    
    def update_purchases(self):
        prod_code = self.ids.code_inp.text
        products_container = self.ids.products
        target_code = self.stocks.find_one({'product_code': prod_code})
        if target_code == None:
            pass
        else: 
            """
                Creating Dynamic widget according to product code
            """
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            products_container.add_widget(details)

            # CREATING DYNAMIC LABELS
            code = Label(text=prod_code, size_hint_x=.2, color=(.06, .45, .45, 1))
            name = Label(text=target_code['product_name'], size_hint_x=.3, color=(.06, .45, .45, 1))
            qty = Label(text='1', size_hint_x=.1, color=(.06, .45, .45, 1))
            disc = Label(text='0.00', size_hint_x=.1, color=(.06, .45, .45, 1))
            price = Label(text=str(target_code['product_price']), size_hint_x=.1, color=(.06, .45, .45, 1))
            total = Label(text='0.00', size_hint_x=.2, color=(.06, .45, .45, 1))

            # ADDING LABELS TO THE CONTAINER WIDGET
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(disc)
            details.add_widget(price)
            details.add_widget(total)

            # UPDATE PREVIEW PANEL
            prod_name = name
            prod_price = float(price.text)
            prod_qty = str(1)
            self.total += prod_price
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t'+str(self.total)
            self.ids.current_prod.text = str(prod_name.text)
            self.ids.current_price.text = str(prod_price)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]


            prod_target = -1
            for i,c in enumerate(self.cart):
                if c == prod_code:
                    prod_target = i
                    print(prod_target)
            
            if prod_target >= 0:
                prod_qty = self.qty[prod_target]+1
                self.qty[prod_target] = prod_qty
                expr = '%s\t\tx\d\t'%(prod_name.text)
                rexpr = prod_name.text+'\t\tx'+str(prod_qty)+'\t'
                new_text = re.sub(expr, rexpr, prev_text)
                preview.text = new_text + purchase_total
            else:
                self.cart.append(prod_code)
                self.qty.append(1)
                new_preview = '\n'.join([prev_text, prod_name.text+'\t\tx'+prod_qty+'\t\t'+str(prod_price), purchase_total])
                preview.text = new_preview

            self.ids.disc_inp.text = '0.00'
            self.ids.disc_perc_inp.text = '0.00'
            self.ids.vat_inp.text = '15%'
            self.ids.price_inp.text = str(prod_price)
            self.ids.total_inp.text = str(purchase_total)
            self.ids.qty_inp.text = str(prod_qty)
            

    
class OperatorApp(App):
    def build(self):
        return OperatorWindow()


if __name__=="__main__":
    oa = OperatorApp()
    oa.run()