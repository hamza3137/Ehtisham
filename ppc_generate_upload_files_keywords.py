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
    0 : 'Exact',
    1 : 'Phrase',
    2 : 'Broad',
}

ignore_strs_list = ['.','™', 'ō','-','/',',','\'','ģ','%','_','’','|','+','$','ã','‘',\
')','(','\\',':','®','?','º','"',]

def open_excel_for_read(file_location):
    print ('Opening file {0} .....'.format(configuration_file.FILE_LOCATION[file_location]))
    workbook = xlrd.open_workbook(configuration_file.FILE_LOCATION[file_location])
    return workbook

def read_all_rows_cols (workbook,by_name):
    try:
        if by_name:
            str_worksheet = workbook.sheet_by_name(configuration_file.account_name.upper())
        else:
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
                if temp[j] not in unique_words:
                    unique_words.append(temp[j])

    return unique_words

def de_duplicate(str_data1 , str_data2 , str_data3, i ):
    search_name = str_data1[1][i]
    temp_list = list() # List that will be reference for dedupe
    unique_list = list()

    if str_data1[2][i] == 'sp suggested' :
        for j in range(len(str_data2)):
            if search_name.lower() in str_data2[j][5].lower():
                if int(str_data2[j][9]) >= 1:
                    temp_list.append(str_data2[j][6])
    elif str_data1[2][i] == 'pcst':
        for j in range(len(str_data3)):
            if search_name.lower() in str_data3[j][5].lower():
                if int(str_data3[j][20]) >= 3:
                    temp_list.append(str_data3[j][6])
    elif str_data1[2][i] == 'tcst':
        for j in range(len(str_data3)):
            if search_name.lower() in str_data3[j][5].lower():
                if int(str_data3[j][20]) >= 1:
                    temp_list.append(str_data3[j][6])
    else: # From Self Cerebro or any other data that has less confidence
        for j in range(len(str_data3)):
            if search_name.lower():
                if search_name.lower() in str_data3[j][5].lower():
                    #print (search_name.lower())
                    #print (str_data3[j][9])
                    #print (str_data3[j][5].lower())
                    if str_data3[j][9]:
                        if int(str_data3[j][9]) >= 1:
                            temp_list.append(str_data3[j][6])


    for j in range(7,len(str_data1)):
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
                        unique_list.append(str_data1[j][i])

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

def calculate_bids_for_campaigns(str_data1 , str_data3 , i):
    bid = list()
    search_name = str_data1[1][i]
    ref_data = str_data1[2][i]
    enhance_multiplier = configuration_file.enhance_bid_multiplier

    if ref_data == 'sp suggested' or ref_data == 'pcst':
        cpc = calculate_bid_for_exact(search_name,str_data3)
        bid.append ( round ( enhance_multiplier * cpc , 2 ) )
        bid.append ( round ( enhance_multiplier * cpc * 0.9 , 2 ) )
        bid.append ( round ( enhance_multiplier * cpc * 0.9 * 0.75 , 2 ) )

    elif ref_data == 'tcst':
        cpc = calculate_bid_for_exact(search_name,str_data3)
        bid.append ( 0 )
        bid.append ( round ( cpc * 0.9 * 0.9 , 2 ) )
        bid.append ( round ( cpc * 0.9 * 0.9 * 0.75 , 2 ) )

    elif ref_data == 'gp':
        bid.append(0)
        bid.append(0.27)
        bid.append(0.27)

    else:
        # all other cases like self cerebro for mining new keywords perspective
        bid.append(0)
        bid.append(0.51)
        bid.append(0.51)

    return bid

def check_max_bid_limit (bid , max_bid):
    temp_list = list()

    for i in range(len(bid)):
        temp = bid[i]
        if float(temp) > max_bid:
            temp = str(max_bid)
        temp_list.append(temp)

    return temp_list

def write_campaign_header(out_worksheet, camp_name, ii, bid, budget, sku, rows, start_date, end_date,format2):

    if ii == 0 :
        out_worksheet.write(rows,1, 'Campaign')

        out_worksheet.write(rows,3, camp_name)
        if budget:
            out_worksheet.write(rows,4,budget)
        else:
            out_worksheet.write(rows,4,20)
        out_worksheet.write(rows,5,start_date,format2)
        out_worksheet.write(rows,6,end_date,format2)
        out_worksheet.write(rows,7,"Manual")
        out_worksheet.write(rows,15,"Enabled")
        rows = rows + 1
        ad_group_name = camp_name
    else:
        ad_group_name = camp_name + ' ' + str(ii)
##    print ('loop number = {0},ad group name is {1}'.format(ii,ad_group_name))
    out_worksheet.write(rows,1, 'AdGroup')
    out_worksheet.write(rows,3, camp_name)
    out_worksheet.write(rows,9, ad_group_name)
    out_worksheet.write_number(rows,10, float(bid) )
    out_worksheet.write(rows,16, "Enabled")
    rows = rows + 1

    if type(sku) is float:
        sku = str(int(sku))
    out_worksheet.write(rows,1, 'Ad')
    out_worksheet.write(rows,3, camp_name)
    out_worksheet.write(rows,9, ad_group_name)
    out_worksheet.write(rows,14, sku)
    out_worksheet.write(rows,17, "Enabled")
    rows = rows + 1

    return rows

