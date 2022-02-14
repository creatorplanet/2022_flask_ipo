from flask import Flask, jsonify
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text 
import os 

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)  

def create_app():
    app = Flask(__name__) 
    app.json_encoder = CustomJSONEncoder   
    # if test_config is None:
    #     app.config.from_pyfile("config.py")
    # else:
    #     app.config.update(test_config)
    # database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0) 
    database = create_engine(os.environ['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database   
        
    @app.route('/python')
    def hello_python():    
        return'Hello, Python!'   

    @app.route("/ipocalendar", methods=['GET'])
    def ipo_calendar():
        rows = app.database.execute(text(""" 
            SELECT 
                company,
                ipo_date,
                confirmed_price,
                hope_price,
                competition_rate,
                organizer
            FROM ipo_calendar 
        """)).fetchall()
        ipo_calendar = [{
            'company' : row['company'], # 종목명
            'ipo_date' : row['ipo_date'], # 공모주일정
            'confirmed_price' : row['confirmed_price'],  # 확정공모가
            'hope_price' : row['hope_price'], # 희망공모가
            'competition_rate' : row['competition_rate'], # 청약경쟁률
            'organizer' : row['organizer'], # 주간사 
        } for row in rows]
        return jsonify({
            'ipo_calendar' : ipo_calendar
        })  

    @app.route("/newipo", methods=['GET'])
    def new_ipo():
        rows = app.database.execute(text(""" 
            SELECT
                company_id,
                new_ipo_date,
                confirmed_price_id,
                start_price,
                end_price
            FROM new_ipo
        """)).fetchall()
        new_ipo = [{
            'company_id' : row['company_id'], # 기업명
            'new_ipo_date' : row['new_ipo_date'], # 신규상장일
            'confirmed_price_id' : row['confirmed_price_id'], # 공모가(원)
            'start_price' : row['start_price'], # 시초가(원)
            'end_price' : row['end_price'], # 첫날종가(원) 
        } for row in rows]
        return jsonify({
            'new_ipo' : new_ipo
        }) 


    return app