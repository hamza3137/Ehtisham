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


epb = {
    0 : 'exact',
    1 : 'phrase',
    2 : 'broad',
}

ignore_strs_list = ['.','™', 'ō','-','/',',','\'','ģ','%','_','’','|','+','$','ã','‘',\
')','(','\\',':','®','?','º','"',]

def open_excel_for_read(file_location):
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook):
    try:
        #print ('0')
        str_worksheet = workbook.sheet_by_index(0)
        #str_worksheet = workbook.sheet_by_name('Sheet1')
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

def de_duplicate(str_data1 , i ):

    temp_list = list() # List that will be reference for dedupe
    unique_list = list()


    for j in range(10,len(str_data1)):
        ignore = False
        if isinstance(str_data1[j][i], float) or isinstance(str_data1[j][i], int):
            continue

        if str_data1[j][i].startswith('B0') or str_data1[j][i].startswith('b0'):
            #exit ("ASIN is not expected in Input file : {0} \n \
            #row: {1} , column = {2}".format(str_data1[j][i],j+1,i+1))
            print ("ASIN is not expected in Input file : {0} \n \
            row: {1} , column = {2}".format(str_data1[j][i],j+1,i+1))
            continue
        for jj in range(len(ignore_strs_list)):
            if re.findall('\\' + ignore_strs_list[jj],str_data1[j][i]):
                ignore = True
        if str_data1[j][i] and ignore is False:
            if str_data1[j][i] not in unique_list:
                if str_data1[j][i] not in temp_list:
                    if 'kindle' not in str_data1[j][i]:
                        if len(str_data1[j][i].split(' ')) <= 8:
                            unique_list.append(str_data1[j][i])
        #work around for the ongoing issue
        #if len(unique_list) == 2:
        #S    break

    return unique_list

def calculate_bid_for_exact(search_name,str_data3):
    spend = 0.0
    clicks = 0.0

    for j in range(len(str_data3)):
        if search_name.lower() in str_data3[j][5].lower():
            if 'EXACT' == str_data3[j][7]:
                spend = spend + float(str_data3[j][13])
                clicks = clicks + float(str_data3[j][10])

    if clicks > 0.0:
        cpc = spend/clicks
    else:
        cpc = 0.0
        exit('cpc for {0} is {1}, check search name consistency'.format(search_name,cpc))
        #print('cpc for {0} is {1}, check search name consistency'.format(search_name,cpc))
        #cpc = 1.29

    return cpc


def check_max_bid_limit (bid , max_bid):
    temp_list = list()

    for i in range(len(bid)):
        temp = bid[i]
        if float(temp) > max_bid:
            temp = str(max_bid)
        temp_list.append(temp)

    return temp_list

def write_campaign_header(out_worksheet, camp_name, str_data, index, rows, start_date, end_date,format2):

    out_worksheet.write(rows,1, 'Campaign')

    out_worksheet.write(rows,3, camp_name)

    if str_data[2][index]:
        out_worksheet.write(rows,4,str_data[2][index])
    else:
        out_worksheet.write(rows,4,10)

    out_worksheet.write(rows,6,start_date,format2)
    out_worksheet.write(rows,7,end_date,format2)
    out_worksheet.write(rows,8, 'daily')
    out_worksheet.write(rows,10,str_data[5][index])
    out_worksheet.write(rows,11,str_data[6][index])
    out_worksheet.write(rows,12,str_data[7][index])
    out_worksheet.write(rows,13,str_data[9][index])
    out_worksheet.write(rows,14,str_data[8][index])  # Creative Urls
    out_worksheet.write(rows,15,'Off')
    out_worksheet.write(rows,16,'+0%')


    rows = rows + 1

    return rows

def write_campaign_keywords(out_worksheet, camp_name,bid , epb, unique_list,rows ):

    for jj in range(len(unique_list)):
        out_worksheet.write(rows,1, 'Keyword')
        out_worksheet.write(rows,3, str(camp_name))
        out_worksheet.write(rows,18, str(bid))
        out_worksheet.write(rows,19, unique_list[jj])
        out_worksheet.write(rows,20, epb)
        rows = rows + 1

    return rows

