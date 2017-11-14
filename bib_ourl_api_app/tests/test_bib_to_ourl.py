# -*- coding: utf-8 -*-

import cgi, json, logging, pprint

from bib_ourl_api_app import settings_app
from bib_ourl_api_app.lib.openurl import bib_from_openurl, bib_from_qdict, openurl_from_bib
from django.test import SimpleTestCase  ## TestCase requires db


log = logging.getLogger(__name__)
SimpleTestCase.maxDiff = None


class TestClient( SimpleTestCase ):
    """ Checks client url hit. """

    def setUp(self):
        self.bibjson = '''{
      "_rfr": "info:sid/firstsearch.oclc.org:MEDLINE",
      "author": [
        {
          "firstname": "BK",
          "lastname": "Frogner",
          "name": "Frogner, BK"
        }
      ],
      "end_page": "71",
      "identifier": [
        {
          "id": "1175-5652",
          "type": "issn"
        },
        {
          "id": "678061209",
          "type": "oclc"
        }
      ],
      "issue": "6",
      "journal": {
        "name": "Applied health economics and health policy"
      },
      "pages": "361 - 71",
      "place_of_publication": null,
      "publisher": null,
      "start_page": "361",
      "title": "The missing technology: an international comparison of human capital investment in healthcare.",
      "type": "article",
      "volume": "8",
      "year": "2010"
    }'''

    def test_v1_bibjson_get(self):
        """ Checks '/v1/ request-exact call'. """
        params = { 'bibjson': self.bibjson }
        headers = {'HTTP_HOST': '127.0.0.1', 'REQUEST_URI': 'foo'}  # passing in headers: <https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.Client.get>
        response = self.client.get( '/v1/bib_to_ourl/', params, **headers )  # project root part of url is assumed
        self.assertEqual(
            200, response.status_code
        )
        self.assertEqual(
            bytes, type(response.content)
        )
        dct = json.loads( response.content )
        self.assertEqual(
            ['query', 'response'], sorted( dct.keys() )
        )
        self.assertEqual(
            '''ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Ajournal&rft.atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&rft.jtitle=Applied+health+economics+and+health+policy&rft.genre=article&rfr_id=info%3Asid/info%3Asid/firstsearch.oclc.org%3AMEDLINE&rft.date=2010&rft.au=Frogner%2C+BK&rft.volume=8&rft.issue=6&rft.spage=361&rft.end_page=71&rft.pages=361+-+71&rft.issn=1175-5652&rft_id=http%3A//www.worldcat.org/oclc/678061209''',
            dct['response']['openurl']
        )

    ## end class TestClient()


class TestThesisToOpenURL( SimpleTestCase ):
    """
    Testing thesis and dissertations.  Pulled from logs May, 2014.
    """

    def test_a(self):
        #http://search.proquest.com/pqdtft/docview/1473656916/abstract
        q = 'ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Mangla%2C+Akshay&rft.aulast=Mangla&rft.aufirst=Akshay&rft.date=2013-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=&rft.btitle=&rft.title=Rights+for+the+Voiceless%3A+The+State%2C+Civil+Society+and+Primary+Education+in+Rural+India&rft.issn=&rft_id=info:doi/'
        b = bib_from_openurl(q)
        self.assertEqual(b['title'], 'Rights for the Voiceless: The State, Civil Society and Primary Education in Rural India')
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Mangla, Akshay')

    def test_b(self):
        q = u"""
?ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Grossman%2C+Robert+Allen&rft.aulast=Grossman&rft.aufirst=Robert&rft.date=1988-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=&rft.btitle=&rft.title=The+Lute+Suite+in+G+Minor+BWV+995+by+Johann+Sebastian+Bach%3A+A+comparison+of+the+autograph+manuscript+and+the+lute+intabulation+in+Leipzig%2C+Sammlung+Becker%2C+MS.+111.ii.3&rft.issn=&rft_id=info:doi/
"""
        b = bib_from_openurl(q)
        self.assertTrue('Lute Suite in G Minor BWV 995 by Johann Sebastian Bach' in b['title'])
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['year'], '1988')

    def test_c(self):
        q = u"""
ctx_ver=Z39.88-2004&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Benjamin%2C+Ruha&rft.aulast=Benjamin&rft.aufirst=Ruha&rft.date=2008-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=9780549836568&rft.btitle=&rft.title=Culturing+consent%3A+Science+and+democracy+in+the+stem+cell+state&rft.issn=&rft_id=info:doi/
"""
        b = bib_from_openurl(q)
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Benjamin, Ruha')
        #ids
        ids = b['identifier']
        self.assertTrue(
            {
            'type': 'isbn', 'id': '9780549836568'
            } in ids
        )
        self.assertTrue(
            {
            'type': 'doi', 'id': 'doi:\n'
            } not in ids
        )

    def test_d(self):
        q = u"""
ctx_ver=Z39.88-2004&ctx_enc=info:ofi/enc:UTF-8&rfr_id=info:sid/ProQuest+Dissertations+%26+Theses+Full+Text&rft_val_fmt=info:ofi/fmt:kev:mtx:dissertation&rft.genre=dissertations+%26+theses&rft.jtitle=&rft.atitle=&rft.au=Ahuja%2C+Amit&rft.aulast=Ahuja&rft.aufirst=Amit&rft.date=2008-01-01&rft.volume=&rft.issue=&rft.spage=&rft.isbn=9780549979340&rft.btitle=&rft.title=Mobilizing+marginalized+citizens%3A+Ethnic+parties+without+ethnic+movements&rft.issn=&rft_id=info:doi/
"""
        b = bib_from_openurl(q)
        self.assertEqual(b['type'], 'dissertation')
        self.assertEqual(b['author'][0]['name'], 'Ahuja, Amit')
        self.assertEqual(b['title'], 'Mobilizing marginalized citizens: Ethnic parties without ethnic movements')
        self.assertEqual(b['identifier'][0]['id'], '9780549979340')

    ## end class TestThesisToOpenURL()


