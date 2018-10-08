import csv
import requests
import re


config = '''
  _____               _  _   
 |_   _|            _| || |_ 
   | |  _ __  _ __ |_  __  _|
   | | | '_ \| '_ \ _| || |_ 
  _| |_| | | | | | |_  __  _|
 |_____|_| |_|_| |_| |_||_|  
 Import your CSV phonebook to
 your Innovaphone PBX.
 Author: Sebastian Perske
 https://github.com/perskes
 Version: 1.0
 ================================
 Please enter the required Infos.
        '''
print(config)
csvFile = input("Global Path to CSV-File (default: .\list.csv): ") or "list.csv"
#csvFile = "C:\\Users\\s.perske\\PycharmProjects\\innoToolkit\\list.csv"
delimiter = input("Delimiter (default: ;): ") or ";"
#delimiter = ";"

#innovaphoneIP = "http://192.168.100.1"
innovaphoneIP = input("Innovaphone IP http://... (default: http://192.168.100.1):") or "http://192.168.100.1"

pbxAdmin = input("Username (pbx-admin): ")
pbxPass = input("Password: ")


longName = "&cn"
displayName = "&dn"
name = "&h323"
number = "&e164"
description = "&text"
email = "&email"
sendEMail = "&h323-email"
password = "&pwd"
passwordConfirm = "&pwd1"
node = "&node"
pbx = "&loc"
sendNumber = "&fake"
groupIndication = "&gi"
configTemplate = "&config"
hardwareID = "&dev1.hw"

#parse HTTP XML reply from PBX (error or state)
def parseReply(reply):
    reply = str(reply)
    error = re.compile('error=\"(.*?)\"')
    if "error" in reply:
        matchResult = error.search(reply)
        if matchResult:
            result = matchResult.group(0)
    elif 'state="ok"' in reply:
        result = 'state="ok"'
    return result


#
def addGroup(number,groups,PBX):
    url = (innovaphoneIP + "/PBX0/ADMIN/mod_cmd_login.xml?"
     "cmd=submit-groups&xsl=pbx_edit_groups.xsl&guid="+getGUID(number)+"loc="+PBX
     )
    params = ""
    for group in groups.split(","):
        params = params + "&grp-name="+group.strip()+"&grp-dyn=&grp=&grp-name="
    r = requests.get(url+params+"&save=Apply", auth=(pbxAdmin, pbxPass))
    foo = str(r.content)
    msg = ""
    for grp in groups.split(","):
        if grp in foo:
            msg = msg + " OK: " + grp + ","
        else:
            msg = msg + " NOK: " + grp + ","
    return msg.strip()


def getGUID(number):
    #print(number)
    getList = innovaphoneIP + "/PBX0/ADMIN/mod_cmd_login.xml?cmd=show&user=*&search="+str(number)+"&search-loc=&search-grp=&hide=&xsl=pbx_objs_right.xsl"
    r = requests.get(getList, auth=(pbxAdmin, pbxPass))
    status = r.status_code
    reply = str(r.content)
    filter = re.compile('guid=\"(.*?)\"')
    matchResult = filter.search(reply)
    #print(reply)
    #print(matchResult)
    return matchResult.group(1)


with open(csvFile, 'r') as phonebook:
    csv_reader = csv.reader(phonebook, delimiter=delimiter)
    line_count = 2
    next(csv_reader)
    next(csv_reader) #yes, this skips two lines. yes, this is a stupid aproach. yes, I didn't care to find a better solution in a short time..
    for row in csv_reader:
        if line_count == 1: #header fields, required for matching
            header = row
            line_count += 1
        else:
            if row[0] != "": #if there is no longname, the row does not count!
                subscriber = row
                addScubscriber = (innovaphoneIP + "/PBX0/ADMIN/mod_cmd_login.xml?cmd=submit-object" #add subscriber
                                   + longName + "=" + row[0]
                                   + displayName + "=" + row[1]
                                   + name + "=" + row[2]
                                   + number + "=" + row[3]
                                   + description + "=" + row[4]
                                   + email + "=" + row[5]
                                   + sendEMail + "=" + row[6]
                                   + password + "=" + row[7]
                                   + passwordConfirm + "=" + row[8]
                                   + node + "=" + row[9]
                                   + pbx + "=" + row[10]
                                   + sendNumber + "=" + row[11]
                                   #+ groups + "=" + row[12]
                                   + configTemplate + "=" + row[13]
                                   + hardwareID + "=" + row[14]
                                  )
                #r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
                #print(addScubscriber)
                addScubscriber = addScubscriber.replace(" ","%20")
                r = requests.get(addScubscriber, auth=(pbxAdmin, pbxPass))
                status = r.status_code
                reply = r.content
                #print(str(row[3]))
                print("Add Subscriber" + "| Status: " + str(row[0]) + ", " + str(row[3]) + ", HTTP Request: " + str(status) + ", Result: " + parseReply(reply) + " | Add Groups: " + addGroup(row[3], row[12], row[10]))
                #PBX submit-groups /cmd submit-groups /xsl pbx_edit_groups.xsl /guid /loc PBX_Gleisdorf /grp-name /grp-name Technik-MSR /grp-active on /grp-dyn /grp-add /save OK /userid admin
                #print(reply)

