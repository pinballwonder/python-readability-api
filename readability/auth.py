# -*- coding: utf-8 -*-

"""
readability.core
~~~~~~~~~~~~~~~~

This module provides the authentication functionality for the Readability
HTTP API.

"""

import logging
import oauth2
import urllib
from cgi import parse_qsl


logger = logging.getLogger(__name__)
DEFAULT_BASE_URL_TEMPLATE = 'https://readability.com/api/rest/v1/{0}'
ACCESS_TOKEN_URL = 'oauth/access_token/'


def xauth(consumer_key, consumer_secret, username, password,
    base_url_template=DEFAULT_BASE_URL_TEMPLATE):
    """Returns an OAuth token that can be used with clients.BaseClient.

    :param consumer_key: Your Readability consumer key
    :type consumer_key: string

    :param consumer_secret: Your Readability consumer secret
    :type consumer_key: string

    :param username: A username
    :type username: string

    :param password: A password
    :type username: string

    :param base_url_template: Template for generating Readability API urls.
    :type base_url_template: string

    """
    # fetch oauth token from server
    consumer = oauth2.Consumer(consumer_key, consumer_secret)
    client = oauth2.Client(consumer)
    client.add_credentials(username, password)
    client.authorizations

    params = {}
    params['x_auth_username'] = username
    params['x_auth_password'] = password
    params['x_auth_mode'] = 'client_auth'

    client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    url = base_url_template.format(ACCESS_TOKEN_URL)

    logger.debug('POST to %s.', url)

    r, content = client.request(
        url, method='POST', body=urllib.urlencode(params))

    token = dict(parse_qsl(content))
    try:
        token = (token['oauth_token'], token['oauth_token_secret'])
    except KeyError:
        raise Exception('Invalid Credentials.')

    return token