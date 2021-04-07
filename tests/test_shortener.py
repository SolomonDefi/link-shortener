"""
Test the URL shortener API
"""


def test_short_urls(client, app):
    """
    Test creating and getting short urls
    """
    test_url1 = 'supplies'
    test_url2 = 'supplies2'
    test_target = 'https://solomondefi.com'
    access_token = app.config['access_token']
    server_name = app.config['SERVER_NAME']

    # Get non-existent url
    rsp = client.get(f'/api/links/{test_url1}/')
    assert rsp.status_code == 404

    # Missing access token
    rsp = client.post('/api/links/', json={'short': test_url1, 'target': test_target})
    assert rsp.status_code == 401

    # Successfully create a link
    rsp = client.post(
        '/api/links/',
        json={'access_token': access_token, 'short': test_url1, 'target': test_target},
    )
    assert rsp.status_code == 201
    url = rsp.get_json()['url']
    assert url['short'] == test_url1
    assert url['target'] == test_target
    assert url['short_url'] == f'{server_name}/{test_url1}'

    rsp = client.get(f'/api/links/{test_url1}/')
    assert rsp.status_code == 200
    assert rsp.get_json()['url'] == url

    # Successfully create a link with fallback
    rsp = client.post(
        '/api/links/',
        json={
            'access_token': access_token,
            'short': test_url1,
            'fallback': test_url2,
            'target': test_target,
        },
    )
    assert rsp.status_code == 201
    url = rsp.get_json()['url']
    assert url['short'] == test_url2

    # Successfully create a link with random generation
    rsp = client.post(
        '/api/links/',
        json={
            'access_token': access_token,
            'short': test_url1,
            'fallback': test_url2,
            'target': test_target,
        },
    )
    assert rsp.status_code == 201
    url = rsp.get_json()['url']
    assert url['short'] != test_url1
    assert url['short'] != test_url2
    assert len(url['short']) == 4

    # Successfully create a link with random generation
    rsp = client.post(
        '/api/links/', json={'access_token': access_token, 'target': test_target}
    )
    assert rsp.status_code == 201
    url = rsp.get_json()['url']
    assert len(url['short']) == 4


def test_short_redirect(client, app):
    """
    Test short url redirects
    """
    test_url1 = '1'
    test_target = 'https://solomondefi.com'
    access_token = app.config['access_token']

    # Create a link and test the redirect
    rsp = client.post(
        '/api/links/',
        json={'access_token': access_token, 'target': test_target, 'short': test_url1},
    )
    assert rsp.status_code == 201
    short = rsp.get_json()['url']['short']

    rsp = client.get(f'/{short}?ref=share')
    assert rsp.status_code == 301
    assert rsp.location == f'{test_target}?ref=share'
