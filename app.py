from flask import Flask
app = Flask(__name__)

def DB_Helth():
    return "DB not install yet!"

def DB_Conect():
    return 0

def DB_Query(query):
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
    app.run()