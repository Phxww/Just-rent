from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# 使用flask run目前這段程式碼沒有效益
# 使用 python app/__init__.py 才會有效益
# if __name__ == "__main__":
#     app.run(debug=True, port=5001)

from app import routes, models

