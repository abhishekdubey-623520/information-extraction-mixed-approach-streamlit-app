import os.path

import streamlit as st
import helper_functions
import shutil
import re
import fitz
import pandas as pd
from kira_apis import *
from PyPDF2 import PdfReader, PdfWriter

st.set_page_config(layout="wide", page_title="Information Extraction Tool",
                       menu_items={"Get Help": "https://www.extremelycoolapp.com/help",
                                   'About': "# This is a header. This is an *extremely* cool app!"})
st.header("Information Extraction Tool")
# st.write("===print all regex ", smart_field_list)
token = f"Bearer {os.environ['KIRA_TOKEN']}"

with st.expander(
                    "ℹ️ -  How it works?",
                    expanded=False):
    st.write("This tool will help you to tag keywords in the documents which were not tagged or trained in KIRA")
# st.info("Sample")
smart_field_list = ["*ed to be conducted", "Leakage", "after the closing", "adequate reserves"]
doc_id = st.sidebar.text_input('1. Enter KIRA document ID: ')


# checking correct doc id or not
if len(doc_id) != 0:
    temp_id = get_template_id(url=f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/{doc_id}/templates', token=token)

    if temp_id == 99999:
        st.warning("Invalid document id!")
        doc_id = False

col_selected = st.sidebar.multiselect('2. Select one or more regex',
                                      ["*ed to be conducted", "Leakage", "after the closing",
                                       "adequate reserves"], help='', default=smart_field_list)
enter_regex = st.sidebar.checkbox('Want to include your own keywords ?')
if enter_regex:
    user_regex = st.sidebar.text_input('Enter your keywords, if more than one use comma as seperator')
    if user_regex:
        smart_field_list.extend([elem.strip() for elem in user_regex.split(',')])

if ("run" not in st.session_state):
    st.session_state.run = False


def flag_to_run():
    st.session_state.run = True


st.sidebar.button('3. Run IET', help='', on_click=flag_to_run)


# modifying the regex smart field
for sf in smart_field_list:
    if "*" in sf:
        _ = sf.replace("*","\w*")
        i = smart_field_list.index(sf)
        smart_field_list.pop(i)
        smart_field_list.insert(i, _)




# token = f"Bearer {os.environ['KIRA_TOKEN']}"
# st.write("=====, ", st.session_state.run, "===", doc_id)




if doc_id and st.session_state.run:
    if os.path.exists("downloaded_file"):
        shutil.rmtree('downloaded_file')
    st.session_state.run = False
    with st.spinner("Fetching the document from KIRA..."):
        base_url = 'https://us.cc.app.kirasystems.com/platform-api/v1/documents'
        # temp_id = get_template_id(url=f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/{doc_id}/templates', token=token)

        #print("################## 1 ################## : Fetched temp_id", temp_id)
        file_loc = get_doc_location(url=f'https://us.cc.app.kirasystems.com/platform-api/v1/documents/export?export_format=pdf&document_ids={doc_id}',
                                    template_id=temp_id, token=token)
        #print("################### 2 ####################### Fetched file location ", file_loc)

        while True:
            response = get_redirect_link(file_loc, token=token)
            if 'redirect_href' in response:
                print("Gonna come out of While loop")
                break
            else:
                import time
                print("Waiting 30 seconds")
                time.sleep(30)
                continue

        #print("################### 3 ####################### downloaded file", response['redirect_href'])
        get_doc(response['redirect_href'], doc_id, token=token)
        st.success('Fetched document from KIRA')


    file_name = os.listdir(os.path.join("downloaded_file", doc_id))[0]
    # uploaded_file = os.path.join(file_path, file_name)
    uploaded_file = os.path.join(os.path.join("downloaded_file", doc_id),
                                 os.listdir(os.path.join("downloaded_file", doc_id))[0])

    with st.spinner("Extracting all the smart-fields from KIRA doc..."):
        content = []
        writer = PdfWriter()
        reader = PdfReader(uploaded_file)
        d = helper_functions.bookmark_dict(reader.getOutlines(), reader)
        #print("################### 4 ####################### parsed the kira bookmarks", d)

        for pg in range(reader.getNumPages()):
            writer.add_page(reader.pages[pg])
            PageObj = reader.getPage(pg)
            content.append(PageObj.extractText())
        #print("################### 5 ####################### read complete content of the doc")
        for k, v in d.items():
            writer.add_bookmark(v, k)
        #print("################### 6 ####################### recreated the kira bookmark in the new doc")
        # Create dataframe out of the pages
        Text = []
        PageNo = []
        for ind, v in enumerate(content):
            con = re.split('\.\s*\n', v)
            Text.extend(con)
            PageNo.extend([ind] * len(con))
        st.success('Document recreated!')

    with st.spinner("Running REGEX and extracting the keywords..."):
        full_sf_df = {}
        found_smart_field = []
        for sf in smart_field_list:
            df = pd.DataFrame({'PageNo': PageNo, 'Text': Text})
            temp = df['Text'].apply(lambda row: helper_functions._helper_matcher(row, '\s+'.join(sf.split()))).apply(pd.Series).rename(
                {0: 'Matched', 1: 'Location'}, axis=1)
            df = pd.concat([df, temp], axis=1)

            full_sf_df[sf] = df
            # Creating book mark for the Keyword
            #print(df[df.Matched]['PageNo'].unique())
            if len(df[df.Matched]['PageNo'].unique()) > 0:
                # if "*" in sf:
                #     print("************finding**********************", df[df.Matched]['keyword'].unique()[0])
                #     #print("$$$$$$$$$$$$$",df[df.Matched]['Location'])
                #     sf = df[df.Matched]['keyword'].unique()[0]
                for i in sorted(list(df[df.Matched]['PageNo'].unique())):
                    writer.add_bookmark(sf, i, color=(255, 0, 0))  # add parent bookmark
                found_smart_field.append(sf)

    # writer.add_bookmark("Introduction", 17, color=(255, 0, 0))  # add parent bookmark
    # writer.add_bookmark("Hello, World", 23, color=(255, 0, 0))

        pdf_out = open(os.path.join('downloaded_file', doc_id, f'processed_{file_name}'), 'wb')
        writer.write(pdf_out)
        pdf_out.close()
        st.success('Ran REGEX and extracted the keywords provided!')

    with st.spinner("Highlighting the doc..."):
        #print("################### 7 ####################### written the processed file")
        my_pdf = fitz.open(os.path.join('downloaded_file', doc_id, f'processed_{file_name}'))
        for sf in found_smart_field:
            if '*ed' in sf:
                sf = ' '.join(sf.split()[-3:])
            my_text = sf
            #print(sf)
            # iterating through pages for highlighting the input phrase
            for n_page in my_pdf:

                matchWords = n_page.search_for(my_text, quads=True)
                #     print("--", matchWords)
                for word in matchWords:
                    my_highlight = n_page.add_highlight_annot(word)
                    my_highlight.update()
                    # my_highlight.setColors(colors={255,192,203}, fill={255,192,203})

            # saving the pdf file as highlighted.pdf
        my_pdf.save(os.path.join('downloaded_file', doc_id, f'highlighted_{file_name}'))
        st.success('Document highlighted!')
    #print("################### 8 ####################### created the highlighted file")
    # Making available for download
    with open(os.path.join('downloaded_file', doc_id, f'highlighted_{file_name}'), 'rb') as f:
        st.download_button('Download file', f, file_name=f'highlighted_{uploaded_file}')
    #print("################### 9 ####################### written the highlighted file")







