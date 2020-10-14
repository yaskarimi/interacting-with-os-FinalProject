import re
import csv
import operator

per_user = {}
error = {}
info_list = []
error_list = []
user_list = []
users = []
line = ["May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (Yasmine)" ,
        "May 27 11:45:40 ubuntu.local ticky: ERROR: Error creating ticket [#1234] (mamad)",
        "May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (mamad)",
        "May 27 11:45:40 ubuntu.local ticky: ERROR: Error example ticket [#1234] (mamad)",
        "May 27 11:45:40 ubuntu.local ticky: ERROR: Error example ticket [#1234] (Yasmine)",
        "May 27 11:45:40 ubuntu.local ticky: ERROR: Error example2 ticket [#1234] (ian)"]
#with open(syslog) as file :
for log in line:
    if re.search(r"ticky: INFO: ([\w ]*) ", log) != None :
      info_list += re.findall(r"ticky: INFO: ([\w ]*) ", log)
    if re.search(r"ticky: ERROR: ([\w ]*) ", log) != None :
      error_list += (re.findall(r"ticky: ERROR: ([\w ]*) ", log))
    users += re.findall(r"\([\w]*\)$" , log)


for usr in users:
    if usr not in user_list or len(user_list) == 0:
        user_list.append(usr)
    continue
user_list.sort()


   # user_list_in.insert(0 , ["Username" , "Info" , "Error"])
def dict_usr(user_list):
    per_user = {}

    for usr in user_list:
        for log in line:
            if usr in log:

                if usr not in per_user.keys():
                 per_user[usr] = {}
                 defaults = ["INFO" , "ERROR"]
                 per_user[usr] = dict.fromkeys(defaults)
                 per_user[usr]["INFO"] = 0
                 per_user[usr]["ERROR"] = 0
                 if re.search(r"ticky: INFO: ([\w ]*) ", log) != None:
                    per_user[usr]["INFO"]=1
                 elif re.search(r"ticky: ERROR: ([\w ]*) ", log) != None :
                    per_user[usr]["ERROR"]=1

                elif usr in per_user.keys():
                    if re.search(r"ticky: INFO: ([\w ]*) ", log) != None:
                     per_user[usr]["INFO"] += 1
                    elif re.search(r"ticky: ERROR: ([\w ]*) ", log) != None:
                     per_user[usr]["ERROR"] += 1


            continue

    return per_user


def dict_er(error_list):
    error_dict = {}
    for er in error_list:
        if er not in error_dict.keys():
         error_dict[er] = 1
        elif er in error_dict.keys():
            error_dict[er] +=1
    sorted_er = sorted(error_dict.items(),  key=operator.itemgetter(1) , reverse=True)
    return sorted_er


def add_csv(er_data , user_data):

    with open( "user_statistics.csv", "w") as file:
       writer = csv.writer(file)
       writer.writerow(["Username" , "INFO" , "ERROR"])
       for key in user_data.keys():
           writer.writerow([key] + [user_data[key]["INFO"]] + [user_data[key]["ERROR"]])


    file.close()

    with open("error_message.csv" , "w") as f :
        writer = csv.writer(f)
        writer.writerow(["ERROR" , "Count"])
        for data in er_data:
            writer.writerow(data)
    f.close()

add_csv(dict_er(error_list) ,  dict_usr(user_list))