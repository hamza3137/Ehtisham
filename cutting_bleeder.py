#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     24/04/2019

#-------------------------------------------------------------------------------
##    This script will be performing cutting bleeders
##
##    Ad Group Negative bleeder Manual
##    Ad Group Negavtive bleeder Auto
##    Keyword Bleeder Manual
##    Asin bleeder manual
##    Auto targeting  bleeder

##    For Ad level
##    click >= 25, spend >= 7, order = 0
##    for keyword, asin level
##    final bid = cpc * 0.5
##
##
##    For keyword, asin
##    click >= 8, spend >=1 , order = 0
##    final bid = cpc * 0.75
##
##
##    For auto targeting
##    click >= 12, spend >=1 , order = 0
##    final bid = lower (cpc,current bid)

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

def ensure_current_bid (bulk_data,val,i):

    if val[10]:
        pass
    else:
        for j in range(i):
            if bulk_data[i-j][1] == 'Ad Group':
                if bulk_data[i-j][3] == val[3]:
                    if bulk_data[i-j][9] == val[9]:
                        val[10] = bulk_data[i-j][10]
                        break

    return val

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook)

    date = datetime.datetime.now().strftime("%m%d%Y_%H%M")

    b4_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_cutting_bleeder_b4_change_' + date + '.xlsx'

    after_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_cutting_bleeder_after_change_' + date + '_upload.xlsx'

    out_workbook1 = xlsxwriter.Workbook(b4_change)
    out_worksheet1 = out_workbook1.add_worksheet()

    out_workbook2 = xlsxwriter.Workbook(after_change)
    out_worksheet2 = out_workbook2.add_worksheet()

    row = 0

    for i,val in enumerate(bulk_data):
        if i == 0:
            out_worksheet1.write_row(i,0,val)
            out_worksheet2.write_row(i,0,val)
            row = row + 1
            continue
        #print ('line number {0}'.format(i))
        if val[1] == 'Ad Group':
            if int(val[19]) >= 25:
                if int(val[21]) == 0:
                    if float(val[20]) >= 7.0:
                        cpc = float(val[20])/float(val[19])

                        if float(val[10]) > cpc * 0.5:
                            out_worksheet1.write_row(row,0,val)
                            val[10] = str(round(cpc * 0.5,2))
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1


#        if val[1] == 'Keyword':
#        if val[1] == 'Product Targeting' and val[13] == 'Targeting Expression':
        if val[1] == 'Keyword' or  ( val[1] == 'Product Targeting' and val[13] == 'Targeting Expression'):
            if int(val[19]) >= 8:
                if int(val[21]) == 0:
                    if float(val[20]) >= 1.0:
                        val = ensure_current_bid (bulk_data,val,i)
                        cpc = float(val[20])/float(val[19])

                        if float(val[10]) > cpc * 0.75:
                            out_worksheet1.write_row(row,0,val)
                            val[10] = str(round(cpc * 0.75,2))
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1

        if val[1] == 'Product Targeting' and val[13] == 'Targeting Expression Predefined':
            if int(val[19]) >= 8:
                if int(val[21]) == 0:
                    if float(val[20]) >= 1.0:
                        val = ensure_current_bid (bulk_data,val,i)
                        cpc = float(val[20])/float(val[19])

                        if float(val[10]) > cpc:
                            out_worksheet1.write_row(row,0,val)
                            val[10] = str(round(cpc,2))
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1


    out_workbook1.close()
    out_workbook2.close()

    main()