def write_campaign_keywords(out_worksheet, camp_name, ii, epb, unique_list,rows,low_performing_kws,bid ):
    if ii == 0 :
        ad_group_name = camp_name
    else:
        ad_group_name = camp_name + ' ' + str(ii)

    bad_keyword_max_bid = configuration_file.bad_keyword_max_bid

    for jj in range(len(unique_list)):
        out_worksheet.write(rows,1, 'Keyword')
        out_worksheet.write(rows,3, str(camp_name))
        out_worksheet.write(rows,9, str(ad_group_name))
        out_worksheet.write(rows,11, unique_list[jj])

        if float(bid) > bad_keyword_max_bid:
            for kk in range(len(low_performing_kws)):
                if unique_list[jj] == low_performing_kws[kk]:
                    print ('low performing keyword detected: {0}'.format(low_performing_kws[kk]))
                    out_worksheet.write(rows,10, bad_keyword_max_bid)
        out_worksheet.write(rows,13, epb)
        out_worksheet.write(rows,17, "Enabled")
        rows = rows + 1

    return rows

def get_low_performing_kws_list(str_data4, sku):
    kws_list = list()

    if str_data4:
        for i in range(len(str_data4[0])):
            if sku == str_data4[1][i]:
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
    workbook1 = open_excel_for_read('keywords_to_add_file')
    str_data1 = read_all_rows_cols(workbook1,0)
    workbook2 = open_excel_for_read('target_file_location')
    str_data2 = read_all_rows_cols(workbook2,0)
    workbook3 = open_excel_for_read('str_file_location')
    str_data3 = read_all_rows_cols(workbook3,0)
    workbook4 = open_excel_for_read('low_bid_keywords_asins')
    str_data4 = read_all_rows_cols(workbook4,1)
    products = configuration_file.PRODUCTS
    date = datetime.datetime.now().strftime("%m%d%Y_%H%M")

    upload_file_name = configuration_file.FILE_LOCATION['upload_file_location'] \
    + configuration_file.account_name + '_keywords_' + date + '_upload.xlsx'

    date = datetime.datetime.now().strftime("%m%d%Y")

    out_workbook = xlsxwriter.Workbook(upload_file_name)
    out_worksheet = out_workbook.add_worksheet()
    format2 = out_workbook.add_format({'num_format': 'mm/dd/yy'})
    rows = 0
    cols = 0

    out_worksheet.write(rows,cols, 'Record ID')
    cols = cols + 1
    out_worksheet.write(rows,cols, 'Record Type')
    cols = cols + 1
    out_worksheet.write(rows,cols, 'Campaign ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Daily Budget')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Start Date')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign End Date')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Targeting Type')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Portfolio ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Ad Group Name')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Max Bid')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Keyword or Product Targeting')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Product Targeting ID')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Match Type')
    cols = cols + 1
    out_worksheet.write(rows,cols,'SKU')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Campaign Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Ad Group Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Status')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Bidding strategy')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Placement Type')
    cols = cols + 1
    out_worksheet.write(rows,cols,'Increase bids by placement')
    rows = rows + 1


    for i in range(1,len(str_data1[0])):
        unique_list = de_duplicate(str_data1 , str_data2 , str_data3, i )
        #print (str_data1[3][i])
        if str_data1[3][i]:
            bid = str_data1[3][i].split(',')
        else:
            bid = calculate_bids_for_campaigns(str_data1 , str_data3, i)
        if len(bid) != 3:
            exit('bid array length in not 3, check !!!')
        if configuration_file.max_bid_limit_set:
            bid = check_max_bid_limit (bid , configuration_file.max_bid)

        budget = str_data1[4][i]
        sku_name = str_data1[0][i]
        if str_data1[5][i]:
            start_date = str_data1[5][i]
        else:
            start_date = datetime.datetime.now().strftime("%m/%d/%Y")
        end_date = str_data1[6][i]
        if not str_data1[2][i]:
            exit('No reference source mentioned, please check column {0}'.format(i+1))

        low_performing_kws = get_low_performing_kws_list(str_data4, sku_name)

        base_camp_name = str(str_data1[0][i]) + ' ' + str_data1[2][i] + ' ' + date + ' ' + str_data1[1][i] + ' '
        #base_camp_name = str(str_data1[0][i]) + ' ' + str_data1[2][i] + ' ' +  '08122019 ' + str_data1[1][i] + ' '

        #print ('base camp name = {0}'.format(base_camp_name))

        if unique_list:
            loops = math.ceil (len(unique_list)/990)

            for ii in range(loops):
                for j in range(len(bid)):

                    if float(bid[j]) != 0:
                        camp_name = base_camp_name + epb[j]
                        #print ('camp name before passing = {0}'.format(camp_name))

                        rows = write_campaign_header(out_worksheet, camp_name, ii, bid[j], budget, sku_name, rows, start_date, end_date,format2)

                        rows = write_campaign_keywords(out_worksheet, camp_name, ii, epb[j], unique_list[990*ii:990*ii+990],rows,low_performing_kws,bid[j] )



    out_workbook.close()

    main()

