import streamlit as st

import base64
regex_list = ["*ed to be conducted", "Leakage", "after the closing", "adequate reserves"]
doc_id = st.sidebar.text_input('1. Enter document ID: ')
col_selected = st.sidebar.multiselect('2. Select one or more regex', regex_list, help='')

with open("temp.pdf","rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
f.close()
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
#
st.markdown(pdf_display, unsafe_allow_html=True)
import streamlit.components.v1 as components  # Import Streamlit

# Render the h1 block, contained in a frame of size 200x200.
# pdf_display = f'<iframe src="data:application/html;charset=utf-8,%3Chtml%3E%3Cbody%3Efoo%3C/body%3E%3C/html%3E" width="800" height="800" type="application/html"></iframe>'
# st.markdown(pdf_display, unsafe_allow_html=True)
