import requests
import json
from bs4 import BeautifulSoup

url = "https://www.nyu.edu/about/policies-guidelines-compliance/policies-and-guidelines/electronic-data-and-system-risk-classification.html"

def main():

    html = requests.get(url).text

    classification_types = [
        "Data Risk Classification",
        "Data Risk Examples",
        "System Criticality Classification",
        "System Criticality Examples",
    ]

    parser = BeautifulSoup(html, "html.parser")

    all_criteria = []
    for class_type in classification_types:
        all_criteria.append({
            "classification": class_type,
            "criteria": get_critieria_for(parser, class_type)
        })

    # Any other processing of data will occur in another script that uses the output of this script
    print(json.dumps(all_criteria, indent=4))

    pass

def get_critieria_for(parser, classification_type):

    title_name = None
    col_criteria = []

    for tag in parser.findAll():

        if (tag.name == "h3"):
            # only begin parsing if encountered a title that matches the target title
            if (title_name is None and tag.string == classification_type):
                title_name = classification_type
            else:
                title_name = None

        # the first <tr> is the column headers
        if (title_name is not None and tag.name == "tr" and tag.ol is None):
            for (col_index, column_header) in enumerate(tag.findAll(name="td")):
                col_criteria.append(get_criteria_for(column_header))
            pass

    return col_criteria

def get_criteria_for(column_header):
    header_name = column_header.b.string  # i.e. low, moderate, high
    alphanum_only = lambda string : "".join([c for c in string if c.isalnum() or c.isspace()])
    return {
        "classification": header_name,
        "criteria": [alphanum_only(li.get_text()) for li in get_next_row_in_column(column_header).ol if li != "\n"]
    }

def get_next_row_in_column(column_td):
    all_columns = column_td.parent.findAll(name="td")
    column_index = [i for (i, ch) in enumerate(all_columns) if ch is column_td][0]
    next_row = [row for row in column_td.parent.next_siblings if row is not None and row.name == "tr"][0] # row containing criteria
    return next_row.findAll(name="td")[column_index]

'''
Notes on website html structure
as of now (08/15/2019), the structure of the site is essentially:

<h3>Data Risk Classification</h3>
<...>
    <...>
        <h3>{classification type}</h3>
    </...>
    <...>
        <table>
        <td><b>{criteria}</b></td>
        ...
    </table>
    </...>
</...>

Goal: Given header, find associated table
approaches: in-order traversal, the first table found after a header will then be parsed and mapped to that header
note: the findall method executes a pre-order traversal (i.e. parent tag, left -> right tags), however,
-based on the structure of the site, a pre-order traversal will be sufficient
'''

if __name__ == "__main__":
    main()