from flask import Flask 
from digitaltimes import create_app

app = Flask(__name__)

if __name__ == '__main__':
    # app.run(host='192.168.0.105') 
    napp=create_app()
    napp.run(debug=True)