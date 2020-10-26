from flask import Flask
from models import db
import requests
import psycopg2
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'Planets_StarWars',
    'host': 'localhost',
    'port': '5432',
}

POSTGRESstr = "database='Planets_StarWars', user='postgres', password='postgres', host='127.0.0.1', port= '5432'"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

def DB_Helth():
    return "DB not install yet!"

def DB_Conect():
    #conn = psycopg2.connect(POSTGRESstr)
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    return 0

def DB_Query(query):
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close()
    return result

def DB_Insert(name, climate, terrain, films, id):
    sql = "INSERT INTO planets (planetsid, planetname, planetclimate, planetterrain, films) VALUES (" + str(id) + ", '" +  str(name) + "', '" + str(climate) + "', '" + str(terrain) + "', '" + str(films) + "')"
    #sql = '''INSERT INTO planets (planetname, planetclimate, planetterrain, films) VALUES ('str(name)', 'str(climate)', 'str(terrain)', 'str(films)')'''
    #DB_Conect()
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor = cursor.execute(sql)
    conn.commit()
    conn.close()
    return 0

def DB_Clean():
    sql = "DELETE FROM planets"
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor = cursor.execute(sql)
    conn.commit()
    conn.close()
    return 0

response = requests.get("https://swapi.dev/api/planets/")
responseJson = response.json()
i = 1
DB_Clean()
for x in responseJson['results']:
    planetName = x['name']
    planetClimate = x['climate']
    planetTerrain = x['terrain']
    films = len(x['films'])
    id = i
    DB_Insert(planetName, planetClimate, planetTerrain, films, id)
    i = i  + 1
while responseJson['next'] is not None:
    response = requests.get(responseJson['next'])
    responseJson = response.json()
    for x in responseJson['results']:
        planetName = x['name']
        planetClimate = x['climate']
        planetTerrain = x['terrain']
        films = len(x['films'])
        id = i
        DB_Insert(planetName, planetClimate, planetTerrain, films, id)
        i = i + 1


@app.route('/')
def Helth():
    return DB_Helth()

@app.route('/new/planet/<string:name>/climate/<string:climate>/terrain/<string:terrain>')
def AddPlanet(name,climate,terrain):
    resultQuery = DB_Query('SELECT * from planets WHERE planetsid = (SELECT MAX(planetsid) FROM planets)')
    result = resultQuery[0]
    id = result[-1]
    #print(lastTree)
    DB_Insert(name,climate,terrain,0,id)
    return "Insert Planet"

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