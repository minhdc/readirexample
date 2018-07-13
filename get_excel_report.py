import setttings 
import xlsxwriter
import datetime
import os 
import pandas as pd
import logging


from pathlib import Path
from time import sleep

from csvhandle import get_outbox_email_list_per_day,get_outbox_relation_per_day
from csvhandle import get_total_mail_of_a_address,get_total_mail_of_b_address
from displayutils import printProgressBar


##logging config
logging.basicConfig(filename='excel_report.log',level=logging.INFO)
print("inited logger")
####################initialization
try:
    email_count = 0
    file_name = setttings.EXCEL_FILE_LOC+"Báo cáo NGK ngày "+setttings.CURRENT_DAY+setttings.EXCEL_EXTENSION
    date = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().year) 
    eml_csv = ''
    outbox_rela_as_series = pd.Series()

    try:
        eml_csv = pd.read_csv(os.path.join(setttings.CSV_FILE_LOC,'eml_data'+setttings.CURRENT_DAY+setttings.CSV_EXTENSION),sep=",")
        eml_csv = eml_csv.drop_duplicates(subset=['eml_file_name','a_address','b_address'])    
        #extension = '.txt'
        outbox_rela_as_series = get_outbox_relation_per_day(eml_csv,date)
    except FileNotFoundError as e:
        print("\n\nChưa có file .csv của ngày hôm nay\n\n")  
        exit(1)      



    #create workbook & wo3rksheet
    workbook = xlsxwriter.Workbook(file_name)
    main_worksheet = workbook.add_worksheet("Tổng quan")
    a_address_worksheet = workbook.add_worksheet("Đối tượng gửi")
    b_address_worksheet = workbook.add_worksheet("Đối tượng nhận")
    #formatting stuffs
    bold = workbook.add_format({'bold':1})
    money_format = workbook.add_format({'num_format':'$#,##0'})
    date_format = workbook.add_format({'num_format':'dd mm yyyy'})

    #create format in merged range  
    merge_format = workbook.add_format({
        'bold'      : 1,
        'border'    : 1,
        'align'     : 'center',
        'valign'    : 'vcenter',
        'fg_color'  : '#a0d0db'
    })
    from_format = workbook.add_format({
        'bold'      : 1,
        'border'    : 1,
        'align'     : 'center',
        'valign'    : 'vcenter',    
        'fg_color'  : '#dfda41'
    })
    to_format = workbook.add_format({
        'bold'      : 1,
        'border'    : 1,
        'align'     : 'center',
        'valign'    : 'vcenter',    
        'fg_color'  : '#00ced8'
    })
    number_of_mails_format = workbook.add_format({
        'bold'      : 1,
        'border'    : 1,
        'align'     : 'center',
        'valign'    : 'vcenter',    
        'fg_color'  : '#e68484'
    })
    location_format = workbook.add_format({
        'bold'      : 1,
        'border'    : 1,
        'align'     : 'center',
        'valign'    : 'vcenter',    
        'fg_color'  : '#a8d8ba'
    })

    #header
    main_worksheet.write('A1','Địa chỉ gửi',from_format)
    main_worksheet.write('B1','Địa chỉ nhận',to_format)
    main_worksheet.write('C1','Số lượng thư',number_of_mails_format)
    main_worksheet.write('D1','Vị trí lưu trữ trên máy',location_format)
    main_worksheet.freeze_panes(1,0)
    row = 1
    col = 0

    #adjust columns width
    main_worksheet.set_column('A1:B1',30)
    main_worksheet.set_column('C1:C1',15)
    main_worksheet.set_column('D1:D1',180)
    main_worksheet.set_row(0,40)

    #print(outbox_rela_as_series)

    #initProgressBar
    printProgressBar(0,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)
    for i in range(0,len(outbox_rela_as_series)):
        for each_b_addr in outbox_rela_as_series[i]:
            start_pos = row
            
            main_worksheet.write(row,col,outbox_rela_as_series.index[i],from_format)
            col += 1
            main_worksheet.write(row,col,each_b_addr,to_format)
            col += 1
            main_worksheet.write(row,col,len(get_outbox_email_list_per_day(eml_csv,date,outbox_rela_as_series.index[i],each_b_addr)),number_of_mails_format)
            col += 1
            for each_mail in get_outbox_email_list_per_day(eml_csv,date,outbox_rela_as_series.index[i],each_b_addr):
                main_worksheet.write_url(row,col,each_mail)
                row += 1
            stop_pos = row-1
            col = 0
            row += 1
            main_worksheet.merge_range(start_pos,0,stop_pos,0,outbox_rela_as_series.index[i],from_format)
            main_worksheet.merge_range(start_pos,1,stop_pos,1,each_b_addr,to_format)
            main_worksheet.merge_range(start_pos,2,stop_pos,2,
                len(get_outbox_email_list_per_day(eml_csv,date,outbox_rela_as_series.index[i],
                each_b_addr)),number_of_mails_format)
