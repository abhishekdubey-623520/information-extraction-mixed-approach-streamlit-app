import streamlit as st
from helper_functions import *
import requests
import os
import json
import requests, zipfile, io



def get_template_id(url=None, token=None):
    response = requests.get(url=url,
                            headers={'Connection': 'close',
                                     'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                   '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                   'Safari/537.36.',
                                     "Authorization": token
                                     }
                            )
    try:
        return json.loads(response.content)[0]['template_id']
    except:
        print("Invalid doc id")
        return 99999

def get_doc_location(url=None, template_id=None, token=None):
    data = {
        "pdf_quality": "medium",
        "include_highlight": True,
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
                 "Authorization": token
                 },
        json=data,
        stream=False
        )
    return response.headers['content-location']

def get_redirect_link(url=None, token=None):
    print("---------url inside get_redirect_link---", url)
    response = requests.get(url=url,
                             headers={'Connection': 'close',
                                      'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                    '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                    'Safari/537.36.',
                                      "Authorization": token
                                      },

                             stream=False
                             )
    return json.loads(response.text)




def get_doc(url=None, doc_id=None, token=None):
    print("inside get_doc")
    file = url.split('/')[-2]
    url = url + "/" + file
    print("Created URL :", url)
    r = requests.get(url=url,
                     headers={'Connection': 'close',
                              'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                            '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                            'Safari/537.36.',
                              "Authorization": token
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
#                               "Authorization": token
#                               })
#     return json.loads(r.text)

def get_smartfld(url=None, token=None):
    print("inside smartfld")
    response = requests.get(url=url,
                            headers={'Connection': 'close',
                                     'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                                                   '(KHTML, like Gecko) Chrome/51.0.2704.103 '
                                                   'Safari/537.36.',
                                     "Authorization": token
                                     }
                            )

    return json.loads(response.text)