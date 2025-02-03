from flask import Flask
from app.config import get_settings


app = Flask(__name__)
app.config.from_object(get_settings())

from app import views
