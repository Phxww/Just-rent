# 切換目錄，一定要在引入app前
import sys
sys.path.insert(0, '/Users/annachu/mento3/Just-rent')

# 引入app和model
from app import app, db
from sqlalchemy import text
from app.models import User, Car
import json

# 檢查資料庫資料
# def query_cars_with_raw_sql():
#     with app.app_context():
#         sql = "SELECT * FROM users"
#         result = db.session.execute(text(sql))
#         for row in result:
#             print(row)
# if __name__ == "__main__":
#     print("\nQuerying with Raw SQL:")
#     query_cars_with_raw_sql()


def import_cars():
    with open('/Users/annachu/mento3/Just-rent/app/script/cars.json', 'r') as f:
        cars_data = json.load(f)

    with app.app_context():
        for car_data in cars_data:
            # car_data['door'] = int(car_data['door'].replace('門', ''))
            car = Car(
                name=car_data.get("name"),
                brand=car_data.get("brand"),
                year=car_data.get("year"),
                model=car_data.get("model"),
                body=car_data.get("body"),
                door=car_data.get("door"),
                seat=car_data.get("seat"),
                car_length=car_data.get("car_length"),
                wheelbase=car_data.get("wheelbase"),
                power_type=car_data.get("power_type"),
                displacement=car_data.get("displacement"),
            )
            db.session.add(car)

        db.session.commit()
        db.session.close()


if __name__ == "__main__":
    import_cars()
