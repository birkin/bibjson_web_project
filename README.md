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
            "ourl": "issn=1175-5652&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/firstsearch.oclc.org:MEDLINE&req_dat=<sessionid>0</sessionid>&pid=<accession number>678061209</accession number><fssessid>0</fssessid>&rft.date=2010&volume=8&date=2010&rft.volume=8&rfe_dat=<accessionnumber>678061209</accessionnumber>&url_ver=Z39.88-2004&atitle=The missing technology: an international comparison of human capital investment in healthcare.&genre=article&epage=71&spage=361&id=doi:&rft.spage=361&rft.sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&aulast=Frogner&rft.issue=6&rft.epage=71&rft.jtitle=Applied health economics and health policy&rft.aulast=Frogner&title=Applied health economics and health policy&rft.aufirst=BK&rft_id=urn:ISSN:1175-5652&sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&sid=FirstSearch:MEDLINE&rft.atitle=The missing technology: an international comparison of human capital investment in healthcare.&issue=6&rft.issn=1175-5652&rft.genre=article&aufirst=BK"
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
        #   "ourl": "ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Ajournal&rft.atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&rft.jtitle=Applied+health+economics+and+health+policy&rft.genre=article&rfr_id=info%3Asid/info%3Asid/firstsearch.oclc.org%3AMEDLINE&rft.date=2010&rft.au=Frogner%2C+BK&rft.volume=8&rft.issue=6&rft.spage=361&rft.end_page=71&rft.pages=361+-+71&rft.issn=1175-5652&rft_id=http%3A//www.worldcat.org/oclc/678061209"
        # }'

    - TODO: format as 'query'/'response' as for openurl-to-bib


---


### notes

- not reflected in this commit history is that this project is a speck on the shoulders of the great work done by [Ted Lawless](https://github.com/lawlesst) who created the [original bibjsontools](https://github.com/lawlesst/bibjsontools).

- code contact: birkin_diana@brown.edu

---
