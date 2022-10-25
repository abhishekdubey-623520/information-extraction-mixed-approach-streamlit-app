import pandas as pd
import re

def kira_proc_exec(raw_text, sf):
    import itertools
    def flatten_send_min_max(row):
        return min(list(itertools.chain(*sf[:10][2]['text_ranges']))), max(
            list(itertools.chain(*sf[:10][2]['text_ranges'])))

    t = []
    sm_fl = []
    text_range = []
    for elem in sf:
        t.append(elem['text'])
        sm_fl.append(elem['field_name'])
        text_range.append(elem['text_ranges'])

    kira_op = pd.DataFrame({'Result_raw': t, 'Result': t, 'Smart Field Nam': sm_fl, 'text_range': text_range})
    kira_op['Result_raw'] = kira_op['Result_raw'].apply(lambda row: row.replace(")", " ").replace("(", " "))
    kira_op['text_st_end'] = kira_op.text_range.apply(
        lambda row: [min(list(itertools.chain(*row))), max(list(itertools.chain(*row)))])
    kira_op['pattern'] = kira_op.Result_raw.apply(lambda row: """[^a-z]*""".join(row.split()))
    print("Kira file created")

    def kira_matcher(row):
        try:
            # exp = f'{clean_text[row[0] : row[1]].strip().split()[0]}.*{clean_text[row[0] : row[1]].strip().split()[-1]}[^\s]+'
            iter = re.finditer(row, raw_text.replace(")", " ").replace("(", " "), re.IGNORECASE)
            locations = [m.span() for m in iter]
            if locations:
                return [locations[0][0], locations[0][1]]
        except:
            #         print(row)
            return None

    kira_op['location'] = kira_op.pattern.apply(lambda row: kira_matcher(row))
    print("Kira processing done")
    ko = kira_op[~kira_op.location.isna()][['Smart Field Nam', 'location']].sort_values(by=['location'])
    return ko