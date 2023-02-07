import re

def _helper_matcher(row, keyword):
    iter = re.finditer(keyword, row, re.IGNORECASE)
    locations = [m.span() for m in iter]
    if locations:
        #print("----------------", row[locations[0][0]])
        return True, locations
    else:
        return False, None


def bookmark_dict(bookmark_list, reader):
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # recursive call
            result.update(bookmark_dict(item))
        else:
            result[reader.getDestinationPageNumber(item)] = item.title
    return result





