from flask import Flask
from init_db import init_neo4j
from routes.phone_blueprint import phone_blueprint

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
app.register_blueprint(phone_blueprint)

with app.app_context():
    app.neo4j_driver = init_neo4j()

if __name__ == '__main__':
    app.run()
