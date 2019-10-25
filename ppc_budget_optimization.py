#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Imran Hameed
#
# Created:     08/25/2019
#-------------------------------------------------------------------------------

##Budget Adjustment script
##  Old  algorithem
##Acos < 25%, order >=5, increase budget by 30%
##25 <= Acos < 40 , order >=5, increase budget by 10%
##40 <= Acos < 60 ,  floor budget to $20 if order >=5 otherwise small(20,0.8*current budget)
##60 <= Acos < 100 , order >=5, decrease budget by 25%
##60 <= Acos < 100 , order < 5, decrease budget by 50%
## New algorithm
## For orders >=5
## if acos <= 20, increase budget by 25%
## if 20 < acos <= 60, change budget by -5/4*acos+50
##  60 < acos <= 100, change budget by -15/40*acos - 2.5
## acos > 100 decrease budget by 50%
## for order < 5 and acos > 60%, reduce budget by 50%
## ceil budget for acos > 40% to $20

##Acos > 100, decrease budget by 50%
##Order = 0, spend > 40 , decrease budget by 70%
##Order = 0, spend > 15 , decrease budget by 50%
##Order = 0, spend > 7 , decrease budget by 25%


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

def budget_bounds(after_change_budget):

    if after_change_budget > 1000:
        print ('hitting budget ceiling')
        after_change_budget = 1000.0
    if after_change_budget < 5:
##        print ('hitting budget floor')
        after_change_budget = 5.0

    return round(after_change_budget,2)

def calculate_change_factor(acos):
    if acos <= 0.2:
        y = 0.25
    elif acos <= 0.6:
        y = (-5/4*acos*100 + 50) / 100
    elif acos <= 1:
        y = (-25/40*acos*100 + 12.5 )/100
    else:
        y = -0.5

    change_factor = y + 1
    return change_factor

def main():
    print ("Exiting Main")
    pass

if __name__ == '__main__':
    workbook = open_excel_for_read('bulk_file_location')
    bulk_data = read_all_rows_cols(workbook,'Sponsored Products Campaigns')


    date = datetime.datetime.now().strftime("%m%d%Y")

    b4_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_budget_optimization_b4_change_' + date + '.xlsx'
    after_change = configuration_file.FILE_LOCATION['upload_file_location']  \
    + configuration_file.account_name + '_budget_optimization_after_change_' + date + '_upload.xlsx'

    out_workbook1 = xlsxwriter.Workbook(b4_change)
    out_worksheet1 = out_workbook1.add_worksheet()

    out_workbook2 = xlsxwriter.Workbook(after_change)
    out_worksheet2 = out_workbook2.add_worksheet()
    row = 0


    for i,val in enumerate(bulk_data):

        budget_changed = 0
        after_change_budget = 0.0

        if i == 0:
            out_worksheet1.write_row(row,0,val)
            out_worksheet2.write_row(row,0,val)
            row = row + 1
            continue

        if val[1] == 'Campaign':
            if int(val[21]) == 0:
                if float(val[20]) >= 40:
                    after_change_budget = float(val[4]) * 0.3
                    budget_changed = 1
                elif float(val[20]) >= 15:
                    after_change_budget = float(val[4]) * 0.5
                    budget_changed = 1
                elif float(val[20]) >= 7:
                    after_change_budget = float(val[4]) * 0.70
                    budget_changed = 1
            else:
                acos = float(val[20])/float(val[23])
                if (int(val[21]) >= 5):
                    change_factor = calculate_change_factor(acos)
                    after_change_budget = round(float(val[4]) * change_factor,2)
                    budget_changed = 1
                    if acos < 0.4 and after_change_budget < 20:
                        after_change_budget = 20
                else:
                    if acos >= 0.6:
                        after_change_budget = round(float(val[4]) * 0.5,2)
                        budget_changed = 1

                if acos >= 0.4 and  int(val[21]) < 30:
                    if budget_changed == 1 :
                        if after_change_budget > 20:
                            after_change_budget = 20
                    else :
                        if float(val[4]) > 20:
                            after_change_budget = 20
                            budget_changed = 1

            start_date = val[6]
            start_date_obj = datetime.datetime.strptime(start_date,'%m/%d/%Y')
            todays_date = datetime.datetime.now()
            delta = todays_date - start_date_obj
            if val[15] == 'enabled':
                if delta.days > 120 :
                    if (int(val[21]) >= 1):
                        acos = float(val[20])/float(val[23])
                        if acos > 1:
                            out_worksheet1.write_row(row,0,val)
                            val[15] = 'paused'
                            out_worksheet2.write_row(row,0,val)
                            row = row + 1
                            budget_changed = 0
                            print ('Pausing Campaign: {0}'.format(val[3]))


        if (budget_changed == 1) and (float(val[4]) != after_change_budget):

            after_change_budget = budget_bounds (after_change_budget)
            if float(val[4]) != after_change_budget :
                out_worksheet1.write_row(row,0,val)
                val[4] = str(after_change_budget)
                out_worksheet2.write_row(row,0,val)
                row = row + 1

    out_workbook1.close()
    out_workbook2.close()


    main()

