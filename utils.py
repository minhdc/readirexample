import os 
import re
import shutil
import setttings
import datetime
import sys
import traceback

from emailclassification import get_eml_header,get_eml_header_value_by_key
from watchdog.observers import Observer
from csvhandle import *

def get_from_address_from_obfuscated_string(input_string):
    if '<' in input_string:
        #return re.findall(r"<(.*?)>",input_string)
        return re.findall(r'[\w\.-]+@[\w\.-]+',input_string)
    else:
        result = []
        result.append(input_string)
        return result


def get_email_address_from_obfuscated_string(input_string):
    #print("raw add input string: ",input_string)
    number_of_email_addr = input_string.count('@')
    #print("number of @ ",number_of_email_addr)
    if number_of_email_addr == 1:
        return get_from_address_from_obfuscated_string(input_string)

    #list_of_addr = re.findall("(?:[a-z0-9!#$%&'*+/=?^_{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",input_string)        
    #list_of_addr = re.findall(r"\A[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",input_string)
    
    #using regex
    list_of_addr = re.findall(r'[\w\.-]+@[\w\.-]+',input_string)
    
    #print("len of list of addr: ", len(list_of_addr))
    
    if len(list_of_addr) != number_of_email_addr:
        print("[DANGER]missing email address....")
    return list_of_addr
    


def create_folder_if_not_exists(parent_path,folder_name):
    try:
        os.makedirs(os.path.join(parent_path, folder_name),exist_ok=True)
    except PermissionError as e:
        print(e)


def copy_eml_file_to_storing_folder(src_included_eml_file_name,dst):
    try:
        shutil.copy(src_included_eml_file_name,dst)      
    except PermissionError as e:
        print(e)


def get_current_dir_list(curren_path):
    result = [os.path.join(curren_path,x) for x in os.listdir(curren_path)]    
    return result


def do_the_classification_job_for_single_eml_file(eml_file_path):
    '''
        sending path: A -> B ---> C
        classified path: C >>>> A >>>> B
    '''    
    dst = os.path.dirname(eml_file_path.replace(setttings.SRC_DIR,setttings.DST_DIR))
    eml_header = get_eml_header(eml_file_path)
    try:    
                   
        print(eml_file_path)
            #get X-Apparently-To address:
        raw_x = get_eml_header_value_by_key(eml_header,"X-Apparently-To")
        x_apparently_to_addr = re.findall(r'[\w\.-]+@[\w\.-]+',raw_x)    
        create_folder_if_not_exists(dst,x_apparently_to_addr[0])
            
            #get From Address:
        from_addr_list = get_eml_header_value_by_key(eml_header,"From")
        from_addr_list = get_from_address_from_obfuscated_string(from_addr_list)        
                

        create_folder_if_not_exists(os.path.join(dst,os.path.join(x_apparently_to_addr[0],os.path.join(from_addr_list[0]))),"Outbox")
        copy_eml_file_to_storing_folder(eml_file_path,os.path.join(os.path.join(dst,os.path.join(x_apparently_to_addr[0],from_addr_list[0])),"Outbox"))        

            #   get To address      - there are many of them.. so we have a LIST   
        to_addr_as_big_string = get_eml_header_value_by_key(eml_header,"To")
        if to_addr_as_big_string is not None:
            to_addr_as_list = get_email_address_from_obfuscated_string(to_addr_as_big_string)    
            for each_address in to_addr_as_list:        
                if from_addr_list[0] == each_address: #create inbox for A Address
                    create_folder_if_not_exists(os.path.join(dst,os.path.join(x_apparently_to_addr[0],from_addr_list[0])),"Inbox") 
                    copy_eml_file_to_storing_folder(eml_file_path,os.path.join(dst,os.path.join(x_apparently_to_addr[0],os.path.join(from_addr_list[0],"Inbox"))))

                write_eml_data_to_csv_file('eml_data.csv',str(eml_file_path).encode('utf-8'),os.path.getsize(eml_file_path),from_addr_list[0],each_address,x_apparently_to_addr[0],str(datetime.datetime.now()))
                try:
                    create_folder_if_not_exists(os.path.join(os.path.join(dst,os.path.join(x_apparently_to_addr[0],os.path.join(from_addr_list[0],"Outbox")))),each_address)
                    copy_eml_file_to_storing_folder(eml_file_path,os.path.join(os.path.join(dst,os.path.join(x_apparently_to_addr[0],os.path.join(from_addr_list[0],"Outbox")),each_address)))
                except FileNotFoundError:
                    print("file name too long...")
                    copy_eml_file_to_storing_folder(eml_file_path,os.path.join(dst,os.path.join(x_apparently_to_addr[0],os.path.join(from_addr_list[0],"Outbox"))))
        else:
            create_folder_if_not_exists(os.path.join(dst,x_apparently_to_addr[0]),"Spam")
            copy_eml_file_to_storing_folder(eml_file_path,os.path.join(dst,os.path.join(x_apparently_to_addr[0],"Spam")))

    except Exception as e:
        create_folder_if_not_exists(dst,"Error_Mail")
        copy_eml_file_to_storing_folder(eml_file_path,os.path.join(dst,"Error_Mail"))
        print(e)
        traceback.print_exc(file=sys.stdout)
        


        #get CC address
        #cc_addr_as_big_string = get_eml_header_value_by_key(eml_header,"CC")
        #if cc_addr_as_big_string is not None:
        #    print("this eml has CC too :3 ")
        #    cc_addr_as_list = get_email_address_from_obfuscated_string(cc_addr_as_big_string)
        #    for each_address in cc_addr_as_list:                
        #        create_folder_if_not_exists(os.path.join(os.path.join(dst,each_address),"Inbox"),from_addr_list[0])
        #       copy_eml_file_to_storing_folder(eml_file_path,os.path.join(os.path.join(os.path.join(dst,each_address),"Inbox"),from_addr_list[0]))
        #else:
        #    print("this eml file doesnt have CC")
        
        print("successfully created and copy eml file: %r to folders" %(eml_file_path))
        setttings.EMAIL_COUNT_FOR_CURRENT_SESSION = setttings.EMAIL_COUNT_FOR_CURRENT_SESSION + 1
        pass


