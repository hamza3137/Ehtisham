#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     24/04/2019

#-------------------------------------------------------------------------------
##    This script will be used for account import to ppc process


import xlrd
import xlsxwriter
import re
import datetime
import sys

if (len(sys.argv) > 1 ):
    configuration_file = __import__(sys.argv[1])
else:
    import config_nexon as configuration_file


def open_excel_for_read(file_location):
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook):
    try:
        str_worksheet = workbook.sheet_by_name('Sponsored Products Campaigns')
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
##        x = x + 1
    return table

def calculate_G_formula(acos,target_acos,current_bid,cpc):
    if acos <= target_acos:
        output_bid = current_bid
    else:
        output_bid = (1 - (acos - target_acos)/100) * current_bid
        if output_bid < 0.8 * cpc:
            output_bid = 0.8 * cpc

    return round(output_bid,2)


def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook)
    products = configuration_file.PRODUCTS

    b4_change = configuration_file.base_file_location + configuration_file.account_name \
    + '_adgroup_renames.xlsx'

    out_workbook1 = xlsxwriter.Workbook(b4_change)
    out_worksheet1 = out_workbook1.add_worksheet()

    row = 0

    for i,val in enumerate(bulk_data):
        #print ('here at 1')
        if i == 0:
            out_worksheet1.write(row,0,'Campaign Name')
            out_worksheet1.write(row,1,'Ad Group Name')
            out_worksheet1.write(row,2,'SKU Name')
            out_worksheet1.write(row,3,'Comments')
            row = row + 1
            continue


        if val[1] == 'Ad':
            for j in range(len(products)):
                search_name = products[j]['search_name']
                sku = products[j]['sku']
                #print (sku)
                #print (val[13])
                if sku == val[14]:
                    if search_name not in val[9]:
                        out_worksheet1.write(row,0,val[3])
                        out_worksheet1.write(row,1,val[9])
                        out_worksheet1.write(row,2,val[14])
                        text = 'Please add text "' + search_name + '" to ad group ' + val[9]
                        out_worksheet1.write(row,3,text)
                        row = row + 1


    out_workbook1.close()

    main()

