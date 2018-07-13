import csv
from pathlib import Path
import pandas as pd

def init_csv_file(csv_filename_as_path):
    with open(csv_filename_as_path,"w") as csvfile:
        fieldnames = ['eml_file_name','size','a_address','b_address','c_address','date']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writeheader()


def write_eml_data_to_csv_file(csv_filename_as_path,eml_file_name,size,a_address,b_address,c_address,date):
    '''
        write eml_data to csv_file
    '''    
    if not Path(csv_filename_as_path).is_file():
        init_csv_file(csv_filename_as_path)   
    
    with open(csv_filename_as_path,'a',encoding="utf-8-sig") as csvfile:
        fieldnames = ['eml_file_name','size','a_address','b_address','c_address','date']                 
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        #writer.writeheader()
        writer.writerow({'eml_file_name':eml_file_name,'size':size,'a_address':a_address,'b_address':b_address,'c_address':c_address,'date':date})
        #print(eml_file_name)
        

def get_all_row_in_csv(csv_filename_as_path,fieldnames):
    result = []
    with open(csv_filename_as_path) as csvfile:
        reader = csv.DictReader(csvfile)        
        for row in reader:
            result.append(row)
    return result

        
def get_row_by_fieldname_in_csv(csv_filename_as_path,single_field_name):
    result = []
    with open(csv_filename_as_path) as csvfile:
        reader = csv.DictReader(csvfile,fieldnames=single_field_name)
        for row in reader:
            result.append(row)
    return result


def get_outbox_relation_per_day(dataframe,d_m_y_as_string):
    '''
        return a Series with index = a_address and corresponding list of b_address
    '''
    return dataframe[dataframe['date']==d_m_y_as_string].groupby('a_address')['b_address'].apply(list)


def get_outbox_email_list_per_day(dataframe,d_m_y_as_string,a_address,b_address):
    '''
        return a series of eml_file_name corresponding to a_address and b_address
    '''
    return dataframe[(dataframe['a_address'] == a_address) & (dataframe['b_address'] == b_address) & (dataframe['date'] == d_m_y_as_string)]['eml_file_name']


def get_total_mail_of_a_address(dataframe,d_m_y_as_string):
    '''
        return a Series with index = a_address, and corresponding eml_file_name as list
    '''
    return dataframe[dataframe['date']==d_m_y_as_string].groupby('a_address')['eml_file_name'].apply(list)


def get_total_mail_of_b_address(dataframe,d_m_y_as_string):
    '''
        return a Series with index = b_address, and corresponding eml_file_name as list
    '''
    return dataframe[dataframe['date']==d_m_y_as_string].groupby('b_address')['eml_file_name'].apply(list)

