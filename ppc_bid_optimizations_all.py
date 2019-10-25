#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     08/18/2019
#-------------------------------------------------------------------------------
##    All bids should be ceiled at 2.98
##  Aggressive bids for good performing keywords/asins
##
##    if conversion_rate > 12% and orders >= 5
##            If Acos <= 15%
##                Increase bid by 25%
##            If 15% < Acos <= 30%
##                Increase bid by slope eq y = mx + c
##                m = -25/15 , c = 50, x = acos, y = bid increase
##            If  30 < Acos <= 50
##                do not change current bid
##
##  White list Handling
##  G formula for high acos

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

def read_all_rows_cols (workbook,name):
    try:
        str_worksheet = workbook.sheet_by_name(name)
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

def calculate_G_formula(acos,target_acos,current_bid,cpc):
    if acos <= target_acos:
        output_bid = current_bid
    else:
        output_bid = (1 - (acos - target_acos)/100) * current_bid
        if output_bid < 0.8 * cpc:
            output_bid = 0.8 * cpc
        if output_bid > current_bid: #someone manually reduces the bid
            output_bid = current_bid

    return round(output_bid,2)

def calculate_increase_factor(acos):

    if acos <= 0.15:
        increase_factor = 0.25
    elif  (acos > 0.15) and (acos <= 0.3):
        increase_factor = (-25/15*acos*100 + 50)/100
    else:
        increase_factor = 0

##    print ('acos:{0} , increase_factor: {1}'.format(acos,increase_factor))

    return increase_factor

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook,'Sponsored Products Campaigns')

    workbook1 = open_excel_for_read('white_list_file')
    str_data1 = read_all_rows_cols(workbook1,configuration_file.account_name.upper())

    white_list_keywords = list()
    # Reading data in white list
    for i, val in enumerate(str_data1):
        if i == 0:
            continue
        if val[0]:
            val.append(0)
            white_list_keywords.append(val)


    date = datetime.datetime.now().strftime("%m%d%Y_%H%M")

    b4_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_bid_calculations_b4_change_' + date + '.xlsx'
    after_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_bid_calculations_after_change_' + date + '_upload.xlsx'

    out_workbook1 = xlsxwriter.Workbook(b4_change)
    out_worksheet1 = out_workbook1.add_worksheet()

    out_workbook2 = xlsxwriter.Workbook(after_change)
    out_worksheet2 = out_workbook2.add_worksheet()
    row = 0

    highest_bid = configuration_file.max_highest_bid
    target_acos = configuration_file.target_acos
    wl_target_acos = configuration_file.wl_target_acos

    for i,val in enumerate(bulk_data):

        in_whitelist = 0
        bid_changed = 0
        after_change_bid = 0.0

        if i == 0:
            out_worksheet1.write_row(row,0,val)
            out_worksheet2.write_row(row,0,val)
            row = row + 1
            continue

        if val[1] == 'Keyword':
            for jj,white in enumerate(white_list_keywords):
                if white[0] == val[3]:
                    if white[1] == val[9]:
                        if white[2] == val[11]:
                            if ( (white[6] and white[6].lower() == val[13]) or val[13] == 'exact'):
                                in_whitelist = 1
                                break

        if val[1] == 'Keyword' or  ( val[1] == 'Product Targeting' and \
        (val[13] == 'Targeting Expression' or val[13] == 'Targeting Expression Predefined')):
            ## No bid aggression for auto targeting campaigns
            if val[13] != 'Targeting Expression Predefined' and configuration_file.sales_optimized:

                if int(val[21]) >= 5:

                    if not val[10]:
                        val = ensure_current_bid(bulk_data,val,i)
                    if float(val[21])/float(val[19]) > 0.12:
                        acos = float(val[20])/float(val[23])

                        if acos <= 0.5:

                            increase_factor = calculate_increase_factor(acos)
                            temp = round(float(val[10])*(1 + increase_factor),2)
                            if in_whitelist:
                                if temp < float(white_list_keywords[jj][3]):
                                    temp = float(white_list_keywords[jj][3])
                            if temp > highest_bid:
                                temp = highest_bid
                            if float(val[20]) > 0.0:
                                cpc =  float(val[20])/float(val[19])
                                if temp < 0.8 * cpc:
#                                    print (val)
#                                    print('Should not be here at 1')
                                    temp = 0.8 * cpc
                            after_change_bid = temp
                            bid_changed = 1

##                        elif float(val[20])/float(val[23]) < 0.5 and float(val[20])/float(val[23]) > 0.3:
##
##                            temp = round(float(val[10])*1.1,2)
##                            if in_whitelist:
##                                if temp < float(white_list_keywords[jj][3]):
##                                    temp = float(white_list_keywords[jj][3])
##                            if temp > highest_bid:
##                                temp = highest_bid
##                            after_change_bid = temp
##                            bid_changed = 1

            if (float(val[23]) > 0.0) and (int(val[21]) > 0) :
                if not val[10]:
                    val = ensure_current_bid(bulk_data,val,i)

                acos = float(val[20])/float(val[23])*100
                if float(val[20]) > 0.0:
                    cpc =  float(val[20])/float(val[19])
                else:
                    continue
                if in_whitelist:
                    if bid_changed == 1:
                        pass
                    else:
                        temp = float(val[10])
                        if temp < float(white_list_keywords[jj][3]):
                            temp = float(white_list_keywords[jj][3])
                        if temp > highest_bid:
                            temp = highest_bid

                        after_change_bid = calculate_G_formula(acos,wl_target_acos,temp,cpc)
                        bid_changed = 1

                    white_list_keywords[jj][8] = 1

                else:
                    if bid_changed == 1:
                        pass
                    else:
                        temp = float(val[10])
                        if temp < after_change_bid:
                            temp = after_change_bid
                        if temp > highest_bid:
                            temp = highest_bid

                        after_change_bid = calculate_G_formula(acos,target_acos,temp,cpc)
                        bid_changed = 1

            elif (float(val[23]) > 0.0) and (int(val[21]) > 0) :
                print('some thing is wrong;check {0}'.format(val))

##            Waiting for Sean's response for now
##            if val[1] == 'Ad Group':
##            if 'auto' in val[9].lower():
##                acos = float(val[20])/float(val[23])*100
##                if float(val[20]) > 0.0:
##                    cpc =  float(val[19])/float(val[20])
##                else:
##                    continue
##
##                temp = float(val[10])
##
##                after_change_bid = calculate_G_formula(acos,target_acos,temp,cpc)
##                bid_changed = 1



        if (bid_changed == 1) and (float(val[10]) != after_change_bid):
            out_worksheet1.write_row(row,0,val)
            val[10] = str(after_change_bid)
            out_worksheet2.write_row(row,0,val)
            row = row + 1


    out_workbook1.close()
    out_workbook2.close()


    main()

