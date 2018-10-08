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
     "cmd=submit-groups&xsl=pbx_edit_groups.xsl&guid="+getGUID(number)+
     "loc="+PBX
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
    getList = innovaphoneIP + "/PBX0/ADMIN/mod_cmd_login.xml?cmd=show&user=*&search="+str(number)+"&search-loc=&search-grp=&hide=&xsl=pbx_objs_right.xsl"
    r = requests.get(getList, auth=(pbxAdmin, pbxPass))
    status = r.status_code
    reply = str(r.content)
    filter = re.compile('guid=\"(.*?)\"')
    matchResult = filter.search(reply)
    print(reply)
    print(matchResult)
    return matchResult.group(1)

getGUID(180)