# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from . import settings_app
from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)


def ourl_to_bib( request ):
    """ Converts openurl to bibjson. """
    log.debug( '\n\n\nstarting ourl_to_bib()...' )
    # if v1_validator.validate_request( request.method, request.META.get('REMOTE_ADDR', ''), request.POST ) is False:
    #     log.info( 'request invalid, returning 400' )
    #     return HttpResponseBadRequest( '400 / Bad Request' )
    # result_data = caller.request_exact( request.POST )
    # interpreted_response_dct = caller.interpret_result( result_data )
    # log.debug( 'returning response' )
    # jsn = json.dumps( interpreted_response_dct, sort_keys=True, indent=2 )
    # return HttpResponse( jsn, content_type='application/javascript; charset=utf-8' )
    return HttpResponse( 'ourl_to_bib coming' )


def bib_to_ourl( request ):
    """ Converts bibjson to openurl. """
    log.debug( '\n\n\nstarting bib_to_ourl()...' )
    if v2_request_validator.validate_bib_request( request.method, request.META.get('REMOTE_ADDR', ''), request.POST ) is False:
        log.info( 'request invalid, returning 400' )
        return HttpResponseBadRequest( '400 / Bad Request' )
    ( patron_barcode, title, author, year ) = ( request.POST['patron_barcode'], request.POST['title'], request.POST['author'], request.POST['year'] )
    result_dct = v2_request_bib_caller.request_bib( patron_barcode, title, author, year )
    log.debug( 'returning response' )
    jsn = json.dumps( result_dct, sort_keys=True, indent=2 )
    return HttpResponse( jsn, content_type='application/javascript; charset=utf-8' )
    return HttpResponse( 'bib_to_ourl coming' )


def access_test( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    log.debug( 'now-time, ```%s```' % str(now) )
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )


def info( request ):
    """ Returns simplest response. """
    return HttpResponseRedirect( settings_app.README_URL )
