import streamlit as st
from helper_functions import *
from spacy import displacy
import requests
import json
import requests, zipfile, io
import os
from kira_proc import kira_proc_exec
from kira_apis import *
st.write("Starting the code")

regex_list = ["*ed to be conducted", "Leakage", "after the closing", "adequate reserves"]
doc_id = st.sidebar.text_input('1. Enter document ID: ')
col_selected = st.sidebar.multiselect('2. Select one or more regex', regex_list, help='')


def flag_to_run():
    st.session_state.run = True


st.sidebar.button('3. Run', help='', on_click=flag_to_run)


print("doc_id---------", doc_id,st.session_state.run)
# get the doc

# fetch template id  : /documents/{did}/templates
# doc_metadata = get_doc_metadate()
if doc_id:
    base_url = 'https://us.cc.app.kirasystems.com/platform-api/v1/documents'
    temp_id = get_template_id(f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/{doc_id}/templates')
    print("################## 1 ##################", temp_id)
    file_loc = get_doc_location(url=f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/export?export_format=pdf&document_ids={doc_id}',
                                template_id=temp_id)
    print("################### 2 #######################", file_loc)

    while True:
        response = get_redirect_link(file_loc)
        if 'redirect_href' in response:
            print("Gonna come out of While")
            break
        else:
            import time
            print("Waiting 30 seconds")
            time.sleep(40)
            continue

    print("################### 3 #######################", response['redirect_href'])
    get_doc(response['redirect_href'], doc_id)
    sf = get_smartfld(url=f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/{doc_id}/field-instances')
    print("=====4====== ", sf[:2])
    print("The api calls have finished")

    # reading the file and create the df
    file_name = os.listdir(os.path.join("downloaded_file", doc_id))[0]
    df, raw_text = process_file(os.path.join("downloaded_file", doc_id, file_name))

    # create the kira_op
    ko = kira_proc_exec(raw_text, sf)

    ent = []
    colors = {}
    ent_list = []
    for i,v in ko.iterrows():
        ent.append({'start': v['location'][0],
                    'end': v['location'][1],
                    'label': v['Smart Field Nam']
                   })
        colors[v['Smart Field Nam']] = 'yellow'
        ent_list.append(v['Smart Field Nam'])


    custom = {
        "text": raw_text,
        "ents": ent,
        "title": None
    }
    st.write("All processing done")
    options = {'ents' : ent_list, 'colors':colors}
    rend = displacy.render(custom, style="ent", manual=True, options=options)
    st.markdown(rend, unsafe_allow_html=True)