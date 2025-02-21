import json, datetime as date
from db import SetMenu, Cuisine, menu_cuisines, app, db
from typing import Optional
from sqlalchemy import func, desc
def query_db():
    with app.app_context():
        return (
            SetMenu.query.all(), 
            Cuisine.query.all()
        )
    
def returnPagination(select):
    with app.app_context():
        pagination = db.paginate(select, page = 1, per_page=20, max_per_page=10)
        print(pagination, 'PAGINATION')
        return {
              "menus": [set_menu.list_data() for set_menu in pagination.items],
              "total": pagination.total,
              "pages": pagination.pages,
              "current_page": pagination.page
          }
    
def get_menu_by_cuisine(cuisine: str) -> Optional[SetMenu]:
    with app.app_context():
        name = cuisine.replace('-', ' ').title()
        
        query = (SetMenu.query
            .join(menu_cuisines)
            .join(Cuisine)
            .filter(
                func.lower(Cuisine.name) == func.lower(name),
                SetMenu.status == 1
            )
            .order_by(SetMenu.number_of_orders.desc()))
        
        return {
            "menus": [menu.list_data() for menu in query.all()],
            "total": query.count()
        }
        
        
#Use indexing to optimse faster queryies

def get_all_menus() -> Optional[SetMenu]:
    with app.app_context():
        # Get all menus without pagination first
        query = (SetMenu.query
            .filter(SetMenu.status == 1)
            .order_by(SetMenu.number_of_orders.desc()))
        
        return {
            "menus": [menu.list_data() for menu in query.all()],
            "total": query.count()
        }

def get_cuisine_data():
    with app.app_context():

      cuisine_data = (db.session.query(
          Cuisine.name,
          Cuisine.id,
          func.count(SetMenu.id).filter(SetMenu.status == 1).label('menu_count'),
          func.sum(SetMenu.number_of_orders)              
              .label('total_orders')
      )
      .select_from(Cuisine)
      .join(menu_cuisines)                               
      .join(SetMenu)
      .group_by(Cuisine.name) 
      .order_by(desc('total_orders'))
      .all())
    return {
        "cuisines": [{"id": cuisine.id, "name": cuisine.name, "menu_count": cuisine.menu_count, "total_orders": cuisine.total_orders} for cuisine in cuisine_data]
    }


def add_menu(data):
    try:
        with app.app_context():
            json_data = data.json()['data']
            if not isinstance(json_data, list):
                json_data = [json_data]
            
            for menu in json_data:
                if isinstance(menu, str):
                    menu = json.loads(menu)
                
                menu_cuisines = []
                cuisine_data = menu.pop('cuisines', [])
                for c_data in cuisine_data:
                    cuisine = Cuisine.query.get(c_data['id']) or Cuisine(**c_data)
                    menu_cuisines.append(cuisine)
                
                if 'created_at' in menu:
                    menu['created_at'] = date.datetime.fromisoformat(
                        menu['created_at'].replace('Z', '')
                    )
                
                menu_item = SetMenu(
                    **menu,
                    cuisines=menu_cuisines
                )
                db.session.add(menu_item)
            
            db.session.commit()
            return {"message": "Data imported successfully"}
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}

