from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
from flask_wtf import CSRFProtect
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)  # 綁定 LoginManager於app，負責管理使用登入流程
login.login_view = 'login'  # 如果未登入，會自動重新定向到視圖函示的endpoint。目前endpoint將視圖函示的名稱默認



# 使用flask run目前這段程式碼沒有效益
# 使用 python app/__init__.py 才會有效益
# if __name__ == "__main__":
#     app.run(debug=True, port=5001)

from app import routes, models

