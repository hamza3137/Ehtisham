#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     08/18/2019
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
    print ('Opening file {0}'.format(configuration_file.FILE_LOCATION[file_location]))
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

    return round(output_bid,2)

def get_low_performing_kws_list(str_data4, search_name):
    kws_list = list()

    if str_data4:
        for i in range(len(str_data4[0])):
            if search_name == str_data4[0][i]:
                for j in range(2,len(str_data4)):
                    kws_list.append(str_data4[j][i])
                break
#    print('printing keyword list')
#    print (kws_list)
    return kws_list


def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook,'Sponsored Products Campaigns')

    workbook1 = open_excel_for_read('low_bid_keywords_asins')
    str_data1 = read_all_rows_cols(workbook1,configuration_file.account_name.upper())


    date = datetime.datetime.now().strftime("%m%d%Y_%H%M")

    b4_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_bad_performer_b4_change_' + date + '.xlsx'
    after_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_bad_performer_after_change_' + date + '_upload.xlsx'

    out_workbook1 = xlsxwriter.Workbook(b4_change)
    out_worksheet1 = out_workbook1.add_worksheet()

    out_workbook2 = xlsxwriter.Workbook(after_change)
    out_worksheet2 = out_workbook2.add_worksheet()
    row = 0

    sku_bad_performer_dict = dict()
    for index in range(1,len(str_data1[0])):
        search_name = str_data1[0][index]
        low_performing_kws = get_low_performing_kws_list(str_data1, search_name)
        sku_bad_performer_dict[search_name] = low_performing_kws

    bad_keyword_max_bid = configuration_file.bad_keyword_max_bid

    for i,val in enumerate(bulk_data):

        bid_changed = 0
        after_change_bid = 0.0

        if i == 0:
            out_worksheet1.write_row(row,0,val)
            out_worksheet2.write_row(row,0,val)
            row = row + 1
            continue

        if (val[1] == 'Keyword' and 'negative' not in val[13]) or \
         ( val[1] == 'Product Targeting' and val[13] == 'Targeting Expression'):

                for key,val2 in sku_bad_performer_dict.items():
                    if key in val[9]:
                        if val[11] in sku_bad_performer_dict[key]:
                            if not val[10]:
                                val = ensure_current_bid(bulk_data,val,i)
                            if float(val[10]) > bad_keyword_max_bid:
                                if int(val[21]) == 0:
                                    bid_changed = 1
                                    break
                                else:
                                    if float(val[20])/float(val[23]) <= 0.35 and int(val[21]) > 1:
                                        print ('passing {0} keyword for search name {1}'.format(val[11],key))
                                        #print (val)
                                        pass
                                    else:
                                        bid_changed = 1
                                    break

        if (bid_changed == 1) and (float(val[10]) != bad_keyword_max_bid):
            out_worksheet1.write_row(row,0,val)
            val[10] = str(bad_keyword_max_bid)
            out_worksheet2.write_row(row,0,val)
            row = row + 1



    out_workbook1.close()
    out_workbook2.close()


    main()

