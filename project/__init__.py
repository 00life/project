from flask import Flask
app = Flask(__name__)

from project.home import Home
from project.ptq import PTQ
from project.lp import LP
from project.cm import CM
from project.ggo import GGO,Func_emailAll
from project.contact import Contact
from project.apps import Apps
from project.donate import Donate
from project.ideas import Ideas
from project.std import Std
from project.connect import DropMenu, CreateSTD_func, XmlSTD_func, XmlCM_func, ShowSTD_func
from project.admin import Admin

app.config['SECRET_KEY'] = '579aadeaeee0b8f9bbdadc18b5a6e2c8'

app.register_blueprint(Home,url_prefix="")
app.register_blueprint(PTQ,url_prefix="")
app.register_blueprint(LP,url_prefix="")
app.register_blueprint(CM,url_prefix="")
app.register_blueprint(GGO,url_prefix="")
app.register_blueprint(Contact,url_prefix="")
app.register_blueprint(Apps,url_prefix="")
app.register_blueprint(Donate,url_prefix="")
app.register_blueprint(Ideas,url_prefix="")
app.register_blueprint(Std,url_prefix="")
app.register_blueprint(DropMenu,url_prefix="")
app.register_blueprint(CreateSTD_func,url_prefix="")
app.register_blueprint(XmlSTD_func,url_prefix="")
app.register_blueprint(XmlCM_func,url_prefix="")
app.register_blueprint(ShowSTD_func,url_prefix="")
app.register_blueprint(Func_emailAll,url_prefix="")
app.register_blueprint(Admin,url_prefix="")