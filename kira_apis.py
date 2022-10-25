import streamlit as st
from helper_functions import *
from spacy import displacy
import requests
import os
import json
import requests, zipfile, io



def get_template_id(url):
    response = requests.get(url=url,
                            headers={'Connection': 'close',
                                     'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                   '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                   'Safari/537.36.',
                                     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
                                     }
                            )
    return json.loads(response.content)[0]['template_id']

def get_doc_location(url, template_id):
    data = {
        "pdf_quality": "medium",
        "include_highlight": False,
        "template_ids": [
            template_id
        ]
    }
    response = requests.post(
        url=url,
        headers={'Connection': 'close',
                 'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                               'Safari/537.36.',
                 "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
                 },
        json=data,
        stream=False
        )
    return response.headers['content-location']

def get_redirect_link(url):
    print("---------url inside get_redirect_link---", url)
    response = requests.get(url=url,
                             headers={'Connection': 'close',
                                      'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                    '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                    'Safari/537.36.',
                                      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
                                      },

                             stream=False
                             )
    return json.loads(response.text)




def get_doc(url, doc_id):
    print("inside get_doc")
    file = url.split('/')[-2]
    url = url + "/" + file
    print("Created URL :", url)
    r = requests.get(url=url,
                     headers={'Connection': 'close',
                              'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                            '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                            'Safari/537.36.',
                              "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
                              })
    print("Ran the response")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("Got the zipped file")
    z.extractall(os.path.join("downloaded_file", doc_id))
    print("Written the file")


# def get_doc_metadate(url):
#     r = requests.get(url=url,
#                      headers={'Connection': 'close',
#                               'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
#                                             '(KHTML, like Gecko) Chrome/51.0.2704.103 '
#                                             'Safari/537.36.',
#                               "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
#                               })
#     return json.loads(r.text)

def get_smartfld(url):
    print("inside smartfld")
    response = requests.get(url=url,
                            headers={'Connection': 'close',
                                     'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                   '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                   'Safari/537.36.',
                                     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzIjoiK09mSHFjbG1KTXdxWHJja04wS1NleVJFN0h5WVp3eVdvQ25SSjZSVXpkWG80MFRRL1ZHcHB6RHdYd25DaWVQZyIsImYiOjIsInYiOjJ9.Cs1tkRJLDQQAwR8WSBuIVXYa19Vo1y6BtcUb-ThzGVE"
                                     }
                            )

    return json.loads(response.text)





