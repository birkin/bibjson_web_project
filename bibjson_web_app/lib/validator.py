# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint, time
import requests
from bdpy3 import BorrowDirect
from bdpy3_web_app import settings_app


log = logging.getLogger(__name__)


class V2RequestValidator( object ):
    """ Contains validation functions for views.v2 item-requests """

    def __init__( self ):
        log.debug( 'helper initialized' )
        pass

    def validate_bib_request( self, method, ip, post_params ):
        """ Checks request validity; returns boolean.
            Called by views.v1() """
        log.debug( 'method, `%s`' % method )
        validity = False
        if method == 'POST':
            if self.check_keys( post_params ) is True:
                if self.check_ip( ip ) is True:
                    if self.check_auth( post_params ) is True:
                        validity = True
        log.debug( 'overall_validity, `%s`' % validity )
        return validity

    def check_keys( self, params ):
        """ Checks required keys; returns boolean.
            Called by validate_request() """
        log.debug( 'params, ```%s```' % pprint.pformat(params) )
        keys_good = False
        required_keys = [ 'api_authorization_code', 'api_identity', 'patron_barcode', 'title', 'author', 'year' ]
        for required_key in required_keys:
            if required_key not in params.keys():
                break
            if required_key == required_keys[-1]:
                keys_good = True
        log.debug( 'keys_good, `%s`' % keys_good )
        return keys_good

    def check_ip( self, ip ):
        """ Checks ip; returns boolean.
            Called by validate_request() """
        validity = False
        if ip in settings_app.LEGIT_IPS:
            validity = True
        else:
            log.debug( 'bad ip, `%s`' % ip )
        log.debug( 'validity, `%s`' % validity )
        return validity

    def check_auth( self, params ):
        """ Checks auth params; returns boolean.
            Called by validate_request() """
        validity = False
        if params.get( 'api_authorization_code', 'nope' ) == settings_app.WEB_API_AUTHORIZATION_CODE:
            if params.get( 'api_identity', 'nope' ) == settings_app.WEB_API_IDENTITY:
                validity = True
        log.debug( 'validity, `%s`' % validity )
        return validity

    ## end class V2RequestValidator()
