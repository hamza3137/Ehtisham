#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     08/25/2019
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


def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook,'Sponsored Products Campaigns')


    date = datetime.datetime.now().strftime("%m%d%Y")

    output_file = configuration_file.base_file_location \
    + configuration_file.account_name + '_campaign_placement_stats_' + date + '.xlsx'


    out_workbook1 = xlsxwriter.Workbook(output_file)
    out_worksheet1 = out_workbook1.add_worksheet()

    row = 0
    col = 0
    out_worksheet1.write(row,col,'Campaign Name')
    out_worksheet1.write(row,col+1,'Acos')
    out_worksheet1.write(row,col+2,'Orders')
    out_worksheet1.write(row,col+3,'Top Search Acos')
    out_worksheet1.write(row,col+4,'Top Search Orders')
    out_worksheet1.write(row,col+5,'Rest of page Acos')
    out_worksheet1.write(row,col+6,'Rest of page Orders')
    out_worksheet1.write(row,col+7,'Product page Acos')
    out_worksheet1.write(row,col+8,'Product page Orders')
    row = row + 1

    campaign_data = [0]*9
    campaign_name = ''

    for i,val in enumerate(bulk_data):


        if val[1] == 'Campaign':
            if campaign_data:
                if campaign_data[0] != 0:
                    out_worksheet1.write_row(row,0,campaign_data)
                    row = row + 1
                campaign_data = [0]*9
            if int(val[21]) >= 1:
                campaign_name = val[3]
                acos = float(val[20])/float(val[23])
                campaign_data[0] = val[3]
                campaign_data[1] = round (acos * 100, 2)
                campaign_data[2] = int(val[21])

        if val[1] =='Campaign By Placement' and val[3] == campaign_name:
            if int(val[21]) >= 1:
                if val[26] == 'Top of search (page 1)':
                    acos = float(val[20])/float(val[23])
                    campaign_data[3] = round (acos * 100, 2)
                    campaign_data[4] = int(val[21])

                elif val[26] == 'Rest of search':
                    acos = float(val[20])/float(val[23])
                    campaign_data[5] = round (acos * 100, 2)
                    campaign_data[6] = int(val[21])


                elif val[26] == 'Product pages':
                    acos = float(val[20])/float(val[23])
                    campaign_data[7] = round (acos * 100, 2)
                    campaign_data[8] = int(val[21])


    out_workbook1.close()


    main()

