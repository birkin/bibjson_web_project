### about

This is a lightweight [django](https://www.djangoproject.com) app that provides an api to convert an [openurl](https://en.wikipedia.org/wiki/OpenURL) to [bibjson](http://okfnlabs.org/projects/bibjson/), and to convert bibjson to an openurl.

- in a nutshell, openurl: _"OpenURL is a standardized format for encoding a description of a resource within a ... URL..."_ (excerpted from the above openurl link)

- in a nutshell, bibjson: _"BibJSON is a convention for representing bibliographic metadata in JSON..."_ (excerpted from the above bibjson link)

- django is a python webapp framework; this project is lightweight in the sense that it doesn't use or require a database or templating.

---


### openurl-to-bibjson usage

- python example request

        # -*- coding: utf-8 -*-

        import requests  # http://docs.python-requests.org/en/master/


        raw_openurl = '''issn=1175-5652&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/firstsearch.oclc.org:MEDLINE&req_dat=<sessionid>0</sessionid>&pid=<accession number>678061209</accession number><fssessid>0</fssessid>&rft.date=2010&volume=8&date=2010&rft.volume=8&rfe_dat=<accessionnumber>678061209</accessionnumber>&url_ver=Z39.88-2004&atitle=The missing technology: an international comparison of human capital investment in healthcare.&genre=article&epage=71&spage=361&id=doi:&rft.spage=361&rft.sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&aulast=Frogner&rft.issue=6&rft.epage=71&rft.jtitle=Applied health economics and health policy&rft.aulast=Frogner&title=Applied health economics and health policy&rft.aufirst=BK&rft_id=urn:ISSN:1175-5652&sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&sid=FirstSearch:MEDLINE&rft.atitle=The missing technology: an international comparison of human capital investment in healthcare.&issue=6&rft.issn=1175-5652&rft.genre=article&aufirst=BK'''

        payload = { 'ourl': raw_openurl }
        r = requests.get('http://127.0.0.1/bib_ourl_api/v1/ourl_to_bib/', params=payload)

        ## note: requests automatically properly encodes the openurl -- this encoding step is important ##

- the output, via `print( r.content )`

        b'{
          "query": {
            "date_time": "2017-11-10 13:46:49.137818",
            "url": "https://plibwwwcit.services.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=ctx_ver%253DZ39.88-2004%2526rft_val_fmt%253Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Ajournal%2526rft.atitle%253DThe%2520missing%2520technology%253A%2520an%2520international%2520comparison%2520of%2520human%2520capital%2520investment%2520in%2520healthcare.%2526rft.jtitle%253DApplied%2520health%2520economics%2520and%2520health%2520policy%2526rft.genre%253Darticle%2526rfr_id%253Dinfo%253Asid%252Finfo%253Asid%252Ffirstsearch.oclc.org%253AMEDLINE%2526rft.date%253D2010%2526rft.au%253DFrogner%252C%2520BK%2526rft.volume%253D8%2526rft.issue%253D6%2526rft.spage%253D361%2526rft.end_page%253D71%2526rft.pages%253D361%2520-%252071%2526rft.issn%253D1175-5652%2526rft_id%253Dhttp%253A%252F%252Fwww.worldcat.org%252Foclc%252F678061209"
          },
          "response": {
            "bib": {
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
            },
            "elapsed_time": "0:00:00.007019"
          }
        }'

---

### bibjson-to-openurl usage

