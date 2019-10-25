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

def add_key_to_kw_dict(key,kw_dict):
    if key[0] not in kw_dict:
        kw_dict[key[0]] = [key[2]]
    else:
        if key[2] not in kw_dict[key[0]]:
            kw_dict[key[0]].append(key[2])
    return kw_dict

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    products = configuration_file.PRODUCTS
    bulk_data = read_all_rows_cols(workbook)

    kw_dict = dict()
    tbkw_dict = dict()


    for i in range(len(bulk_data)):

        for ii in range(len(products)):
            # Reading rows and columns of audit str sheet
            search_name = products[ii]['search_name']
            sku = products[ii]['search_name']
            #print (products[ii]['search_name'])
            #print (bulk_data[i][8].lower())
            if search_name.lower() in bulk_data[i][9].lower():
                if bulk_data[i][1] == 'Keyword' or ( bulk_data[i][1] == 'Product Targeting' and bulk_data[i][13] == 'Targeting Expression' ):

                    if int(bulk_data[i][19]) > 1:
                        if (sku,bulk_data[i][11]) not in tbkw_dict:
                            tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])] = [int(bulk_data[i][19]),float(bulk_data[i][20]),float(bulk_data[i][23])]
                        else:
                            tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][0] = tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][0]  + int(bulk_data[i][19])
                            tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][1] = tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][1]  + float(bulk_data[i][20])
                            tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][2] = tbkw_dict[(sku,bulk_data[i][13],bulk_data[i][11])][2]  + float(bulk_data[i][23])


##                elif bulk_data[i][1] == 'Product Targeting':
##
##                    if 'asin' in bulk_data[i][11]:
##                        if int(bulk_data[i][19]) > 1:
##                            if (sku,bulk_data[i][11]) not in tbkw_dict:
##                                tbkw_dict[(sku,bulk_data[i][11])] = [int(bulk_data[i][19]),float(bulk_data[i][20]),float(bulk_data[i][23])]
##                            else:
##                                tbkw_dict[(sku,bulk_data[i][11])][0] = tbkw_dict[(sku,bulk_data[i][11])][0]  + int(bulk_data[i][19])
##                                tbkw_dict[(sku,bulk_data[i][11])][1] = tbkw_dict[(sku,bulk_data[i][11])][1]  + float(bulk_data[i][20])
##                                tbkw_dict[(sku,bulk_data[i][11])][2] = tbkw_dict[(sku,bulk_data[i][11])][2]  + float(bulk_data[i][23])


    for key,value in tbkw_dict.items():
        if tbkw_dict[key][1] > 10.0:
            if tbkw_dict[key][2] > 0.0:
                if tbkw_dict[key][1] > 25.0:
                    if tbkw_dict[key][1] / tbkw_dict[key][2] > 0.6:
                        #print (key[1])
                        #print (tbkw_dict[key][1])
                        #print (tbkw_dict[key][1] / tbkw_dict[key][2])
                        kw_dict = add_key_to_kw_dict(key,kw_dict)

            else:
                #print (key[1])
                #print (tbkw_dict[key][1])
                kw_dict = add_key_to_kw_dict(key,kw_dict)





    temp = configuration_file.FILE_LOCATION['gen_lb_keywords_asins']
    out_workbook = xlsxwriter.Workbook(temp)
    out_worksheet = out_workbook.add_worksheet()
    col = 0
    out_worksheet.write(0,col,'Search Name')
    out_worksheet.write(1,col,'Sku')
    out_worksheet.write(2,col,'Keywords/Asins')
    col = col + 1
    temp1_list = list()
    temp2_list = list()


    for key,val in kw_dict.items():
        out_worksheet.write(0,col,key)
        for ii in range(len(products)):
            # Reading rows and columns of audit str sheet
            search_name = products[ii]['search_name']
            if search_name == key :
                out_worksheet.write(1,col,products[ii]['sku'])
                break
        out_worksheet.write_column(2,col, val)
        col = col + 1

#    out_worksheet.write(0,0,'Account level bad Kws and Asins')
#    out_worksheet.write_column(1,0, temp1_list)

    out_workbook.close()
    main()

