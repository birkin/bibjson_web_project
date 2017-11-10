# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from . import settings_app
from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from bib_ourl_api_app.lib.openurl import bib_from_openurl, openurl_from_bib


log = logging.getLogger(__name__)


def ourl_to_bib( request ):
    """ Converts openurl to bibjson. """
    log.debug( '\n\n\nstarting ourl_to_bib()...' )
    start = datetime.datetime.now()
    ourl = request.GET.get( 'ourl', None )
    if not ourl:
        return HttpResponseBadRequest( '400 / Bad Request -- no `ourl` openurl parameter')
    log.debug( 'ourl, ```%s```' % ourl )
    bib = bib_from_openurl( ourl )
    log.debug( 'type(bib), `%s`' % type(bib) )
    log.debug( 'bib, ```%s```' % bib )
    rtrn_dct = {
        'query': {
            'ourl': ourl,
            'date_time': str( start )
        },
        'response': {
            'bib': bib,
            'elapsed_time': str( datetime.datetime.now() - start )
        }
    }
    jsn = json.dumps( rtrn_dct, sort_keys=True, indent=2 )
    return HttpResponse( jsn, content_type='application/javascript; charset=utf-8' )


def bib_to_ourl( request ):
    """ Converts bibjson to openurl. """
    log.debug( '\n\n\nstarting bib_to_ourl()...' )
    start = datetime.datetime.now()
    bibjson = request.GET.get( 'bibjson', None )
    if not bibjson:
        return HttpResponseBadRequest( '400 / Bad Request -- no `bibjson` parameter')
    bib = json.loads( bibjson )
    ourl = openurl_from_bib(bib)
    log.debug( 'ourl, ```%s```' % ourl )
    rtrn_dct = {
        'ourl': ourl
    }
    jsn = json.dumps( rtrn_dct, sort_keys=True, indent=2 )
    return HttpResponse( jsn, content_type='application/javascript; charset=utf-8' )


def access_test( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    log.debug( 'now-time, ```%s```' % str(now) )
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )


def info( request ):
    """ Returns simplest response. """
    return HttpResponseRedirect( settings_app.README_URL )
