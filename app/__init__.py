# basically just iniatializes the website i think

from flask import Flask
from config import Config
from flask_session import Session
import webbrowser

sess = Session()
# starts the app
app = Flask(__name__, template_folder='templates')
# sets the config
app.config.from_object(Config)
# sets up the session
sess.init_app(app)
# gets the website routes and db layout
from app import routes
# opens the web browser
webbrowser.open('http://localhost:5000', new=2, autoraise=True )
# runs the app
app.run()