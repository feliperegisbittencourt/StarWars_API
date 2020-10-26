from flask import Flask, Response, jsonify
from models import db
import requests
import psycopg2
import json
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

def DB_Query_JSON(query):
    dic = {
        'planetsid': 'id',
        'planetname': 'name',
        'planetclimate': 'climate',
        'planetterrain': 'terrain',
        'films': 'films'
    }
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    results = []
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        linha = dict(zip(columns, row))
        obj = {}
        for l in linha:
            obj[dic[l]] = linha[l]
        results.append(obj)
    
    cursor.close()
    conn.close()

    return results


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
    id = result[-1] + 1
    #print(lastTree)
    DB_Insert(name,climate,terrain,0,id)
    return "Insert Planet"

@app.route('/planets')
def ListPlanets():
    planets = DB_Query_JSON(f'''SELECT planetsid, planetname FROM planets''')
    return Response(json.dumps({'planets': planets}), mimetype="application/json")

@app.route('/planet/name/<string:name>')
def PlanetByName(name):
    planet = DB_Query_JSON(f"SELECT * FROM planets WHERE planetname LIKE '" + str(name) + "'")
    return Response(json.dumps({'planet': planet}), mimetype="application/json")

@app.route('/planet/id/<string:id>')
def PlanetById(id):
    planet = DB_Query_JSON(f"SELECT * FROM planets WHERE planetsid = '" + str(id) + "'")
    return Response(json.dumps({'planet': planet}), mimetype="application/json")

@app.route('/delete/planet/<string:name>')
def DeleteByName(name):
    query = "DELETE from planets WHERE planetname LIKE '" + str(name) + "'"
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return "Planet Removed"

@app.route('/delete/planet/id/<string:id>')
def DeleteById(id):
    query = "DELETE from planets WHERE planetsid LIKE '" + str(id) + "'"
    conn = psycopg2.connect(database="Planets_StarWars", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    return "Planet Removed"

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()