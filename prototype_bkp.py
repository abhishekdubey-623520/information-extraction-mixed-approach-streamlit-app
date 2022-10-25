import streamlit as st
from helper_functions import *
from kira_apis import sf
from spacy import displacy
from io import StringIO

# uploaded_file = st.file_uploader("Choose a file")
# with open(uploaded_file.name, mode='wb') as w:
#     w.write(uploaded_file.getvalue())

# read the file
# df, text = process_file("Project Alta - Stock Purchase Agreement, 4864-5916-2134_10.pdf")
#
# # read KIRA
#
#
# df['text_clean'] = df['text_raw'].map(lambda row: remove_non_alphabet(row))
# df['text_clean'] = df['text_clean'].map(lambda row: remove_urls(row))
# df['text_clean'] = df['text_clean'].map(lambda row: remove_stop_words(row))
# print("===0====",df.head())
# complete_text = " ".join(df['text_clean'].tolist())
#
#
#
#
# def _helper_matcher(row, keyword):
#     iter = re.finditer(keyword, row, re.IGNORECASE)
#     locations = [m.span() for m in iter]
#     if locations:
#         return True, locations
#     else:
#         return False, None
# t = []
# sm_fl = []
# for elem in sf:
#     t.append(elem['text'])
#     sm_fl.append(elem['field_name'])
# kira_op = pd.DataFrame({'Result_raw':t, 'Result':t, 'Smart Field Nam':sm_fl})
# # kira_op.reset_index(drop=True, inplace=True)
# # kira_op.columns = ['Result']
# print("===1====",kira_op.head())
# kira_op['Result_clean'] = kira_op['Result'].map(lambda row : remove_non_alphabet(row))
# kira_op['Result_clean'] = kira_op['Result_clean'].map(lambda row: remove_urls(row))
# kira_op['Result_clean'] = kira_op['Result_clean'].map(lambda row: remove_stop_words(row))
#
#
#
#

# smart_field_list = ["*ed to be conducted", "Leakage", "after the closing", "adequate reserves"]
# # smart_field_list = {"adequate reserves":{'exclude_if_present':["Permitted Encumbrances", "Permitted Lien"]}}
#
# for sf in smart_field_list:
#     if "*" in sf:
#         _ = sf.replace("*", "\w*")
#         i = smart_field_list.index(sf)
#         smart_field_list.pop(i)
#         smart_field_list.insert(i, _)
#
#
#
# total_matched_df = pd.DataFrame()
# for sf in smart_field_list:
#     matched_df = matcher(df.copy(), sf)
#     total_matched_df = pd.concat([total_matched_df, matched_df])
# print("=====3=====", total_matched_df.columns)
# # if uploaded_file is not None:
# #     # To read file as bytes:
# #     # bytes_data = uploaded_file.getvalue()
# #     # st.write(bytes_data)
# #
# #     # # To convert to a string based IO:
# #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
# #     # st.write(stringio)
# #
# #     # To read file as string:
# #     string_data = stringio.read()
# #     st.write(string_data)

f = open('raw_text.txt', 'r')
raw_text = f.read()
f.close()

from kira_apis import sf
import pandas as pd
import re




import itertools
def flatten_send_min_max(row):
    return min(list(itertools.chain(*sf[:10][2]['text_ranges']))), max(list(itertools.chain(*sf[:10][2]['text_ranges'])))


t = []
sm_fl = []
text_range = []
for elem in sf:
    t.append(elem['text'])
    sm_fl.append(elem['field_name'])
    text_range.append(elem['text_ranges'])


kira_op = pd.DataFrame({'Result_raw':t, 'Result':t, 'Smart Field Nam':sm_fl, 'text_range':text_range})
kira_op['Result_raw'] = kira_op['Result_raw'].apply(lambda row : row.replace(")", " ").replace("(", " "))
kira_op['text_st_end'] = kira_op.text_range.apply(lambda row : [min(list(itertools.chain(*row))), max(list(itertools.chain(*row)))] )
kira_op['pattern'] = kira_op.Result_raw.apply(lambda row : """[^a-z]*""".join(row.split()))


def kira_matcher(row):
    try:
        #exp = f'{clean_text[row[0] : row[1]].strip().split()[0]}.*{clean_text[row[0] : row[1]].strip().split()[-1]}[^\s]+'
        iter = re.finditer(row, raw_text.replace(")", " ").replace("(", " "), re.IGNORECASE)
        locations = [m.span() for m in iter]
        if locations:
            return [locations[0][0] , locations[0][1]]
    except:
#         print(row)
        return None

kira_op['location'] = kira_op.pattern.apply(lambda row : kira_matcher(row))

ko = kira_op[~kira_op.location.isna()][['Smart Field Nam','location']].sort_values(by=['location'])


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


#colors = {"ORG": "linear-gradient(90deg, #aa9cfc, #fc9ce7)"}
# colors = {"ORG": "red", "PERSON" : '#7aecec', "TEST":'yellow', 'TEST1':'pink'}
# options = {"ents": ["ORG", "PERSON", "TEST", "TEST1"], "colors": colors}
options = {'ents' : ent_list, 'colors':colors}
rend = displacy.render(custom, style="ent", manual=True, options=options)

# rendering the raw html to the UI
import streamlit.components.v1 as components
# st.markdown(rend, unsafe_allow_html=True)


import base64

# f = open("temp.txt","w")
# f.write(rend)
# f.close()

# f = open('temp.html', 'w')
# f.write(rend)
# f.close()

# import pdfkit
# pdfkit.from_file('temp.html', 'out.pdf')

# with open("temp.pdf","rb") as f:
# base64_pdf = base64.b64encode(rend).decode('utf-8')
r = bytes(rend, 'utf-8')
print(len(r))
pdf_display = f'<iframe srcdoc={rend} width="1200" height="1200"></iframe>'
#
st.markdown(pdf_display, unsafe_allow_html=True)





