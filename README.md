# Innovaphone CSV import

### Description
This is a Python script to import a CSV-Phonebook into your Innovaphone PBX.
It's written for techs that have to set up multiple PBXs and want to focus on the important tasks instead of
spending a lot of time clicking through the interface of the PBX.

It works by utilizing the Innovaphone "mod cmd", the same functions the Web-Interface uses.

### Goals
- speed up the process of adding dozens or hundreds of users to your PBX
- pass all the non-unique parameters to the users
- let the client fill out the csv with their data and plug the list into the script

### Features
- easily add subscribers via http requests automatically
- configure the subscriber with the following parameters: E-Mail, send E-Mail, send number, groups and the MAC-Address (for provisioning) as well as the required fields (longName, displayName, H323


### Requirements
Modules
```sh
import csv
import requests
import re
```

Innovaphone Admin-Credentials

### To-Do: 
  - adding group indications for the individual user
  - making groups active/inactive
  - making groups dynamic/static

### Warning

I do not guarantee that every action this script takes is intended, and not everything has been testet yet.
Altough it was tested with an already installed IP800, it might have some unwanted side effects!
Only use it on new, out of the box PBXs.

**For example:**

If you add the subscriber 123 to the group "Sales" it's an "absolute" change not an addition, due to the nature how this specific command was included into the Innovaphone Web-Application/-Frontend.

This means if the subscriber 123 already exists, and you "add" him to Sales, the other groups will be deleted from the Subscribers entry.
