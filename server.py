from flask import Flask, Response
from dotenv import load_dotenv
# Loading up the values
load_dotenv()

from data_modules.subway.main import update_data as update_subway_data

app = Flask(__name__)


@app.route('/')
def hello_world():
   return "Hello, World!"

@app.route('/update_subway')
def update_subway():
   update_subway_data();
   response = Response(status=200)
   return response


if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=8000)
