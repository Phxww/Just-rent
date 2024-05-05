import sys
sys.path.insert(0, '/Users/annachu/mento3/Just-rent')

# 切換目錄，一定要在引入app前
from app import app, db
from app.models import Location


locations = [
    # Taipei City
    Location(name="台北101店", address="110台北市信義區信義路五段7號", city="台北市",
             postal_code="110", latitude=25.0339639, longitude=121.5644722),
    Location(name="士林夜市店", address="111台北市士林區基河路101號", city="台北市",
             postal_code="111", latitude=25.087793, longitude=121.524207),
    Location(name="台北車站店", address="100台北市中正區北平西路3號", city="台北市",
             postal_code="100", latitude=25.047675, longitude=121.517055),

    # Kaohsiung City
    Location(name="高雄85店", address="802高雄市苓雅區自強三路1號", city="高雄市",
             postal_code="802", latitude=22.612686, longitude=120.301899),
    Location(name="駁二特區店", address="803高雄市鹽埕區大勇路1號", city="高雄市",
             postal_code="803", latitude=22.621033, longitude=120.285306),
    Location(name="左營高鐵店", address="813高雄市左營區高鐵路105號", city="高雄市",
             postal_code="813", latitude=22.686955, longitude=120.307945),

    # Taichung City
    Location(name="台中逢甲店", address="407台中市西屯區福星路459號", city="台中市",
             postal_code="407", latitude=24.178441, longitude=120.646672),

    # Tainan City
    Location(name="台南安平店", address="708台南市安平區安平路689號", city="台南市",
             postal_code="708", latitude=23.000675, longitude=120.159025),

    # Taoyuan City
    Location(name="桃園機場店", address="337桃園市大園區航站南路9號", city="桃園市",
             postal_code="337", latitude=25.077531, longitude=121.232823),
]

def create_loacations():
    with app.app_context():
        db.session.add_all(locations)
        db.session.commit()
        db.session.close()


if __name__ == "__main__":
    create_loacations()


