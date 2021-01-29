from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.lang import Builder

from datetime import datetime
from pymongo import MongoClient
from utils.datatable import DataTable
import hashlib

Builder.load_file('admin/admin.kv')


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        client = MongoClient("mongodb+srv://Inam:inam123@devconnector.acy6n.mongodb.net/dev_connector?retryWrites=true&w=majority") 

        db = client['POS']
        self.users = db['users_table']
        self.stocks = db['stocks_table']

        # Init values for product analysis
        product_code = []
        product_name = []
        spinvals = []
        for product in self.stocks.find():
            # print(user)
            product_code.append(product['product_code'])
            prd_name = product.get('product_name')
            if prd_name != None:
                if len(prd_name) > 30:
                    prd_name = prd_name[:30] + '...'
                product_name.append(prd_name)
        
        for x in range(len(product_name)):
            line = ' | '.join([product_code[x], product_name[x]])
            spinvals.append(line)
        
        self.ids.target_product.values = spinvals
    
        #Display Users
        user_content = self.ids.users_scrn
        users = self.get_users()
        datatable = DataTable(table=users)
        user_content.add_widget(datatable)

        #Display Products
        prod_content = self.ids.products_scrn
        products = self.get_products()
        datatable = DataTable(table=products)
        prod_content.add_widget(datatable)
    
    def logout(self):
        self.parent.parent.current = 'scrn_si'
    

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_firstName = TextInput(hint_text='First Name', multiline=False)
        crud_lastName = TextInput(hint_text='Last Name', multiline=False)
        crud_userName = TextInput(hint_text='User Name', multiline=False)
        crud_password = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Operator', values=['Operator', 'Administrator'])
        crud_submit = Button(text='Add', size_hint_x=None, width=100, on_release=lambda x: self.add_user(crud_firstName.text, crud_lastName.text, crud_userName.text, crud_password.text, crud_des.text))

        target.add_widget(crud_firstName)
        target.add_widget(crud_lastName)
        target.add_widget(crud_userName)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
    
    def add_user(self, first, last, user, pwd, des):
        user_content = self.ids.users_scrn
        user_content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.insert_one(
            {
                'first_name': first,
                'last_name': last,
                'user_name': user,
                'password': pwd,
                'designation': des,
                'date': datetime.now()
            }
        )
        users = self.get_users()
        datatable = DataTable(table=users)
        user_content.add_widget(datatable)

    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_firstName = TextInput(hint_text='First Name', multiline=False)
        crud_lastName = TextInput(hint_text='Last Name', multiline=False)
        crud_userName = TextInput(hint_text='User Name', multiline=False)
        crud_password = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Operator', values=['Operator', 'Administrator'])
        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x: self.update_user(crud_firstName.text, crud_lastName.text, crud_userName.text, crud_password.text, crud_des.text))
    

        target.add_widget(crud_firstName)
        target.add_widget(crud_lastName)
        target.add_widget(crud_userName)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
    
    def update_user(self, first, last, user, pwd, des):
        user_content = self.ids.users_scrn
        user_content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        self.users.update_one(
            {
                'user_name': user
            },
            {
                '$set': {
                    'first_name': first,
                    'last_name': last,
                    'user_name': user,
                    'password': pwd,
                    'designation': des,
                    'date': datetime.now()
                }
            }
        )
        users = self.get_users()
        datatable = DataTable(table=users)
        user_content.add_widget(datatable)

    
    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_userName = TextInput(hint_text='User Name', multiline=False)
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x: self.remove_user(crud_userName.text))

        target.add_widget(crud_userName)
        target.add_widget(crud_submit)

    def remove_user(self, user):
        user_content = self.ids.users_scrn
        user_content.clear_widgets()
        
        self.users.delete_one({'user_name': user})

        users = self.get_users()
        datatable = DataTable(table=users)
        user_content.add_widget(datatable)

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code', multiline=False)
        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_weight = TextInput(hint_text='Product Weight', multiline=False)
        crud_stock = TextInput(hint_text='Product Stock', multiline=False)
        crud_order = TextInput(hint_text='Product Order', multiline=False)
        crud_sold = TextInput(hint_text='Product Sold', multiline=False)
        crud_purchase = TextInput(hint_text='Product Purhcase', multiline=False)
        crud_submit = Button(text='Add', size_hint_x=None, width=100, on_release=lambda x: self.add_product(crud_code.text, crud_name.text, crud_weight.text, crud_stock.text, crud_order.text, crud_sold.text, crud_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_order)
        target.add_widget(crud_sold)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)
    
    def add_product(self, code, name, weight, stock, order, sold, purchase):
        content = self.ids.products_scrn
        content.clear_widgets()
        self.stocks.insert_one(
            {
                'product_code': code,
                'product_name': name,
                'product_weight': weight,
                'in_stock': stock,
                'sold': sold,
                'order': order,
                'last_purchase': purchase
            }
        )

        prods = self.get_products()
        stocktable = DataTable(table=prods)
        content.add_widget(stocktable)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code', multiline=False)
        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_weight = TextInput(hint_text='Product Weight', multiline=False)
        crud_stock = TextInput(hint_text='Product Stock', multiline=False)
        crud_order = TextInput(hint_text='Product Order', multiline=False)
        crud_sold = TextInput(hint_text='Product Sold', multiline=False)
        crud_purchase = TextInput(hint_text='Product Purhcase', multiline=False)
        crud_submit = Button(text='Update', size_hint_x=None, width=100, on_release=lambda x: self.update_product(crud_code.text, crud_name.text, crud_weight.text, crud_stock.text, crud_order.text, crud_sold.text, crud_purchase.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_order)
        target.add_widget(crud_sold)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def update_product(self, code, name, weight, stock, order, sold, purchase):
        user_content = self.ids.products_scrn
        user_content.clear_widgets()
        self.stocks.update_one(
            {
                'product_code': code
            },
            {
                '$set': {
                    'product_code': code,
                    'product_name': name,
                    'product_weight': weight,
                    'in_stock': stock,
                    'sold': sold,
                    'order': order,
                    'last_purchase': purchase
                }
            }
        )
        prods = self.get_products()
        datatable = DataTable(table=prods)
        user_content.add_widget(datatable)

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code', multiline=False)
        crud_submit = Button(text='Remove', size_hint_x=None, width=100, on_release=lambda x: self.remove_product(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_product(self, code):
        user_content = self.ids.products_scrn
        user_content.clear_widgets()
        print(code)
        
        self.stocks.delete_one({'product_code': code})

        prods = self.get_products()
        datatable = DataTable(table=prods)
        user_content.add_widget(datatable)


    def get_users(self): 
        client = MongoClient("mongodb+srv://Inam:inam123@devconnector.acy6n.mongodb.net/dev_connector?retryWrites=true&w=majority") 

        db = client['POS']
        users = db.users_table
        _users = {
            'first_names': {},
            'last_names': {},
            'user_names': {},
            'passwords': {},
            'designations': {},
        }

        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []

        for user in users.find():
            # print(user)
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 10: 
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user['designation'])
        
        users_length = len(first_names)
        index = 0

        while index < users_length:
            _users['first_names'][index] = first_names[index]
            _users['last_names'][index] = last_names[index]
            _users['user_names'][index] = user_names[index]
            _users['designations'][index] = designations[index]
            _users['passwords'][index] = passwords[index]

            index += 1

        return _users
    
    def get_products(self): 
        client = MongoClient("mongodb+srv://Inam:inam123@devconnector.acy6n.mongodb.net/dev_connector?retryWrites=true&w=majority") 

        db = client['POS']
        stocks = db.stocks_table
        _stocks = {
            'product_code': {},
            'product_name': {},
            'product_weight': {},
            'in_stock': {},
            'sold': {},
            'order': {},
            'last_purchase': {},
        }

        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []

        for product in stocks.find():
            # print(user)
            product_code.append(product['product_code'])
            prd_name = product.get('product_name')
            if prd_name != None:
                if len(prd_name) > 10:
                    prd_name = prd_name[:10] + '...'
            product_name.append(prd_name)
            product_weight.append(product['product_weight'])
            in_stock.append(product['in_stock'])
            try:
                sold.append(product['sold'])
            except KeyError:
                sold.append('')
            try:
                order.append(product['order'])
            except KeyError:
                order.append('')
            last_purchase.append(product['last_purchase'])
        
        stocks_length = len(product_code)
        index = 0

        while index < stocks_length:
            _stocks['product_code'][index] = product_code[index]
            _stocks['product_name'][index] = product_name[index]
            _stocks['product_weight'][index] = product_weight[index]
            _stocks['in_stock'][index] = in_stock[index]
            _stocks['sold'][index] = sold[index]
            _stocks['order'][index] = order[index]
            _stocks['last_purchase'][index] = last_purchase[index]

            index += 1

        return _stocks

    def view_stats(self):
        target_product = self.ids.target_product.text
        target = target_product[:target_product.find(' | ')]
        name = target_product[target_product.find(' | '):]

    def change_screen(self, instance):
        if instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'user_scrn'
        elif instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'product_scrn'
        elif instance.text == 'Product Analysis':
            self.ids.scrn_mngr.current = 'analysis_scrn'
    
class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__=="__main__":
    AdminApp().run()