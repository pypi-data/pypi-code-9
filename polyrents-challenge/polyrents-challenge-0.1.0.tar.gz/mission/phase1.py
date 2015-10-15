# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template


phase1 = Blueprint('phase1', __name__, url_prefix='/phase1/')


@phase1.route('')
def home():
    if request.cookies.get('uid') != '0':
        return render_template('phase1/home.html')
    else:
        return render_template('phase1/success.html')
