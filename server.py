from flask import Flask
from data_modules.subway.main import update_data as update_subway_data

app = Flask(__name__)

from dotenv import load_dotenv
# Loading up the values
load_dotenv()

@app.route('/')
def hello_world():
   return "Hello, World!"

@app.route('/update_subway')
def update_subway():
   update_subway_data();

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=8000)
