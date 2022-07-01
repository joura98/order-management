from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import UserAPI
from app.api import baozhuangAPI
from app.api import cailiaoAPI
from app.api import customerAPI
from app.api import dingdanAPI
from app.api import lightAPI
from app.api import loginAPI
from app.api import pictureAPI
from app.api import supplierAPI
from app.api import zhanshiAPI
