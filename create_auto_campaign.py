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

def create_file_header(out_worksheet,rows):

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
    return rows

def check_max_bid_limit (bid , max_bid):
    temp_list = list()

    for i in range(len(bid)):
        temp = bid[i]
        if float(temp) > max_bid:
            temp = str(max_bid)
        temp_list.append(temp)

    return temp_list

def write_campaign_header(out_worksheet, camp_name, bid, budget, sku, rows, start_date, end_date,format2):

    out_worksheet.write(rows,1, 'Campaign')

    out_worksheet.write(rows,3, camp_name)
    if budget:
        out_worksheet.write(rows,4,budget)
    else:
        out_worksheet.write(rows,4,8)
    out_worksheet.write(rows,5,start_date,format2)
    out_worksheet.write(rows,6,end_date,format2)
    out_worksheet.write(rows,7,"Auto")
    out_worksheet.write(rows,15,"Enabled")
    rows = rows + 1
    ad_group_name = camp_name

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

def write_campaign_keywords(out_worksheet, camp_name, campaign_for, unique_list,rows ):
    ad_group_name = camp_name

    for jj in range(len(unique_list)):
        out_worksheet.write(rows,1, 'Product Targeting')
        out_worksheet.write(rows,3, str(camp_name))
        out_worksheet.write(rows,9, str(ad_group_name))
        out_worksheet.write(rows,11, unique_list[jj])
        out_worksheet.write(rows,12, unique_list[jj])
        out_worksheet.write(rows,13, 'Targeting Expression Predefined')
        if campaign_for == unique_list[jj]:
            out_worksheet.write(rows,17, "Enabled")
        else:
            out_worksheet.write(rows,17, "Paused")
        rows = rows + 1

    return rows


def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':

    unique_list = ['close-match', 'loose-match', 'complements', 'substitutes']

    high_bid = 1.76
    median_bid = 1.53
    low_bid = 1.13
    sku_name = 'HydratingScrub'
    searchable_name = 'HydratingScrub'

    date = datetime.datetime.now().strftime("%m%d%Y")
    start_date = datetime.datetime.now().strftime("%m/%d/%Y")
    end_date = ''
    upload_file_name = configuration_file.base_file_location \
    + configuration_file.account_name + '_auto_campaign_for_'+ sku_name + '.xlsx'

    out_workbook = xlsxwriter.Workbook(upload_file_name)
    out_worksheet = out_workbook.add_worksheet()
    format2 = out_workbook.add_format({'num_format': 'mm/dd/yy'})

    rows = 0
    rows = create_file_header(out_worksheet,rows)


    for i in range(0,len(unique_list)):

        camp_name = sku_name + ' auto 1 ' + unique_list[i] + ' ' + date + ' ' + searchable_name
        rows = write_campaign_header(out_worksheet, camp_name, high_bid, 12, sku_name , rows, start_date, end_date,format2)
        rows = write_campaign_keywords(out_worksheet, camp_name, unique_list[i], unique_list,rows )

        camp_name = sku_name + ' auto 2 ' + unique_list[i] + ' ' + date + ' ' + searchable_name
        rows = write_campaign_header(out_worksheet, camp_name, median_bid, 8, sku_name , rows, start_date, end_date,format2)
        rows = write_campaign_keywords(out_worksheet, camp_name, unique_list[i], unique_list,rows )

        camp_name = sku_name + ' auto 3 ' + unique_list[i] + ' ' + date + ' ' + searchable_name
        rows = write_campaign_header(out_worksheet, camp_name, low_bid, 8, sku_name , rows, start_date, end_date,format2)
        rows = write_campaign_keywords(out_worksheet, camp_name, unique_list[i], unique_list,rows )

    out_workbook.close()

    main()

