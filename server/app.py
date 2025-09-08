import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from controler import allControllers

load_dotenv()

app = Flask(__name__, template_folder="./templates")
app.secret_key = os.getenv("SECRET_KEY")

bcrypt = Bcrypt(app)
#adding blueprint(routes of controller using a loop 
# into main app)
for bp in allControllers:
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True)