#            main_worksheet.merge_range(start_pos)
        row += 1
        col = 0
        printProgressBar(i+1,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)
    row += 1
    col = 0

    ###########################
    ###########write sheet for a_address
    email_series_for_a_addr = get_total_mail_of_a_address(eml_csv,date)
    #print(email_series_for_a_addr)
    row = 1
    col = 0
    printProgressBar(0,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)
    for i in range(0,len(email_series_for_a_addr)):
        #remove duplicates in list 
        email_series_for_a_addr[i] = list(set(email_series_for_a_addr[i]))
        a_address_worksheet.write(row,col,email_series_for_a_addr.index[i],from_format)
        col += 1
        a_address_worksheet.write(row,col,len(email_series_for_a_addr[i]),number_of_mails_format)
        col += 1
        #row += 1
        start_pos = row    
        for each_mail in email_series_for_a_addr[i]:        
            a_address_worksheet.write_url(row,col,each_mail)
            row += 1
        stop_pos = row-1      
        col = 0
        #row += 1
        a_address_worksheet.merge_range(start_pos,0,stop_pos,0,email_series_for_a_addr.index[i],from_format)
        a_address_worksheet.merge_range(start_pos,1,stop_pos,1,len(email_series_for_a_addr[i]),number_of_mails_format)
        #reset
        col = 0
        printProgressBar(i+1,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)

    a_address_worksheet.set_column('A1:B1',30)
    a_address_worksheet.set_column('C1:C1',180)
    a_address_worksheet.set_row(0,40)

    a_address_worksheet.write('A1','Địa chỉ gửi',from_format)
    a_address_worksheet.write('B1','Số lượng thư',number_of_mails_format)
    a_address_worksheet.write('C1','Vị trí lưu trữ trên máy',location_format)



    ###########################
    ###########write sheet for b_address
    email_series_for_b_addr = get_total_mail_of_b_address(eml_csv,date)
    row = 1
    col = 0
    #printProgressBar(0,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)
    for i in range(0,len(email_series_for_a_addr)):
        b_address_worksheet.write(row,col,email_series_for_b_addr.index[i],to_format)
        col += 1
        b_address_worksheet.write(row,col,len(email_series_for_b_addr[i]),number_of_mails_format)
        col += 1
        #row += 1
        start_pos = row    
        for each_mail in email_series_for_b_addr[i]:        
            b_address_worksheet.write_url(row,col,each_mail)
            row += 1
        stop_pos = row-1        
        col = 0
        #row += 1
        b_address_worksheet.merge_range(start_pos,0,stop_pos,0,email_series_for_b_addr.index[i],to_format)
        b_address_worksheet.merge_range(start_pos,1,stop_pos,1,len(email_series_for_b_addr[i]),number_of_mails_format)
        #reset
        col = 0
        #printProgressBar(i+1,len(outbox_rela_as_series),prefix="Tiến độ:",length=50)

    b_address_worksheet.set_column('A1:B1',30)
    b_address_worksheet.set_column('C1:C1',180)
    b_address_worksheet.set_row(0,40)

    b_address_worksheet.write('A1','Địa chỉ nhận',from_format)
    b_address_worksheet.write('B1','Số lượng thư',number_of_mails_format)
    b_address_worksheet.write('C1','Vị trí lưu trữ trên máy',location_format)


    workbook.close()

    print(r"---------------------------------------------------------------")
    print(r"  _____ ____  __  __ _____  _      ______ _______ ______ _____")
    print(r"/ ____// __ \|  \/  |  __ \| |    |  ____|__   __|  ____|  __\\")
    print(r"| |   | |  | | \  / | |__) | |    | |__     | |  | |__  | |  | |")
    print(r"| |   | |  | | |\/| |  ___/| |    |  __|    | |  |  __| | |  | |")
    print(r"| |___| |__| | |  | | |    | |____| |____   | |  | |____| |__| |")
    print(r" \_____\____/|_|  |_|_|    |______|______|  |_|  |______|_____/ ")
    print(r"---------------------------------------------------------------")     
                                                            
    
    print("\n\nHoàn thành! Nhấn phím bất kỳ để thoát...\n\n")
    input()
except Exception as e:
    logging.error('[ERROR] ' + str(e))
    logging.traceback.print_stack()