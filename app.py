from flask import Flask
from models import db
import requests
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'Planets_StarWars',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

response = requests.get("https://swapi.dev/api/planets/")
responseJson = response.json()

def DB_Helth():
    return "DB not install yet!"

def DB_Conect():
    return 0

def DB_Query(query):
    return 0

def DB_Insert(data):
    return 0

@app.route('/')
def Helth():
    return DB_Helth()

@app.route('/new/planet/<string:name>/climate/<string:climate>/terrain/<string:terrain>')
def AddPlanet(name,climate,terrain):
    return 0

@app.route('/planets')
def ListPlanets():
    return 0

@app.route('/planet/name/<string:name>')
def PlanetByName(name):
    return name

@app.route('/planet/id/<string:id>')
def PlanetById(id):
    return id

@app.route('/delete/planet/<string:name>')
def DeleteByName(name):
    return name

@app.route('/delete/planet/id/<string:id>')
def DeleteById(id):
    return id

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()