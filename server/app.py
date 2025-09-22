import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from controler import allControllers
from db import gernalQuery

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="./templates")
    app.secret_key = os.getenv("SECRET_KEY")
    bcrypt = Bcrypt(app)
    app.extensions["bcrypt"] = bcrypt
    # this function createTable will a genreal Query
    # and return nothing just run query
    # below is extension activation
    gernalQuery("uuid_extension")
    gernalQuery("vector_extension")
    gernalQuery("create_vector_index")
    # creating Types
    gernalQuery("create_type_role")
    # below is table creation
    gernalQuery("create_user_table")
    gernalQuery("create_chat_table")
    gernalQuery("create_quiz_table")

    for bp in allControllers:
        app.register_blueprint(bp)

    @app.route("/")
    def home():
        return render_template("index.html")
    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=False)
