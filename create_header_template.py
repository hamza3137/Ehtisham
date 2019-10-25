#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Asad Ashraf
#
# Created:     24/04/2019
# Copyright:   (c) Asad Ashraf 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlrd
import xlsxwriter
import datetime
import math
import re
import sys

if (len(sys.argv) > 1 ):
    configuration_file = __import__(sys.argv[1])
else:
    import config_nexon as configuration_file


def open_excel_for_read(file_location):
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook,sheet_name):
    try:
        str_worksheet = workbook.sheet_by_name(sheet_name)
    except xlrd.XLRDError:
        return []
    number_rows = str_worksheet.nrows
    number_cols = str_worksheet.ncols

    table = list()
    record = list()

    for x in range(number_rows):
        for y in range(number_cols):
            record.append(str_worksheet.cell(x,y).value)
        table.append (record)
        record = []
    return table


def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook1 = open_excel_for_read('sku_names')
    sku_names_data = read_all_rows_cols(workbook1,configuration_file.account_name.upper())

    upload_file_name = configuration_file.base_file_location \
    + configuration_file.account_name + '_header_template.xlsx'



    out_workbook = xlsxwriter.Workbook(upload_file_name)
    out_worksheet = out_workbook.add_worksheet()
    cols = 0

    out_worksheet.write(0,cols,"Sku")
    out_worksheet.write(1,cols,"Searchable Name")
    out_worksheet.write(2,cols,"Data Reference")
    out_worksheet.write(3,cols,"Bid Exact,Phrase,Broad")
    out_worksheet.write(4,cols,"Budget")
    out_worksheet.write(5,cols,"Start Date")
    out_worksheet.write(6,cols,"End Date")
    out_worksheet.write(7,cols,"Keywords/Asins")

    cols = cols + 1

    sku_list = list()

    for i in range(1,len(sku_names_data)):
        if sku_names_data[i][0]:

            if (sku_names_data[i][4] == 'RUNNING' or sku_names_data[i][4] == 'START'):
                sku_dict = dict()
                out_worksheet.write(0,cols,sku_names_data[i][1])
                out_worksheet.write(1,cols,sku_names_data[i][2])
                cols = cols + 1

                sku_dict['search_name'] = sku_names_data[i][2]
                sku_dict['sku'] = sku_names_data[i][1]
                sku_dict['ad_group_level'] = True
                sku_list.append(sku_dict)

    out_workbook.close()
    print('[')
    for item in sku_list:
        print (str(item) +',')
    print (']')
    main()

