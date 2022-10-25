import fitz
import pandas as pd
import re
import string
from nltk.corpus import stopwords


def process_file(path):
    #from PyPDF2 import PdfFileReader
    #input_file = PdfFileReader(open(path, 'rb'))
    doc = fitz.open(path)
    total_content_raw = []
    total_content_lower = []
    page_number = []
    whole_text = ''
    for page in doc:  # iterate the document pages

        # text = page.getText().encode("utf8")  # get plain text (is in UTF-8)
        text = page.get_text().encode("utf8")
        # text1 = page.getText('text')
        text1 = page.get_text('text')
        whole_text = whole_text + text1
        res = text1.split('.\n \n')
        con = [i for i in text1.split('.\n \n')]
        # return concatenated content
        total_content_raw.extend(con)
        total_content_lower.extend([i.lower() for i in con])
        page_number.extend([str(page.number + 1)] * len(con))
    df = pd.DataFrame({'text_raw': total_content_raw, 'text_lower': total_content_lower, 'page_number': page_number})
    #df = pd.DataFrame({'text_raw': total_content_raw, 'text_lower': total_content_lower})
    return df, whole_text


def matcher(df, keyword):
    def _helper_matcher(row, keyword):
        iter = re.finditer(keyword, row, re.IGNORECASE)
        locations = [m.span() for m in iter]
        if locations:
            return True, locations
        else:
            return False, None

    df['output'] = df.text_raw.apply(lambda row: _helper_matcher(row, keyword))
    mask_df = df['output'].apply(lambda row: pd.Series(row))
    mask_df.columns = ['is_present', 'location']
    final_df = pd.concat([df.drop(columns=['output'], axis=0), mask_df], axis=1)
    final_df = final_df[final_df['is_present']]
    final_df['text_raw'] = final_df['text_raw'].str.replace("\n \n", "\n").str.strip()
    final_df['Smart Field Name'] = keyword
    return final_df

def remove_non_alphabet(text):
    # compile regex
    try:
        punc = string.punctuation + '“' + '”'
        text = text.translate(str.maketrans('', '', punc))
        return text
    except:
        return None


def remove_urls(text):
    # compile regex
    #try:
    url_re = re.compile('(https://+.\S*)')
    text = url_re.sub('', text).strip()
    return text
    # except:
    #     return None


def remove_stop_words(text):
    """take a word and check it against the common stop words list from NLTK"""
    try:
        stops = set(stopwords.words("english"))
        text = ' '.join([word.lower() for word in text.split() if word.lower() not in stops])
        return text
    except:
        return None

def read_in_kira_output(filename):
    if 'csv' in filename:
        kira_op = pd.read_csv(filename)
    elif 'xlsx' in filename:
        kira_op = pd.read_excel(filename, sheet_name=1)
    return kira_op