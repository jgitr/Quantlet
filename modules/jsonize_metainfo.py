# Convert Metainfo.txt to json
import re
import json

# Strip leading and trailing whitespace, linebreak
# This is where further cleaning statements must be applied
def clean_string(_str):
    """
    _str: list of strings
    returns cleaned list of strings
    """
    if isinstance(_str, list):
        return list(map(lambda x: re.sub(r"[\n]*", "", x.strip()), _str))
    elif isinstance(_str, str):
        return re.sub(r"[\n]*", "", _str.strip())
    else:
        raise ValueError('Input is neither string nor list')


def jsonize(meta, fname, out_dir = 'data/metainfo_json/'):
    """
    meta: like q.quantlets['ADM/HermPolyPlot/Metainfo.txt'].metainfo_undebugged
    Example q: "\nName of QuantLet : HermPolyPlot\n\nPublished in : ADM\n\nDescription : 'Plots the first 4 Hermite polynomials on the given grid of \nvalues, probabilistic version.'\n\nKeywords : 'basis, orthogonal series, graphical representation, probability, \ngraphical representation, plot'\n\nSee also : hermitepoly\n\nAuthor : Sergey Nasekin, Katerina Papagiannouli\n\nSubmitted : \n\nExample : Plot of the first 4 Hermite polynomials\n"
    
    fname: target JSON filename, without .JSON extension
    """

    # Define Keys for Output JSON
    target_keys = ['Name of QuantLet', 'Published in', 'Description', 'Keywords', 'See also', 'Author', 'Submitted', 'Example']

    # Split by linebreak
    out = {}
    raw_target_string   = meta.split('\n\n')
    target_string       = clean_string(raw_target_string)

    # Iterate over Substrings split by linebreak. 
    # Add to output dictionary if they are in the Keywords and add the following Substring as Value
    for i in range(len(target_string)):
        # Split each line by ':'
        raw_key, raw_value = target_string[i].split(':')
        key = clean_string(raw_key)
        value = clean_string(raw_value)

        if key in target_keys:
            print('key in target keys!')
            #value = target_string[j]
            out[key] = value
            print('key: ', key)
            print('value :', value)

    out_fname = out_dir + str(fname) + '.json'
    print('Writing ', out_fname)
    with open(out_fname, 'w') as fp:
        json.dump(out, fp)

    return True

def jsonize_all_metainfos(q):
    # Run for all Quantlets
    for key, value in q.quantlets.items():
        print(key)
        meta = q.quantlets[key].metainfo_undebugged
        fname = key.split('.txt')[0]
        fname = '-'.join(fname.split('/'))
        jsonize(meta, fname)

        return True