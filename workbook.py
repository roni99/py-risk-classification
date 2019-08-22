import json
import xlsxwriter
from datetime import datetime

def main():
    timestamp_raw = str(datetime.now()).replace(" ", "_").replace(":", "-")
    timestamp = timestamp_raw[:timestamp_raw.find(".")]

    workbook = xlsxwriter.Workbook("output/risk_classification_workbook_" + str(timestamp) + ".xlsx")

    file_classifications = open("classifications.json", "r")
    classifications = json.load(file_classifications)
    file_classifications.close()

    '''
    Edit the for-loop below to change the format of the resulting excel file

    As-is, the loop will create a sheet for every classification (i.e.: Data Risk, System Criticality)
    - and for each level of risk/criticality in that classification, it will list the criteria that defines the level
    '''

    for classification in classifications:
        current_sheet = prepare_sheet_name(classification["classification"]) # first two words in title as name of sheet
        worksheet = workbook.add_worksheet(current_sheet)
        for (col_index, column) in enumerate(classification["criteria"]):
            current_level = column["classification"]
            worksheet.write(0, col_index, current_level)
            for (row_index, criteria) in enumerate(column["criteria"]):
                worksheet.write(row_index + 1, col_index, criteria)
        pass

    workbook.close()

    pass

def prepare_sheet_name(string):
    if (len(string) > 31):
        return string[:28] + "..."
    else:
        return string

if __name__ == "__main__":
    main()
    pass