def count_current_email(root_input_path):
    dir_list = get_current_dir_list(root_input_path)
    number_of_emails = 0
    for each_dir in dir_list:
        for each_email_file in os.listdir(each_dir):
            number_of_emails = number_of_emails + 1
    return number_of_emails


def do_the_classification_job(eml_file_path):

    list_of_current_file = get_current_dir_list(eml_file_path)
    print("list of current file ",list_of_current_file)
    #print("list of current eml file",list_of_current_file)
    for each_file in list_of_current_file:
        eml_header = get_eml_header(each_file)

        base_dst_dir_name = os.path.join(setttings.DST_DIR,os.path.basename(os.path.dirname(each_file)))
        print("base dst dir name ",base_dst_dir_name)
        #get From Address:
        from_addr_list = get_eml_header_value_by_key(eml_header,"From")
        print("from addr before clean ",from_addr_list)
        from_addr_list = get_from_address_from_obfuscated_string(from_addr_list)        
        print("from addr after clean ",from_addr_list)
        print("file name ",each_file)
        create_folder_if_not_exists(base_dst_dir_name,from_addr_list[0])
        create_folder_if_not_exists(os.path.join(base_dst_dir_name,from_addr_list[0]),"Outbox")
        copy_eml_file_to_storing_folder(each_file,os.path.join(os.path.join(base_dst_dir_name,from_addr_list[0]),"Outbox"))

        #get To address
        to_addr_as_big_string = get_eml_header_value_by_key(eml_header,"To")
        to_addr_as_list = get_email_address_from_obfuscated_string(to_addr_as_big_string)    
        for each_address in to_addr_as_list:
            create_folder_if_not_exists(base_dst_dir_name,each_address)
            create_folder_if_not_exists(os.path.join(base_dst_dir_name,each_address),"Inbox")
            copy_eml_file_to_storing_folder(each_file,os.path.join(os.path.join(base_dst_dir_name,each_address),"Inbox"))


        #get CC address
        cc_addr_as_big_string = get_eml_header_value_by_key(eml_header,"To")
        cc_addr_as_list = get_email_address_from_obfuscated_string(cc_addr_as_big_string)
        for each_address in cc_addr_as_list:
            create_folder_if_not_exists(base_dst_dir_name,each_address)
            create_folder_if_not_exists(os.path.join(base_dst_dir_name,each_address),"Inbox")
            copy_eml_file_to_storing_folder(each_file,os.path.join(os.path.join(base_dst_dir_name,each_address),"Inbox"))

        print("successfully created and copy eml file: %r to folders" %(eml_file_path))

