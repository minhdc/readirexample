import datetime
import setttings
import pandas as pd

from csvhandle import get_outbox_relation_per_day,get_outbox_email_list_per_day


eml_csv = pd.read_csv('eml_data'+setttings.CURRENT_DAY+setttings.CSV_EXTENSION,sep=",")

eml_csv = eml_csv.drop_duplicates(subset=['eml_file_name','a_address','b_address'])
print(eml_csv['date'])

pd.set_option('display.max_colwidth',-1)
date = str(datetime.datetime.now().day) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().year) 
extension = '.txt'
outbox_rela_as_series = get_outbox_relation_per_day(eml_csv,date)

email_count = 0
file_name = "report_example"+setttings.CURRENT_DAY+setttings.CSV_EXTENSION


with open(file_name,"w",encoding="utf-8-sig") as report:
    for i in range(0,len(outbox_rela_as_series)):
        for each_b_addr in outbox_rela_as_series[i]:
            print("==== emails from :<%r> to <%r>:"%(outbox_rela_as_series.index[i],each_b_addr))
            print(get_outbox_email_list_per_day(eml_csv,date,outbox_rela_as_series.index[i],each_b_addr))
            report.write("== emails from :<%r> to <%r>:"%(outbox_rela_as_series.index[i],each_b_addr))
            for each in get_outbox_email_list_per_day(eml_csv,date,outbox_rela_as_series.index[i],each_b_addr):
                report.write("\n\t--"+each)
                email_count += 1
            report.write("\n==>TOTAL: %d emails\n\n"%(email_count))
            email_count = 0
    
report.close()
print("success")