- python example request

        # -*- coding: utf-8 -*-

        import requests  # http://docs.python-requests.org/en/master/


        raw_bibjson = '''{
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

        payload = { 'bibjson': raw_bibjson }

        r = requests.get('http://127.0.0.1/bib_ourl_api/v1/bib_to_ourl/', params=payload)

        ## note: requests automatically properly encodes the bibjson -- this encoding step is important ##

- the output, via `print( r.content )`

        # b'{
        #   "query": {
        #     "date_time": "2017-11-14 16:39:28.548453",
        #     "url": "http://127.0.0.1/bib_ourl_api/v1/bib_to_ourl/?bibjson=%7B%0A++%22_rfr%22%3A+%22info%3Asid%2Ffirstsearch.oclc.org%3AMEDLINE%22%2C%0A++%22author%22%3A+%5B%0A++++%7B%0A++++++%22firstname%22%3A+%22BK%22%2C%0A++++++%22lastname%22%3A+%22Frogner%22%2C%0A++++++%22name%22%3A+%22Frogner%2C+BK%22%0A++++%7D%0A++%5D%2C%0A++%22end_page%22%3A+%2271%22%2C%0A++%22identifier%22%3A+%5B%0A++++%7B%0A++++++%22id%22%3A+%221175-5652%22%2C%0A++++++%22type%22%3A+%22issn%22%0A++++%7D%2C%0A++++%7B%0A++++++%22id%22%3A+%22678061209%22%2C%0A++++++%22type%22%3A+%22oclc%22%0A++++%7D%0A++%5D%2C%0A++%22issue%22%3A+%226%22%2C%0A++%22journal%22%3A+%7B%0A++++%22name%22%3A+%22Applied+health+economics+and+health+policy%22%0A++%7D%2C%0A++%22pages%22%3A+%22361+-+71%22%2C%0A++%22place_of_publication%22%3A+null%2C%0A++%22publisher%22%3A+null%2C%0A++%22start_page%22%3A+%22361%22%2C%0A++%22title%22%3A+%22The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.%22%2C%0A++%22type%22%3A+%22article%22%2C%0A++%22volume%22%3A+%228%22%2C%0A++%22year%22%3A+%222010%22%0A%7D"
        #   },
        #   "response": {
        #     "decoded_bibjson": "{\
        #   \\"_rfr\\": \\"info:sid/firstsearch.oclc.org:MEDLINE\\",\
        #   \\"author\\": [\
        #     {\
        #       \\"firstname\\": \\"BK\\",\
        #       \\"lastname\\": \\"Frogner\\",\
        #       \\"name\\": \\"Frogner, BK\\"\
        #     }\
        #   ],\
        #   \\"end_page\\": \\"71\\",\
        #   \\"identifier\\": [\
        #     {\
        #       \\"id\\": \\"1175-5652\\",\
        #       \\"type\\": \\"issn\\"\
        #     },\
        #     {\
        #       \\"id\\": \\"678061209\\",\
        #       \\"type\\": \\"oclc\\"\
        #     }\
        #   ],\
        #   \\"issue\\": \\"6\\",\
        #   \\"journal\\": {\
        #     \\"name\\": \\"Applied health economics and health policy\\"\
        #   },\
        #   \\"pages\\": \\"361 - 71\\",\
        #   \\"place_of_publication\\": null,\
        #   \\"publisher\\": null,\
        #   \\"start_page\\": \\"361\\",\
        #   \\"title\\": \\"The missing technology: an international comparison of human capital investment in healthcare.\\",\
        #   \\"type\\": \\"article\\",\
        #   \\"volume\\": \\"8\\",\
        #   \\"year\\": \\"2010\\"\
        # }",
        #     "elapsed_time": "0:00:00.006185",
        #     "openurl": "ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Ajournal&rft.atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&rft.jtitle=Applied+health+economics+and+health+policy&rft.genre=article&rfr_id=info%3Asid/info%3Asid/firstsearch.oclc.org%3AMEDLINE&rft.date=2010&rft.au=Frogner%2C+BK&rft.volume=8&rft.issue=6&rft.spage=361&rft.end_page=71&rft.pages=361+-+71&rft.issn=1175-5652&rft_id=http%3A//www.worldcat.org/oclc/678061209"
        #   }
        # }'

    - TODO: format as 'query'/'response' as for openurl-to-bib


---


### notes

- not reflected in this commit history is that this project is a speck on the shoulders of the great work done by [Ted Lawless](https://github.com/lawlesst) who created the [original bibjsontools](https://github.com/lawlesst/bibjsontools).

- code contact: birkin_diana@brown.edu

---
