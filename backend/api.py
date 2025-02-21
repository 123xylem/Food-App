from flask import Flask, render_template, jsonify
import requests
from menu_service import query_db, add_menu, SetMenu, get_menu_by_cuisine, get_cuisine_data, get_all_menus
from typing import List, Optional
# from db import init_db
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app, support_credentials=True)
print(CORS)

url = 'https://staging.yhangry.com/booking/test/set-menus'

# init_db()
@app.route("/api/menus/preview")
def preview_api_data():
    response = requests.get(url)
    return f"<pre>{response.text}</pre>"

#Sync db with api
@app.route("/api/menus/sync")
def sync_menus():
    response = requests.get(url)
    return add_menu(response)

@app.route("/api/menus/")
@cross_origin()
def request_all_menus()-> Optional[SetMenu]:
    try: 
        print('GETTING ALL MENUS')
        menus = jsonify(get_all_menus())
        print(menus, 'MENUS')
        return menus
    
    except Exception as e:
        return {"error!!!": str(e)}


@app.route("/api/menus/cuisine/<string:cuisine>")
@cross_origin()
def get_menus(cuisine: str)-> Optional[SetMenu]:
    try: 
        menus = get_menu_by_cuisine(cuisine)
        print(menus, 'MENUS')
        if menus:
          for menu in menus:
            print(menu, 'MENU')
        return jsonify(menus)
    
    except Exception as e:
        return {"error!!!": str(e)}
    

@app.route("/api/cuisines")
@cross_origin()
def get_cuisines():
    return jsonify(get_cuisine_data())
