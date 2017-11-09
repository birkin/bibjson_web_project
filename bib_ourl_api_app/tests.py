# -*- coding: utf-8 -*-

import json, logging, pprint
from django.test import SimpleTestCase    ## TestCase requires db
from bib_ourl_api_app import settings_app


log = logging.getLogger(__name__)
SimpleTestCase.maxDiff = None


class SomeTest( SimpleTestCase ):
    """ Checks ... library. """

    def setUp(self):
        pass

    def test_a(self):
        """ Checks ... """
        self.assertEqual( 1, 2 )


class AnotherTest( SimpleTestCase ):
    """ Checks ... library. """

    def setUp(self):
        pass

    def test_b(self):
        """ Checks ... """
        self.assertEqual( 3, 4 )
