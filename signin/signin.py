from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from pymongo import MongoClient
import hashlib

Builder.load_file('signin/signin.kv')


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient("mongodb+srv://Inam:inam123@devconnector.acy6n.mongodb.net/dev_connector?retryWrites=true&w=majority") 
        db = client['POS']
        self.users = db['users_table']
    
    def validate_user(self):
        username = self.ids.username_field.text
        password = self.ids.pwd_field.text
        info = self.ids.info

        if username == '' or password == '':
            info.text = "[color=#FF0000]Username or Password is empty[/color]"
        else:
            user = self.users.find_one({'user_name': username})
            if user == None:
                info.text = "[color=#FF0000]Username or Password is incorrect[/color]"
            else:
                password =  hashlib.sha256(password.encode()).hexdigest()
                if username == user['user_name'] and password == user['password']:
                    # info.text = "[color=#00FF00]Succesfully logged in!!![/color]"
                    self.parent.parent.parent\
                        .ids.scrn_op.children[0]\
                            .ids.loggedin_user.text = username
                    if user['designation'] == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    info.text = "[color=#FF0000]Username or Password is incorrect[/color]"

class SigninApp(App):
    def build(self):
        return SigninWindow()


if __name__=="__main__":
    sa = SigninApp()
    sa.run()