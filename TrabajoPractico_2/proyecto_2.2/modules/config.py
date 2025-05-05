from flask import Flask

app = Flask("server")

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from coverage import Coverage


    
