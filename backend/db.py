from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from typing import Optional
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  
# Rate limit for ddos  
app.config['RATELIMIT_DEFAULT'] = "60/minute"

app.config['SQLALCHEMY_CUSTOM_OPTIONS'] = {
    'paramstyle': 'named'  
}
db = SQLAlchemy(app)
# def init_db():
#     with app.app_context():
#         db.create_all()
#         print("Sample data created successfully!")

# Association table for many-to-many relationship
menu_cuisines = db.Table('menu_cuisines',
    db.Column('set_menu_id', db.Integer, db.ForeignKey('set_menu.id')),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('cuisine.id'))
)

class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class SetMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cuisines = db.relationship(
        'Cuisine', 
        secondary=menu_cuisines,
        backref='menus'
    )
    description = db.Column(db.String(500))
    display_text = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(500))
    thumbnail = db.Column(db.String(500))
    is_vegan = db.Column(db.Boolean, default=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    status = db.Column(db.Integer, default=1)
    groups = db.Column(db.JSON, default={
        "dishes_count": 0,
        "selectable_dishes_count": 0,
        "groups": {
            "ungrouped": 0
        }
    })
    price_per_person = db.Column(db.Float)
    min_spend = db.Column(db.Float)
    is_seated = db.Column(db.Boolean, default=False)
    is_standing = db.Column(db.Boolean, default=False)
    is_canape = db.Column(db.Boolean, default=False)
    is_mixed_dietary = db.Column(db.Boolean, default=False)
    is_meal_prep = db.Column(db.Boolean, default=False)
    is_halal = db.Column(db.Boolean, default=False)
    is_kosher = db.Column(db.Boolean, default=False)
    price_includes = db.Column(db.String(500))
    highlight = db.Column(db.String(500))
    available = db.Column(db.Boolean, default=True)
    number_of_orders = db.Column(db.Integer, default=0)
    

    #could add redis cache here for frequently accessed data 
    def list_data(self):
      return {
          'id': self.id,
          'name': self.name,
          'description': self.description,
          'price_per_person': self.price_per_person,
          'min_spend': self.min_spend,
          'groups': self.groups,
          'cuisines': [
              {'id': c.id, 'name': c.name} 
              for c in self.cuisines
          ],
          'image': self.image,
          'thumbnail': self.thumbnail,
          'is_vegan': self.is_vegan,
          'is_vegetarian': self.is_vegetarian,
          'is_seated': self.is_seated,
          'is_standing': self.is_standing,
      }
