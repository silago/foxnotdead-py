from flask import Flask
from flask_admin import Admin

from foxnotdead import items
from foxnotdead import users

import peewee
app = Flask(__name__)


import flask_admin as admin
from flask_admin.contrib.peewee import ModelView


# Add administrative views here



class UserAdmin(ModelView):
    inline_models = (items.UserItems,)




@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    admin = Admin(app, name='foxnotdead', template_mode='bootstrap3')

    admin.add_view(UserAdmin(users.User))
    #admin.add_view(PostAdmin(Post))

    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except:
        pass

app.run(debug=True)







