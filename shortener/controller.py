"""
Shortener API Responses
"""
import random, string
from flask import jsonify, redirect, request
from shortener.models import URL


def response(http_code, data=None):
    if data:
        return jsonify(data), http_code
    return '', http_code


def redirect_link_response(short_link):
    url = URL.query.filter_by(short=short_link).first_or_404()
    target = url.target
    if request.query_string:
        target = f'{target}?{request.query_string.decode("ascii")}'
    return redirect(target, code=301)


def get_short_link_response(config, short_link):
    url = URL.query.filter_by(short=short_link).first_or_404()
    return response(200, data={'url': url.to_web(config)})


def url_available(db, short_link):
    if short_link:
        return db.session.query(URL.id).filter_by(short=short_link).scalar() is None
    return False


def post_success(db, config, testing, target, short):
    url = URL(target=target, short=short)
    if not testing:
        db.session.add(url)
        db.session.commit()
    return response(201, data={'url': url.to_web(config)})


def generate_url(length):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def post_short_link_response(db, config, data):
    """
    Generate a short link based on the request `short` arg, `fallback`, or
    random string generation as a last resort
    """
    user_token = data.get('access_token')
    access_token = config['access_token']
    if not access_token or (access_token != user_token):
        return response(
            401, data={'error': 'You do not have permission to post links.'}
        )

    testing = data.get('testing', False)

    short = data.get('short')
    target = data.get('target')
    if not target:
        return response(400, data={'error': 'A target URL must be provided'})

    if url_available(db, short):
        return post_success(db, config, testing, target, short)

    fallback = data.get('fallback')
    if url_available(db, fallback):
        return post_success(db, config, testing, target, fallback)

    for length in [4, 5, 6, 7]:
        for _ in range(10):
            try_short = generate_url(length)
            if url_available(db, try_short):
                return post_success(db, config, testing, target, try_short)

    return response(400, data={'error': 'Unable to generate unique short url'})
