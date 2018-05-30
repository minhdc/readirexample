import csv

def init_csv_file(csv_filename_as_path):
    with open(csv_filename_as_path,"w") as csvfile:
        fieldnames = ['eml_file_name','size','a_address','b_address','c_address','date']
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        writer.writeheader()


def write_eml_data_to_csv_file(csv_filename_as_path,eml_file_name,size,a_address,b_address,c_address,date):
    if csv.Sniffer().has_header(csv_filename_as_path):
        print("has header")
    with open(csv_filename_as_path,'a') as csvfile:
        fieldnames = ['eml_file_name','size','a_address','b_address','c_address','date']                 
        writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
        #writer.writeheader()
        writer.writerow({'eml_file_name':eml_file_name,'size':size,'a_address':a_address,'b_address':b_address,'c_address':c_address,'date':date})
        

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


#init_csv_file('names.csv')
#write_eml_data_to_csv_file('names.csv','','','','','','')
#write_eml_data_to_csv_file('names.csv','1','1','1','1','1','1')
#write_eml_data_to_csv_file('names.csv','1','1','1','1','1','1')
#write_eml_data_to_csv_file('names.csv','2','2','2','2','12','12')
#write_eml_data_to_csv_file('names.csv','18','17','16','14','14','13')
