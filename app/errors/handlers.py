# -*- coding: utf-8 -*-
__author__ = 'op'

from flask import render_template
from . import bp
from app import db


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404



@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
