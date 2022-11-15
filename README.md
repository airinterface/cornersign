# cornersign

E-paper project

Dependency. 

set "lib" dir in [https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python)

1. git clone https://github.com/waveshare/e-Paper.git
And set it to environment variable "E_PAPER_LIB_DIR"
export E_PAPER_LIB_DIR=<Directory where you have e-Paper Project>/RaspberryPi_JetsonNano/python/lib


2. got to [https://api.mta.info/#/AccessKey](https://api.mta.info/#/AccessKey). Sign up if you haven't. 
   And get the api key 
   export MTA_API_KEY = < API KEY > 

   or add to .env below
   BUCKET_NAME, MTA_API_KEY

3. venv activate
4. run python app.py

