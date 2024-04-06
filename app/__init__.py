from flask import Flask

app = Flask(__name__)


# 使用flask run目前這段程式碼沒有效益
# 使用 python app/__init__.py 才會有效益
# if __name__ == "__main__":
#     app.run(debug=True, port=5001)

from app import routes

