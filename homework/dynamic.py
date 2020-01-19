from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from random import random


bp = Blueprint('dynamic', __name__)

@bp.route('/')
def index():
   return url_for('dynamic.dynamic')

# a simple page that returns something dynamic 
@bp.route('/dynamic') 
def dynamic(): 
    return f'{random()}' 