def write_file_header(out_worksheet, rows):

    cols = 0

    out_worksheet.write(rows,cols, 'Record ID')
    cols = cols + 1
    out_worksheet.write(rows,cols, 'Record Type')
    cols = cols + 1
    out_worksheet.write(rows,cols, 'Campaign ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Budget')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Portfolio ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Start Date')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign End Date')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Budget Type')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Landing Page Url')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Landing Page ASINs')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Brand Name')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Brand Logo Asset ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Headline')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Creative ASINs')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Automated Bidding')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Bid Multiplier')
    cols = cols + 1
    out_worksheet.write(rows,cols,'AdGroup')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Max Bid')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Keyword')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Match Type')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Serving Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Ad Group Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Impressions')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Clicks')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Spend')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Orders')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Total Units')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Sales')
    cols = cols + 1
    out_worksheet.write(rows,cols,'ACoS')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Placement Type')

    rows = rows + 1

    return rows

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook1 = open_excel_for_read('sb_keywords_to_add_file')
    str_data1 = read_all_rows_cols(workbook1)

    products = configuration_file.PRODUCTS
    date = datetime.datetime.now().strftime("%m%d%Y_%H%M")

    upload_file_name = configuration_file.FILE_LOCATION['upload_file_location'] \
    + configuration_file.account_name + '_sb_keywords_' + date + '_upload.xlsx'

    date = datetime.datetime.now().strftime("%m%d%Y")

    out_workbook = xlsxwriter.Workbook(upload_file_name)
    out_worksheet = out_workbook.add_worksheet()
    format2 = out_workbook.add_format({'num_format': 'mm/dd/yy'})
    rows = 0

    rows = write_file_header(out_worksheet, rows)


    for i in range(1,len(str_data1[0])):
        unique_list = de_duplicate(str_data1, i )
        #print (str_data1[3][i])
        if str_data1[1][i]:
            bid = str_data1[1][i].split(',')
        else:
            exit('please provide bids')
        if len(bid) != 3:
            exit('bid array length in not 3, check !!!')
        if configuration_file.max_bid_limit_set:
            bid = check_max_bid_limit (bid , configuration_file.max_bid)

        budget = str_data1[2][i]

        if str_data1[3][i]:
            start_date = str_data1[5][i]
        else:
            start_date = datetime.datetime.now().strftime("%m/%d/%Y")
        end_date = str_data1[4][i]

        if not str_data1[5][i]:
            exit('No Landing Asins available for group {0}'.format(str_data1[0][i]))
        if len(str_data1[5][i].split(',')) < 3:
            exit ('At leaast 3 Asins are needed for landing asins for group {0}'.format(str_data1[0][i]))

        if not str_data1[6][i]:
            exit('No Brand Name mentioned for group {0}'.format(str_data1[0][i]))

        if not str_data1[7][i]:
            exit('No Brand Asset Logo mentioned for group {0}'.format(str_data1[0][i]))

        if not str_data1[8][i]:
            exit('No Creative Asins available for group {0}'.format(str_data1[0][i]))
        if len(str_data1[8][i].split(',')) < 3:
            exit ('At leaast 3 Creative Asins are needed for group {0}'.format(str_data1[0][i]))

        if not str_data1[9][i]:
            exit('No Headline available for group {0}'.format(str_data1[0][i]))
        if len(str_data1[9][i]) > 50:
            print (len(str_data1[9][i]))
            exit('Head is exceeding 50 characters for group {0}'.format(str_data1[0][i]))


        base_camp_name = 'Group ' + str(str_data1[0][i]) + ' ' + date + ' ' + 'subgroup' + ' '

        if unique_list:
            loops = math.ceil (len(unique_list)/990)

            for ii in range(loops):

                for j in range(len(bid)):

                    if float(bid[j]) != 0:
                        camp_name = base_camp_name + str(ii+1) + ' ' + epb[j]

                        rows = write_campaign_header(out_worksheet, camp_name, str_data1, i, rows, start_date, end_date,format2)

                        rows = write_campaign_keywords(out_worksheet, camp_name, bid[j], epb[j], unique_list[990*ii:990*ii+990],rows )



    out_workbook.close()

    main()

