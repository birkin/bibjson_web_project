### on this page

- about
- openurl-to-bibjson usage
- bibjson-to-openurl usage
- notes

---


### about

This is a lightweight [django](https://www.djangoproject.com) app that provides an api to convert an [openurl](https://en.wikipedia.org/wiki/OpenURL) to [bibjson](http://okfnlabs.org/projects/bibjson/), and to convert bibjson to an openurl.

- in a nutshell, openurl: _"OpenURL is a standardized format for encoding a description of a resource within a ... URL..."_ (excerpted from the above openurl link)

- in a nutshell, bibjson: _"BibJSON is a convention for representing bibliographic metadata in JSON..."_ (excerpted from the above bibjson link)

- django is a python webapp framework; this project is lightweight in the sense that it doesn't use or require a database or templating.

---


### openurl-to-bibjson usage

- python example request:

        # -*- coding: utf-8 -*-

        import requests  # http://docs.python-requests.org/en/master/

        raw_openurl = '''issn=1175-5652&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/firstsearch.oclc.org:MEDLINE&req_dat=<sessionid>0</sessionid>&pid=<accession number>678061209</accession number><fssessid>0</fssessid>&rft.date=2010&volume=8&date=2010&rft.volume=8&rfe_dat=<accessionnumber>678061209</accessionnumber>&url_ver=Z39.88-2004&atitle=The missing technology: an international comparison of human capital investment in healthcare.&genre=article&epage=71&spage=361&id=doi:&rft.spage=361&rft.sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&aulast=Frogner&rft.issue=6&rft.epage=71&rft.jtitle=Applied health economics and health policy&rft.aulast=Frogner&title=Applied health economics and health policy&rft.aufirst=BK&rft_id=urn:ISSN:1175-5652&sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&sid=FirstSearch:MEDLINE&rft.atitle=The missing technology: an international comparison of human capital investment in healthcare.&issue=6&rft.issn=1175-5652&rft.genre=article&aufirst=BK'''

        payload = { 'ourl': raw_openurl }
        r = requests.get('http://127.0.0.1/bib_ourl_api/v1/ourl_to_bib/', params=payload)

        ## note: requests automatically properly encodes the openurl -- this encoding step is important ##

- the returned json:

        {
          "query": {
            "date_time": "2017-11-15 17:05:08.414930",
            "url": "http://127.0.0.1/bib_ourl_api/v1/ourl_to_bib/?ourl=issn%3D1175-5652%26rft_val_fmt%3Dinfo%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal%26rfr_id%3Dinfo%3Asid%2Ffirstsearch.oclc.org%3AMEDLINE%26req_dat%3D%3Csessionid%3E0%3C%2Fsessionid%3E%26pid%3D%3Caccession%20number%3E678061209%3C%2Faccession%20number%3E%3Cfssessid%3E0%3C%2Ffssessid%3E%26rft.date%3D2010%26volume%3D8%26date%3D2010%26rft.volume%3D8%26rfe_dat%3D%3Caccessionnumber%3E678061209%3C%2Faccessionnumber%3E%26url_ver%3DZ39.88-2004%26atitle%3DThe%20missing%20technology%3A%20an%20international%20comparison%20of%20human%20capital%20investment%20in%20healthcare.%26genre%3Darticle%26epage%3D71%26spage%3D361%26id%3Ddoi%3A%26rft.spage%3D361%26rft.sici%3D1175-5652(2010)8%3A6%3C361%3ATMTAIC%3E2.0.TX%3B2-O%26aulast%3DFrogner%26rft.issue%3D6%26rft.epage%3D71%26rft.jtitle%3DApplied%20health%20economics%20and%20health%20policy%26rft.aulast%3DFrogner%26title%3DApplied%20health%20economics%20and%20health%20policy%26rft.aufirst%3DBK%26rft_id%3Durn%3AISSN%3A1175-5652%26sici%3D1175-5652(2010)8%3A6%3C361%3ATMTAIC%3E2.0.TX%3B2-O%26sid%3DFirstSearch%3AMEDLINE%26rft.atitle%3DThe%20missing%20technology%3A%20an%20international%20comparison%20of%20human%20capital%20investment%20in%20healthcare.%26issue%3D6%26rft.issn%3D1175-5652%26rft.genre%3Darticle%26aufirst%3DBK"
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
            "decoded_openurl": "issn=1175-5652&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/firstsearch.oclc.org:MEDLINE&req_dat=<sessionid>0</sessionid>&pid=<accession number>678061209</accession number><fssessid>0</fssessid>&rft.date=2010&volume=8&date=2010&rft.volume=8&rfe_dat=<accessionnumber>678061209</accessionnumber>&url_ver=Z39.88-2004&atitle=The missing technology: an international comparison of human capital investment in healthcare.&genre=article&epage=71&spage=361&id=doi:&rft.spage=361&rft.sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&aulast=Frogner&rft.issue=6&rft.epage=71&rft.jtitle=Applied health economics and health policy&rft.aulast=Frogner&title=Applied health economics and health policy&rft.aufirst=BK&rft_id=urn:ISSN:1175-5652&sici=1175-5652(2010)8:6<361:TMTAIC>2.0.TX;2-O&sid=FirstSearch:MEDLINE&rft.atitle=The missing technology: an international comparison of human capital investment in healthcare.&issue=6&rft.issn=1175-5652&rft.genre=article&aufirst=BK",
            "elapsed_time": "0:00:00.006880"
          }
        }

---


### bibjson-to-openurl usage

- python example request:

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

- the returned json:

        {
          "query": {
            "date_time": "2017-11-15 17:10:23.020677",
            "url": "http://127.0.0.1/bib_ourl_api/v1/bib_to_ourl/?bibjson=%7B%20%22_rfr%22%3A%20%22info%3Asid%2Ffirstsearch.oclc.org%3AMEDLINE%22%2C%20%22author%22%3A%20%5B%20%7B%20%22firstname%22%3A%20%22BK%22%2C%20%22lastname%22%3A%20%22Frogner%22%2C%20%22name%22%3A%20%22Frogner%2C%20BK%22%20%7D%20%5D%2C%20%22end_page%22%3A%20%2271%22%2C%20%22identifier%22%3A%20%5B%20%7B%20%22id%22%3A%20%221175-5652%22%2C%20%22type%22%3A%20%22issn%22%20%7D%2C%20%7B%20%22id%22%3A%20%22678061209%22%2C%20%22type%22%3A%20%22oclc%22%20%7D%20%5D%2C%20%22issue%22%3A%20%226%22%2C%20%22journal%22%3A%20%7B%20%22name%22%3A%20%22Applied%20health%20economics%20and%20health%20policy%22%20%7D%2C%20%22pages%22%3A%20%22361%20-%2071%22%2C%20%22place_of_publication%22%3A%20null%2C%20%22publisher%22%3A%20null%2C%20%22start_page%22%3A%20%22361%22%2C%20%22title%22%3A%20%22The%20missing%20technology%3A%20an%20international%20comparison%20of%20human%20capital%20investment%20in%20healthcare.%22%2C%20%22type%22%3A%20%22article%22%2C%20%22volume%22%3A%20%228%22%2C%20%22year%22%3A%20%222010%22%20%7D"
          },
          "response": {
            "decoded_bibjson": "{ \"_rfr\": \"info:sid/firstsearch.oclc.org:MEDLINE\", \"author\": [ { \"firstname\": \"BK\", \"lastname\": \"Frogner\", \"name\": \"Frogner, BK\" } ], \"end_page\": \"71\", \"identifier\": [ { \"id\": \"1175-5652\", \"type\": \"issn\" }, { \"id\": \"678061209\", \"type\": \"oclc\" } ], \"issue\": \"6\", \"journal\": { \"name\": \"Applied health economics and health policy\" }, \"pages\": \"361 - 71\", \"place_of_publication\": null, \"publisher\": null, \"start_page\": \"361\", \"title\": \"The missing technology: an international comparison of human capital investment in healthcare.\", \"type\": \"article\", \"volume\": \"8\", \"year\": \"2010\" }",
            "elapsed_time": "0:00:00.005927",
            "openurl": "ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Ajournal&rft.atitle=The+missing+technology%3A+an+international+comparison+of+human+capital+investment+in+healthcare.&rft.jtitle=Applied+health+economics+and+health+policy&rft.genre=article&rfr_id=info%3Asid/info%3Asid/firstsearch.oclc.org%3AMEDLINE&rft.date=2010&rft.au=Frogner%2C+BK&rft.volume=8&rft.issue=6&rft.spage=361&rft.end_page=71&rft.pages=361+-+71&rft.issn=1175-5652&rft_id=http%3A//www.worldcat.org/oclc/678061209"
          }
        }


---


### notes

- not reflected in this commit history is that this project is a speck on the shoulders of the great work done by [Ted Lawless](https://github.com/lawlesst) who created the [original bibjsontools](https://github.com/lawlesst/bibjsontools).

- code contact: birkin_diana@brown.edu

---
