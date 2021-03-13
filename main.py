#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *
from dateutil.rrule import rrule, MONTHLY
import json
import requests
from tkcalendar import DateEntry
from tkinter import filedialog
import datetime
from fake_useragent import UserAgent
root = Tk()
root.title("Virginia Campground Tool")
astgvar = IntVar()
morrishillvar = IntVar()
bigmeadowvar = IntVar()
trailerlength = IntVar()
numofpeople = IntVar()


headers = {"User-Agent": UserAgent().random}

def outtofile(outdata):
 name=filedialog.asksaveasfile()
 if name is None:
  return
 name.write(str(datetime.datetime.now()))
 name.write("\n-----------------------\n")
 name.write(outdata)
 name.write("\n-----------------------\n")
 name.close()

def clicked():
    resultscreen = Tk()
    resultscreen.title("Result screen "+str(datetime.datetime.now()))
    scrollbar = Scrollbar(resultscreen)
    scrollbar.pack( side = RIGHT, fill = Y )
    try:
        x=int(numofpeople.get())
        if x<1:
            raise TclError()
    except TclError:
        badinputlabel= Label(resultscreen,text="number of people obviously must be a integer greater than 0 or it doesn't work, please try again")
        badinputlabel.pack()
        return True
    if checkindate.get_date()<=datetime.date.today() or checkoutdate.get_date() <=datetime.date.today() or checkindate.get_date()>checkoutdate.get_date():
        badinputlabel= Label(resultscreen,text="Both inputed dates obviously must be in the future or it doesn't work and check in date must be before or equal to check out date as well, please try again")
        badinputlabel.pack()
        return True
    outdatatext=""
    startingdate=checkindate.get_date()
    endingdate=checkoutdate.get_date()
    firstofmonth=datetime.datetime(startingdate.year,startingdate.month,1)
    monthcount = list(rrule(freq=MONTHLY, dtstart=firstofmonth, until=endingdate))
    monthcount = [e.strftime("%Y-%m-%dT00:00:00.000Z") for e in monthcount]
    requestdate=startingdate.strftime("%Y-%m-%dT00:00:00Z")
    apidate=startingdate.strftime("%Y-%m-%dT00:00:00Z")
    thing6=Button(resultscreen,text="Output results to file",command= lambda: outtofile(outdatatext))
    thing6.pack()
    results=0
    if astgvar.get():
        astgoutdata= Listbox(resultscreen, yscrollcommand = scrollbar.set,width=50 )
        astgoutdata.insert(END,"----------------RESULTS FOR ASSATEAGUE ISLAND---------------")
        astgdata=[]
        for month in monthcount:
            astgdata.append(requests.get(url="https://www.recreation.gov/api/camps/availability/campground/232507/month?",params={'start_date':month},headers=headers).json())
        for astginfo in astgdata:
                 for key in astginfo["campsites"].keys():
                     for date in astginfo["campsites"][key]["availabilities"].keys():
                         if checkindate.get_date()<=datetime.datetime.strptime(date,"%Y-%m-%dT00:00:00Z").date()<=checkoutdate.get_date() and astginfo["campsites"][key]["availabilities"][date]=="Available" and int(astginfo["campsites"][key]["max_num_people"])>=numofpeople.get():
                            astgoutdata.insert(END,date+" "+key+" is availabe\n")
                            outdatatext+=date+" "+key+" is availabe\n"
                            results+=1
        astgoutdata.pack(side=LEFT,fill=BOTH)
    if morrishillvar.get():
        morrishilloutdata= Listbox(resultscreen, yscrollcommand = scrollbar.set,width=50 )
        morrishilloutdata.insert(END,"----------------RESULTS FOR MORRIS HILL CAMPGROUND---------------")
        morrishilldata=[]
        for month in monthcount:
            morrishilldata.append(requests.get(url="https://www.recreation.gov/api/camps/availability/campground/232161/month?",params={'start_date':month},headers=headers).json())
        for morrishillinfo in morrishilldata:
                 for key in morrishillinfo["campsites"].keys():
                     for date in morrishillinfo["campsites"][key]["availabilities"].keys():
                         if checkindate.get_date()<=datetime.datetime.strptime(date,"%Y-%m-%dT00:00:00Z").date()<=checkoutdate.get_date() and morrishillinfo["campsites"][key]["availabilities"][date]=="Available" and int(morrishillinfo["campsites"][key]["max_num_people"])>=numofpeople.get():
                            morrishilloutdata.insert(END,date+" "+key+" is availabe\n")
                            outdatatext+=date+" "+key+" is availabe\n"
                            results+=1
        morrishilloutdata.pack(side=LEFT,fill=BOTH)
    if bigmeadowvar.get():
        bigmeadowoutdata= Listbox(resultscreen, yscrollcommand = scrollbar.set,width=50 )
        bigmeadowoutdata.insert(END,"----------------RESULTS FOR BIG MEADOWS CAMPGROUND AT SHENANDOAH---------------")
        bigmeadowdata=[]
        for month in monthcount:
            bigmeadowdata.append(requests.get(url="https://www.recreation.gov/api/camps/availability/campground/232459/month?",params={'start_date':month},headers=headers).json())
        for bigmeadowinfo in bigmeadowdata:
                 for key in bigmeadowinfo["campsites"].keys():
                     for date in bigmeadowinfo["campsites"][key]["availabilities"].keys():
                         if checkindate.get_date()<=datetime.datetime.strptime(date,"%Y-%m-%dT00:00:00Z").date()<=checkoutdate.get_date() and bigmeadowinfo["campsites"][key]["availabilities"][date]=="Available" and int(bigmeadowinfo["campsites"][key]["max_num_people"])>=numofpeople.get():
                            bigmeadowoutdata.insert(END,date+" "+key+" is availabe\n")
                            outdatatext+=date+" "+key+" is availabe\n"
                            results+=1
        bigmeadowoutdata.pack(side=LEFT,fill=BOTH)
    if not astgvar.get() and not bigmeadowvar.get() and not morrishillvar.get():
        noresultslabel=Label(resultscreen,text="You didn't specify any campgrounds, please try again")
        noresultslabel.pack()
    stringresults=str(results)+" results found"
    resultdata=Label(resultscreen,text=stringresults)
    resultdata.pack()

astg = Checkbutton(root,text="Assateague Island National Seashore Camground",onvalue=1,offvalue=0,variable=astgvar)
astg.pack(anchor="w")
morrishill = Checkbutton(root,text="Morris Hill Campground *only open from June to September",variable=morrishillvar)
morrishill.pack(anchor="w")
bigmeadow = Checkbutton(root,text="Big Meadows Campground at Shenandoah National Park",variable=bigmeadowvar)
bigmeadow.pack(anchor="w")
numpeoplelabel= Label(root,text="Number of People")
numpeoplelabel.pack()
numpeople = Entry(root,width=30,textvariable=numofpeople)
numpeople.pack()
cinlabel = Label(root,text="Check-in date")
cinlabel.pack()
checkindate=DateEntry(root,width=30,date_pattern='y-mm-dd')
checkindate.pack()
coutlabel = Label(root,text="Check-out date")
coutlabel.pack()
checkoutdate  = DateEntry(root,width=30,date_pattern='y-mm-dd')
checkoutdate.pack()
testbutton = Button(root,text="Submit",command=clicked)
testbutton.pack()
root.mainloop()
