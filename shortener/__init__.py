"""
Set up Shortener API
"""
import os
from flask import Blueprint, render_template, redirect, request, abort
from shortener.controller import *

# pylint: disable=unused-variable
def make_shortener(app):
    """
    Create Flask blueprint and set up API endpoints

    Args:
        app: The Flask App object

    Returns:
        New Flask blueprint
    """

    blueprint = Blueprint(
        'shortener',
        __name__,
        url_prefix='/api',
    )

    @app.route('/<string:short_link>', methods=['GET'])
    def redirect_link(short_link):
        return redirect_link_response(short_link)

    @blueprint.route('/links/<string:short_link>/', methods=['GET'])
    def get_short_link(short_link):
        return get_short_link_response(app.config, short_link)

    @blueprint.route('/links/', methods=['POST'])
    def post_short_link():
        data = request.get_json() or {}
        return post_short_link_response(app.db, app.config, data)

    return blueprint
