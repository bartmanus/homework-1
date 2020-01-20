from flask import (
    Blueprint, url_for
)
from random import random


bp = Blueprint('dynamic', __name__)

@bp.route('/')
def index():
    return {
        'link': url_for('dynamic.dynamic')
    }

# a simple page that returns something dynamic 
@bp.route('/dynamic') 
def dynamic():
    return {
        'dynamic': f'{random()}'
    }

