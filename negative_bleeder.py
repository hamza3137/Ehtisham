#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     08/18/2019

#-------------------------------------------------------------------------------

# This script takes care for negative bleeders in campaign
# Any search term with 8 or more clicks without any sale
import datetime
import xlrd
import xlsxwriter
import sys
import re

if (len(sys.argv) > 1 ):
    configuration_file = __import__(sys.argv[1])
else:
    import config_nexon as configuration_file

ignore_strs_list = ['.','™', 'ō','-','/',',','\'','ģ','%','_','’','|','+','$','ã','‘',\
')','(','\\',':','®','?','º','"',]


def open_excel_for_read(file_location):
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook):
    str_worksheet = workbook.sheet_by_index(0)

    number_rows = str_worksheet.nrows
    number_cols = str_worksheet.ncols

    table = list()
    record = list()

    for x in range(number_rows):
        for y in range(number_cols):
            record.append(str_worksheet.cell(x,y).value)
        table.append (record)
        record = []
        x = x + 1
    return table

def keyword_doesnt_contain_special_chars (keyword):
    ignore = False
    for jj in range(len(ignore_strs_list)):
        if re.findall('\\' + ignore_strs_list[jj],keyword):
            ignore = True
            print (keyword)
            break
    return not ignore

def entry_in_workbook(out_sheet, str_data, row, match_type):

    out_sheet.write (row, 0, str_data[4])
    out_sheet.write (row, 5, str_data[5])
    if match_type == "Negative targeting expression":
        targeting = 'asin="' + str_data[8].upper() + '"'
        out_sheet.write (row, 8, targeting)
        out_sheet.write (row, 9, targeting)
    else:
        out_sheet.write (row, 8, str_data[8])
    out_sheet.write (row, 10, match_type )
    out_sheet.write (row, 13, "Enabled" )
    row = row + 1
    return row

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('str_file_location')

    # Reading rows and columns of audit str sheet
    str_data = read_all_rows_cols(workbook)

    now = datetime.datetime.now()
    temp = configuration_file.FILE_LOCATION['upload_file_location'] + \
    configuration_file.account_name + '_negative_bleeder_' +\
    now.strftime("%m%d%Y") + '_upload.xlsx'
    out_workbook = xlsxwriter.Workbook(temp)


    out_sheet = out_workbook.add_worksheet()
    row = 0

    out_sheet.write (0, 0, "Campaign Name")
    out_sheet.write (0, 1, "Campaign Daily Budget")
    out_sheet.write (0, 2, "Campaign Start Date")
    out_sheet.write (0, 3, "Campaign End Date")
    out_sheet.write (0, 4, "Campaign Targeting Type")
    out_sheet.write (0, 5, "Ad Group Name")
    out_sheet.write (0, 6, "Max Bid")
    out_sheet.write (0, 7, "SKU")
    out_sheet.write (0, 8, "Keyword or Product Targeting")
    out_sheet.write (0, 9, "Product Targeting ID")
    out_sheet.write (0, 10, "Match Type")
    out_sheet.write (0, 11, "Campaign Status")
    out_sheet.write (0, 12, "Ad Group Status")
    out_sheet.write (0, 13, "Status")
    out_sheet.write (0, 14, "Bid+")

    row = row + 1

    for ii in range(len(str_data)):
        if 'white list' not in str_data[ii][5]:
            if 'BROAD' in str_data[ii][7] or 'PHRASE' in str_data[ii][7]:
                if 'b0' not in str_data[ii][8]:
                    if int(str_data[ii][10]) >= 8:
                        if int(str_data[ii][17]) == 0:
                            if keyword_doesnt_contain_special_chars(str_data[ii][8]):
                                row = entry_in_workbook(out_sheet, str_data[ii], row, "Negative Exact")

        if 'asin auto' in str_data[ii][5]:
            if 'b0' not in str_data[ii][8]:
                if float(str_data[ii][14]) == 0.0 or float(str_data[ii][13])/float(str_data[ii][14]) > 0.3:
                    if keyword_doesnt_contain_special_chars(str_data[ii][8]):
                        row = entry_in_workbook(out_sheet, str_data[ii], row, "Negative Phrase")

        if 'b0' in str_data[ii][8]:
#            if 'auto' not in str_data[ii][5].lower():
            if int(str_data[ii][10]) >= 8:
                if int(str_data[ii][17]) == 0:
                    if 'auto' in str_data[ii][5].lower() or 'automatic' in str_data[ii][5].lower() \
                    or 'auto' in str_data[ii][4].lower() or 'automatic' in str_data[ii][4].lower():
                        row = entry_in_workbook(out_sheet, str_data[ii], row, "Negative Exact")
                    else:
                        row = entry_in_workbook(out_sheet, str_data[ii], row, "Negative targeting expression")



    out_workbook.close()

    main()

