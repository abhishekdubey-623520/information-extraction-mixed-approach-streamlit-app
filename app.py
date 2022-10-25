from helper_functions import *

file_name = "Project Alta - Stock Purchase Agreement, 4864-5916-2134_10.pdf"
df, text = process_file(file_name)

kira_op = read_in_kira_output('403956605_29(Titan Commodore - Asset Purchase Agreement (Execution 2022-06-21))_input.xlsx')
kira_op_bkp = kira_op.copy()




df['text_clean'] = df['text_raw'].map(lambda row : remove_non_alphabet(row))
df['text_clean'] = df['text_clean'].map(lambda row: remove_urls(row))
df['text_clean'] = df['text_clean'].map(lambda row: remove_stop_words(row))

complete_text = " ".join(df['text_clean'].tolist())


kira_op['Result_clean'] = kira_op['Result'].map(lambda row : remove_non_alphabet(row))
kira_op['Result_clean'] = kira_op['Result_clean'].map(lambda row: remove_urls(row))
kira_op['Result_clean'] = kira_op['Result_clean'].map(lambda row: remove_stop_words(row))

smart_field_list = ["*ed to be conducted", "Leakage", "after the closing", "adequate reserves"]
# smart_field_list = {"adequate reserves":{'exclude_if_present':["Permitted Encumbrances", "Permitted Lien"]}}

for sf in smart_field_list:
    if "*" in sf:
        _ = sf.replace("*","\w*")
        i = smart_field_list.index(sf)
        smart_field_list.pop(i)
        smart_field_list.insert(i, _)


complete_text_raw = " ".join(df['text_raw'].tolist())