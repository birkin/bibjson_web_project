# -*- coding: utf-8 -*-

import json, logging, pprint
from django.test import SimpleTestCase    ## TestCase requires db
from bdpy3_web_app import settings_app
from bdpy3_web_app.lib.app_helper import LibCaller


log = logging.getLogger(__name__)
SimpleTestCase.maxDiff = None


class Bdpy3LibTest_RequestExact( SimpleTestCase ):
    """ Checks call to bdpy3 library. """

    def setUp(self):
        self.libcaller = LibCaller()

    def test_request_exact_search__not_found(self):
        """ Checks lib-caller exact-search on not-found. """
        params = { 'user_barcode': settings_app.TEST_PATRON_BARCODE, 'isbn': settings_app.TEST_ISBN_NOT_FOUND }
        result = self.libcaller.request_exact( params )
        self.assertEqual(
            dict,
            type(result)
        )
        self.assertEqual(
            {'Problem': {'ErrorCode': 'PUBRI003', 'ErrorMessage': 'No result'}},
            result
        )


class ClientTest_RequestExact( SimpleTestCase ):
    """ Checks client exact-search on not-found. """

    def test_v1_request_exact__not_found(self):
        """ Checks '/v1/ request-exact call'.
            NOTE: this will really attempt a request! """
        parameter_dict = {
            'api_authorization_code': settings_app.TEST_AUTH_CODE,
            'api_identity': settings_app.TEST_IDENTITY,
            'isbn': settings_app.TEST_ISBN_NOT_FOUND,
            'user_barcode': settings_app.TEST_PATRON_BARCODE
        }
        response = self.client.post( '/v1/', parameter_dict )  # project root part of url is assumed
        self.assertEqual( 200, response.status_code )
        self.assertEqual( bytes, type(response.content) )
        dct = json.loads( response.content )
        log.debug( 'dct, ```%s```' % pprint.pformat(dct) )
        self.assertEqual( {
            'bd_confirmation_code': None,
            'found': False,
            'requestable': False,
            'search_result': 'FAILURE'
            },
            dct
        )


class ClientTest_RequestBib__not_found( SimpleTestCase ):
    """ Checks client bib-search on not-found.
        NOTE: this will really attempt a request! """

    def test_v2_request_bib__not_found(self):
        """ Checks '/v2/ request-bib call for not-found item'. """
        parameter_dict = {
            'api_authorization_code': settings_app.TEST_AUTH_CODE,
            'api_identity': settings_app.TEST_IDENTITY,
            'patron_barcode': settings_app.TEST_PATRON_BARCODE,
            'title': 'Zen and the Art of Motorcycle Maintenance',
            'author': 'Robert M. Pirsig',
            'year': '1874'
        }
        response = self.client.post( '/v2/bib_request/', parameter_dict )  # project root part of url is assumed
        self.assertEqual( 200, response.status_code )
        self.assertEqual( bytes, type(response.content) )
        dct = json.loads( response.content )
        log.debug( 'dct, ```%s```' % pprint.pformat(dct) )
        self.assertEqual(
            [ 'request', 'response' ],
            sorted( dct.keys() )
        )


'''
## disabled because this will really generate a request
class ClientTest_RequestBib__found( SimpleTestCase ):
    """ Checks client bib-search on found item.
        NOTE: this will really attempt a request! """

    def test_v2_request_bib__not_found(self):
        """ Checks '/v2/ request-bib call for found item'. """
        parameter_dict = {
            'api_authorization_code': settings_app.TEST_AUTH_CODE,
            'api_identity': settings_app.TEST_IDENTITY,
            'patron_barcode': settings_app.TEST_PATRON_BARCODE,
            'title': 'Zen and the art of motorcycle maintenance - an inquiry into values',
            'author': 'Robert M. Pirsig',
            'year': '1974'
        }
        response = self.client.post( '/v2/bib_request/', parameter_dict )  # project root part of url is assumed
        self.assertEqual( 200, response.status_code )
        self.assertEqual( bytes, type(response.content) )
        dct = json.loads( response.content )
        log.debug( 'dct, ```%s```' % pprint.pformat(dct) )
        self.assertEqual(
            [ 'request', 'response' ],
            sorted( dct.keys() )
        )
'''


class RootUrlTest( SimpleTestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    # end class RootUrlTest()
