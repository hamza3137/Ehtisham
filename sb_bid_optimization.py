#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     24/04/2019

#-------------------------------------------------------------------------------
##    This script will be performing bid optimization on sponsored brands keywords
##
##
##    Cutting Bleeder
##    Auto G
##    Bid Aggression
##
##
##    For keyword
##    click >= 8, spend >=1 , order = 0
##    final bid = cpc * 0.75
##
##

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
        str_worksheet = workbook.sheet_by_name('Sponsored Brands Campaigns')
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
        if output_bid > current_bid:
            output_bid = current_bid

    return round(output_bid,2)

def calculate_change_factor(acos):

    if acos <= 0.15:
        change_factor = 0.25
    elif  (acos > 0.15) and (acos <= 0.3):
        change_factor = (-25/15*acos*100 + 50)/100
    else:
        change_factor = 0

    return change_factor

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook)

    date = datetime.datetime.now().strftime("%m%d%Y")

    b4_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_sb_bid_optimization_b4_change_' + date + '.xlsx'

    after_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_sb_bid_optimization_after_change_' + date + '_upload.xlsx'

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


        if val[1] == 'Keyword':

            if int(val[28]) == 0:

                if int(val[26]) >= 8:

                    if float(val[27]) >= 1.0:

                        cpc = float(val[27])/float(val[26])

                        if float(val[18]) > cpc * 0.75:
                            out_worksheet1.write_row(row,0,val)
                            val[18] = str(round(cpc * 0.75,2))
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1
            else:
#                print (val)
                if (int(val[26]) > 0) and (float(val[30]) > 0) :
                    convertion_rate = float(val[28])/ float(val[26])
                    acos = float(val[27])/float(val[30])
                    if (int(val[28]) >= 5 and acos <= 0.5 and convertion_rate >= 0.12) \
                    and configuration_file.sales_optimized :

                        change_factor = calculate_change_factor(acos)

                        temp = round(float(val[18])*(1+change_factor),2)

                        #print ('change factor:{0}, new bid: {1}'.format(change_factor,temp))

                        if float(val[18]) > configuration_file.max_bid:
                            temp = float(val[18])
                        elif temp > configuration_file.max_bid:
                            temp = configuration_file.max_bid

                        if temp != float(val[18]):
                            out_worksheet1.write_row(row,0,val)
                            val[18] = str(temp)
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1

##                    elif (int(val[28]) >= 5 and acos <= 0.3 and convertion_rate > 0.12) \
##                    and configuration_file.sales_optimized:
##    ##                    print ('here 2')
##                        temp = round(float(val[18])*1.25,2)
##                        if temp > configuration_file.max_bid:
##                            temp = configuration_file.max_bid
##                        if temp != float(val[18]):
##                            out_worksheet1.write_row(row,0,val)
##                            val[18] = str(temp)
##                            out_worksheet2.write_row(row,0,val)
##                            row = row + 1
                    else:
    ##                    print ('here 3')
                        temp = float(val[18])
                        acos = float(val[27])/float(val[30])*100
                        cpc = cpc = float(val[27])/float(val[26])

                        temp = calculate_G_formula(acos,configuration_file.target_acos,temp,cpc)
                        if temp != float(val[18]):
                            out_worksheet1.write_row(row,0,val)
                            val[18] = str(temp)
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1

                elif (int(val[26]) > 0) or (float(val[30]) > 0 ) :
                    print ('Something wrong; check {0}'.format(val))

    out_workbook1.close()
    out_workbook2.close()

    main()

