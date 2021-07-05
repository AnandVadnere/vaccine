
import requests
import json
from datetime import datetime
import time
import sys
from playsound import playsound
import cgi

form = cgi.FieldStorage()
ProdUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"

headers = {'Accept': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           }

PinCode =form["pin"].value #Enter your pincode here
CheckAfter = 0.25 # Specify your time limit after which you want to check in minutes
VaccineType = form["radioVaccine"].value# Set your vaccine type acceptable values COVISHIELD and COVAXIN
MyAge = form["radioAgegroup"].value # Set your age here, there are different sessions for people having age 45+ and below
iDose = form["radioDose1orDose2"].value
iFee = form["radioFreeorPaid"].value

if iDose =="Dose1":
    Dose = 'available_capacity_dose1'
if iDose =="Dose2":
    Dose = 'available_capacity_dose2'
if iFee == 'free':
    Fee = 'Free'
if iFee == 'paid':
    Fee = 'Paid'

def SlotChecker():
    
    x = datetime.now()
    Day = str(x.day)
    Month = str(x.month)
    Year = str(x.year)
    FetchUrl = ProdUrl + "pincode=" + PinCode + "&date=" + Day + "-" + Month + "-" + Year
    ApiResponse = requests.get(FetchUrl, headers = headers)
                                
    # D = '''
    #     {"centers":[{"center_id":667320,"name":"HSC Semari","address":"Semari Raxaul","state_name":"Bihar","district_name":"East Champaran","block_name":"Raxaul","pincode":845305,"lat":26,"long":84,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"7252e831-2d71-4913-bc78-5fd0fa8beb06","date":"15-05-2021","available_capacity":10,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":682389,"name":"Raxaul Jokiyari","address":"Jokiyari","state_name":"Bihar","district_name":"East Champaran","block_name":"Raxaul","pincode":845305,"lat":26,"long":84,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"c454f42a-f81b-4649-95b6-6002626486e4","date":"15-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]}]}
    # '''
    # Data = json.loads(D)
    Data = json.loads(ApiResponse.text)

    if(len(Data['centers'])) <= 0:
        print("No slots available.")
        sys.exit()

    for c in Data['centers']:
        for s in c['sessions']:
            if (MyAge >= s['min_age_limit'] and s['vaccine'] == VaccineType.upper()) and (s[Dose] > 0 and c[Fee]=='Free'):
                # we have got an availability
                for x in range(5):
                    playsound("loud_alarm_clock.mp3")
  
                #MsgText = "We have found an availability at "+ c['name'] + " for age " + str(s['min_age_limit']) + "+ and vaccine type "+ s['vaccine'] + ". Current available capacity is " + str(s['available_capacity']) + " Do you want to book now ?"
                #UserInput = easygui.ynbox(MsgText, 'Cowin Slot Finder (Author: Anand Vadnere)', ('Yes', 'No'))
                #if(UserInput):
                #    webbrowser.open("https://www.cowin.gov.in/home")
                #    sys.exit()
                #sys.exit()
        print("No slots available in %s." % (c['name'],), end = ' ')
    return 0


while(True):
    SlotChecker()
    print("Last checked at %s " % (str(datetime.now().time()),))
    print("We'll check again in %s minute(s)" % (CheckAfter,))
    playsound("notification (1).mp3")
    time.sleep(CheckAfter*60)

