from flask import Flask
from flask_restful import Api
from page_rotation.rotate import RotatePage

app = Flask(__name__)
api = Api(app)

# Route
api.add_resource(RotatePage, '/rotate_page')

if __name__ == '__main_':
    app.run(port=5000)