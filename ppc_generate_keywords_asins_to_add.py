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


common_words = ['for','-','&','a', 'oz','just','or','to','by','1fl','ō',
'mg','the','in','of','at','me','and','/','ml','this','are','"40','4oz',
'oz.','an','up','.','™',',','ģ','%','_','\'','’','|','+','$','ã']

ignore_strs_list = ['.','™', 'ō','’','|','+','$','ã']

def open_excel_for_read(file_location):
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook):
    try:
        str_worksheet = workbook.sheet_by_index(0)
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

def generate_unique_words (pcst, tcst):
    sstr = []
    unique_words = []
    if tcst:
        for i in range(len(tcst)):
            sstr.append(tcst[i])

    if pcst:
        for i in range(len(pcst)):
            sstr.append(pcst[i])

    if sstr:
        for i in range(len(sstr)):
            temp = sstr[i].split()
            for j in range(len(temp)):
                if temp[j] not in unique_words and temp[j] not in common_words and not re.search('\d+', temp[j]):
                    unique_words.append(temp[j])

    return unique_words

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('str_file_location')
    products = configuration_file.PRODUCTS

    if configuration_file.override_start_date:
        start_date = configuration_file.start_date
    else:
        start_date = datetime.datetime.now().strftime("%m/%d/%Y")

    if configuration_file.override_end_date:
        end_date = configuration_file.end_date
    else:
        end_date = ''

    temp = configuration_file.FILE_LOCATION['keywords_to_add_file']
    out_workbook = xlsxwriter.Workbook(temp)
    out_worksheet = out_workbook.add_worksheet()
    col = 0

    out_worksheet.write(0,col,'Sku')
    out_worksheet.write(1,col,'Search Name')
    out_worksheet.write(2,col,'Reference')
    out_worksheet.write(3,col,'Bid E,P,B')
    out_worksheet.write(4,col, 'Budget')
    out_worksheet.write(5,col, 'Start Date')
    out_worksheet.write(6,col, 'End Date')
    out_worksheet.write(7,col,'Keywords')
    col = col + 1

    temp = configuration_file.FILE_LOCATION['asins_to_add_file']
    out_workbook1 = xlsxwriter.Workbook(temp)
    out_worksheet1 = out_workbook1.add_worksheet()
    col1 = 0

    out_worksheet1.write(0,col1,'Sku')
    out_worksheet1.write(1,col1,'Search Name')
    out_worksheet1.write(2,col1,'Reference')
    out_worksheet1.write(3,col1,'Bid E,P,B')
    out_worksheet1.write(4,col1, 'Budget')
    out_worksheet1.write(5,col1, 'Start Date')
    out_worksheet1.write(6,col1, 'End Date')
    out_worksheet1.write(7,col1,'Asins')
    col1 = col1 + 1

    str_data = read_all_rows_cols(workbook)

    em = configuration_file.enhance_bid_multiplier

    for sku in range(len(products)):

        # Reading rows and columns of audit str sheet
        search_name = products[sku]['search_name']
        pcst = []
        tcst = []
        asins = []
        spend = 0.0
        clicks = 0.0
        for i in range(len(str_data)):
            if i == 0:
                continue
            if search_name.lower() in str_data[i][5].lower():
                if 'EXACT' == str_data[i][7]:
                    spend = spend + float(str_data[i][13])
                    clicks = clicks + float(str_data[i][10])
                if not str_data[i][8].startswith('b0'):
                    if int(str_data[i][20]) >= 3:
                        if str_data[i][8] not in pcst:
                            pcst.append(str_data[i][8])
                    elif int(str_data[i][20]) >= 1 and int(str_data[i][20]) <= 2:
                        if str_data[i][8] not in tcst or str_data[i][8] not in pcst:
                            tcst.append(str_data[i][8])
                else:
                    if int(str_data[i][20]) >= 1:
                        if str_data[i][8] not in asins:
                            asins.append(str_data[i][8])

        if clicks > 0.0:
            cpc = spend/clicks
        else:
            cpc = 0.0
        if pcst:
            out_worksheet.write(0,col,products[sku]['sku'])
            out_worksheet.write(1,col,products[sku]['search_name'])
            out_worksheet.write(2,col,"pcst")
            out_worksheet.write(3,col,str(round(em*cpc,2)) + ',' + str(round(em * cpc * 0.9 ,2)) + ',' + str(round(em*cpc*0.9*0.75,2)))
            out_worksheet.write(4,col, 15)
            out_worksheet.write(5,col, start_date)
            out_worksheet.write(6,col, end_date)
            out_worksheet.write_column(7,col,pcst)
            col = col + 1
        if tcst:
            out_worksheet.write(0,col,products[sku]['sku'])
            out_worksheet.write(1,col,products[sku]['search_name'])
            out_worksheet.write(2,col,"tcst")
            out_worksheet.write(3,col,str(0) + ',' + str(round(cpc * 0.9 * 0.9,2)) + ',' + str(round(cpc*0.9 * 0.9 *0.75,2)))
            out_worksheet.write(4,col, 15)
            out_worksheet.write(5,col, start_date)
            out_worksheet.write(6,col, end_date)
            out_worksheet.write_column(7,col,tcst)
            col = col + 1

        if tcst or pcst:
            unique_words = generate_unique_words (pcst, tcst)
            out_worksheet.write(0,col,products[sku]['sku'])
            out_worksheet.write(1,col,products[sku]['search_name'])
            out_worksheet.write(2,col,"gp")
            out_worksheet.write(3,col,str(0) + ',' + str(0.27) + ',' + str(0.27))
            out_worksheet.write(4,col, 10)
            out_worksheet.write(5,col, start_date)
            out_worksheet.write(6,col, end_date)
            out_worksheet.write_column(7,col,unique_words)
            col = col + 1

        if asins:
            out_worksheet1.write(0,col1,products[sku]['sku'])
            out_worksheet1.write(1,col1,products[sku]['search_name'])
            out_worksheet1.write(2,col1,"converting product")
            out_worksheet1.write(3,col1,round(cpc,2))
            out_worksheet1.write(4,col1, 15)
            out_worksheet1.write(5,col1, start_date)
            out_worksheet1.write(6,col1, end_date)
            out_worksheet1.write_column(7,col1, asins)
            col1 = col1 + 1

    out_workbook.close()
    out_workbook1.close()

    main()