class TestToOpenURL( SimpleTestCase ):

    def test_book_chapter(self):
        q = 'sid=info:sid/sersol:RefinerQuery&genre=bookitem&isbn=9781402032899&&title=The+roots+of+educational+change&atitle=Finding+Keys+to+School+Change%3A+A+40-Year+Odyssey&volume=&part=&issue=&date=2005&spage=25&epage=57&aulast=Miles&aufirst=Matthew'
        b = bib_from_openurl(q)
        ourl = openurl_from_bib(b)
        qdict = cgi.parse_qs(ourl)
        self.assertTrue('bookitem' in qdict.get('rft.genre'))

    def test_missing_title(self):
        #Mock a sample request dict coming from Django.
        request_dict = {
        'rft.pub': ['Triple Canopy'],
        'rft_val_fmt': ['info:ofi/fmt:kev:mtx:book'],
        'rfr_id': ['info:sid/libx:brown'],
        'rft.au': ['Coleman,&#32;Gabriella'],
        'rft.aulast': ['Coleman'],
        'rft.aufirst': ['Gabriella'],
        'rft_id': ['http://canopycanopycanopy.com/15/our_weirdness_is_free'],
        'rft.btitle': ['Our Weirdness Is Free: The logic of Anonymous \u2014 online army, agent of chaos, and seeker of justice'],
        'url_ver': ['Z39.88-2004'],
        'rft.atitle': [''],
        'rft.genre': ['bookitem']}
        b = bib_from_qdict(request_dict)
        ourl = openurl_from_bib(b)
        parsed_ourl = cgi.parse_qs(ourl)
        self.assertTrue('bookitem' in parsed_ourl.get('rft.genre'))
        self.assertTrue('Coleman, Gabriella' in parsed_ourl.get('rft.au'))

    def test_dissertation(self):
        request = {
            'ctx_enc': ['info:ofi/enc:UTF-8'],
            'ctx_ver': ['Z39.88-2004'],
            'rft.au': ['Mangla, Akshay'],
            'rft.aufirst': ['Akshay'],
            'rft.aulast': ['Mangla'],
            'rft.date': ['2013-01-01'],
            'rft.genre': ['dissertations & theses'],
            'rft.title': ['Rights for the Voiceless: The State, Civil Society and Primary Education in Rural India'],
            'rft_id': ['info:doi/'],
            'rft_val_fmt': ['info:ofi/fmt:kev:mtx:dissertation']
        }
        b = bib_from_qdict(request)
        ourl = openurl_from_bib(b)
        parsed_ourl = cgi.parse_qs(ourl)
        self.assertTrue('dissertation' in parsed_ourl.get('rft.genre'))
        self.assertTrue('Rights for the Voiceless' in parsed_ourl.get('rft.title')[0])
        self.assertTrue('Mangla, Akshay') in parsed_ourl.get('rft.au')
        self.assertTrue('2013' in parsed_ourl.get('rft.date'))

    ## end class TestToOpenURL()
