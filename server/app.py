import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from controler import allControllers
from db import gernalQuery

load_dotenv()



def create_app():
    app = Flask(__name__, template_folder="./templates")
    app.secret_key = os.getenv("SECRET_KEY")
    bcrypt = Bcrypt(app)
    app.extensions["bcrypt"] = bcrypt 
    #this function createTable will a genreal Query
    #and return nothing just run query
    gernalQuery("uuid_extension")
    gernalQuery("create_user_table")

    for bp in allControllers:
        app.register_blueprint(bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
