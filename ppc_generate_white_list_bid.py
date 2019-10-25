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

def bid_calculation(bulk_data,input_bid,target_acos):

    if float(bulk_data[23]) != 0.0 :
        acos = float(bulk_data[20]) / float(bulk_data[23]) * 100
    elif float(bulk_data[20]) <= 20.00:
        acos = 50.0
    else:
        acos = 500.0

    #print (acos)
    #print (target_acos)

    current_bid = float(bulk_data[10])


    if  ( acos <= target_acos or float(target_acos) == 0.0):
        if input_bid > current_bid:
            output_bid = input_bid
        else:
            output_bid = current_bid
    else:
        output_bid = (1 - (acos - target_acos)/100) * input_bid
        if output_bid < 0.8 * current_bid:
            output_bid = 0.8 * current_bid

    return str(round(output_bid,2))

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook1 = open_excel_for_read('white_list_file')
    str_data1 = read_all_rows_cols(workbook1,configuration_file.account_name.upper())
    workbook2 = open_excel_for_read('bulk_file_location')
    str_data2 = read_all_rows_cols(workbook2,'Sponsored Products Campaigns')
    date = datetime.datetime.now().strftime("%m%d%Y")

    upload_file_name = configuration_file.FILE_LOCATION['upload_file_location'] \
    + configuration_file.account_name + '_white_list_after_' + date + '_upload.xlsx'

    upload_file_name1 = configuration_file.FILE_LOCATION['upload_file_location'] \
    + configuration_file.account_name + '_white_list_b4_' + date + '.xlsx'
    #date = datetime.datetime.now().strftime("%m%d%Y")

    out_workbook = xlsxwriter.Workbook(upload_file_name)
    out_worksheet = out_workbook.add_worksheet()
    out_workbook1 = xlsxwriter.Workbook(upload_file_name1)
    out_worksheet1 = out_workbook1.add_worksheet()
    rows = 0
    rows1 = 0

    out_worksheet1.write_row(rows1,0,str_data2[0])
    out_worksheet.write_row(rows,0,str_data2[0])
    rows1 = rows1 + 1
    rows = rows + 1

    for i in range(1,len(str_data1)):
        found = 0
        if str_data1[i][0]:
            #print ("pass")
            for j in range(1,len(str_data2)):
                if str_data1[i][0] == str_data2[j][3]:
                    #print ('pass3')
                    if str_data1[i][1] in str_data2[j][9]:
                        if (str_data1[i][6] and str_data1[i][6].lower() == str_data2[j][13]) or str_data2[j][13] == 'exact':
                            if str_data1[i][2] == str_data2[j][11]:
                                if not str_data2[j][10]:
                                    for k in range(j):
                                        if str_data2[j-k][1] == 'Ad Group':
                                            if str_data2[j-k][3] == str_data2[j][3]:
                                                if str_data2[j-k][9] == str_data2[j][9]:
                                                    str_data2[j][10] = str_data2[j-k][10]
                                                    break
                                out_worksheet1.write_row(rows1,0,str_data2[j])
                                str_data2[j][10] = bid_calculation(str_data2[j],float(str_data1[i][3]),100.0)
                                out_worksheet.write_row(rows,0,str_data2[j])
                                rows = rows + 1
                                rows1 = rows1 + 1
                                found = 1
                                break

        elif str_data1[i][5]:

            for j in range(1,len(str_data2)):
                if 'Keyword' == str_data2[j][1]:
                    if str_data1[i][5] in str_data2[j][3]:
                        if (str_data1[i][6] and str_data1[i][6].lower() == str_data2[j][13]) or str_data2[j][13] == 'exact':
                            if str_data1[i][2] == str_data2[j][11]:
                                if not str_data2[j][10]:
                                    for k in range(j):
                                        if str_data2[j-k][1] == 'Ad Group':
                                            if str_data2[j-k][3] == str_data2[j][3]:
                                                if str_data2[j-k][9] == str_data2[j][9]:
                                                    str_data2[j][10] = str_data2[j-k][10]
                                                    break
                                out_worksheet1.write_row(rows1,0,str_data2[j])
                                str_data2[j][10] = bid_calculation(str_data2[j],float(str_data1[i][3]),100.0)
                                out_worksheet.write_row(rows,0,str_data2[j])
                                rows = rows + 1
                                rows1 = rows1 + 1
                                found = 1
                                break
        if found == 0:
            # temporary fix
            rows1 = rows1 + 1
            #out_worksheet1.write_row(rows,0,str_data1[i])
            #print (str_data1[i])
            if str_data1[i][0]:
                out_worksheet.write(rows,1, 'Keyword')
                out_worksheet.write(rows,3, str_data1[i][0])
                out_worksheet.write(rows,9, str_data1[i][1])
                out_worksheet.write(rows,10, str(str_data1[i][3]))
                out_worksheet.write(rows,11, str_data1[i][2])
                if str_data1[i][6]:
                    out_worksheet.write(rows,13, str_data1[i][6])
                else:
                    out_worksheet.write(rows,13, 'exact')
                out_worksheet.write(rows,17, "Enabled")
                rows = rows + 1
            else:
                print ("Have to fix this")
                print (str_data1[i])
    out_workbook.close()
    out_workbook1.close()

    main()

