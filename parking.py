import datetime
import math
import tkinter
from tkinter import ttk
from tkinter import *
import pandas as pd


window = Tk()

window.title("Parking")
window.configure(background='')
window.geometry('800x600')
window.resizable(False,False)

status_vehicle_entry='Enter details'
status_vehicle_exit='Enter slot number'

def vehicle_entry():
    vehicle_number_val=number_input.get()
    vehicle_type_val=default_type.get()
    vehicle_slot_val=default_slot.get()

    global details, vehicle_number, slots, vehicle_type, vehicle_number, entry_time, exit_time, log_count, filled_slots

    details = read_details()
    slots = list(details['Slots'])
    vehicle_type = list(details["Vehicle Type"])
    vehicle_number = list(details['Vehicle Number'])
    entry_time = list(details['Entry Time'])

    if vehicle_number_val in vehicle_number:
        status_vehicle_entry = 'Vehicle already exists'
    elif vehicle_number_val=='':
        status_vehicle_entry = 'Enter vehicle number'
    else:
        if vehicle_slot_val.isdigit()==True:
            entry=str(datetime.datetime.now())
            entry=entry[:-7]
            entry_time=entry[11:]
            entry_date=entry[8:10]

            details.loc[int(vehicle_slot_val),'Vehicle Number']=vehicle_number_val
            details.loc[int(vehicle_slot_val),'Entry Time']=entry

            details.to_csv('parking_details.csv',index=False)


            log_details.loc[log_count,'Slots']=vehicle_slot_val
            log_details.loc[log_count,'Vehicle Number']=vehicle_number_val
            log_details.loc[log_count,'Vehicle Type']=vehicle_type_val
            log_details.loc[log_count,'Entry Time']=entry

            log_count += 1

            log_details.to_csv('parking_log.csv',index=False)


            if vehicle_type_val == 'Bike':
                empty_bike_slots.remove(int(vehicle_slot_val))
                filled_slots.append(int(vehicle_slot_val))
            elif vehicle_type_val == 'Car':
                empty_car_slots.remove(int(vehicle_slot_val))
                filled_slots.append(int(vehicle_slot_val))

            change_slots()

            status_vehicle_entry='Entry Successful, you can park at slot no - '+vehicle_slot_val
            status_entry.config(text=status_vehicle_entry)
        else:
            status_vehicle_entry='Select valid slot'
    
    status_entry.config(text=status_vehicle_entry)
    

def vehicle_exit():
    global details, vehicle_number, slots, vehicle_type, vehicle_number, entry_time, exit_time, log_count, filled_slots

    details = read_details()
    vehicle_number = list(details['Vehicle Number'])
    slots = list(details['Slots'])
    vehicle_type = list(details["Vehicle Type"])
    vehicle_number = list(details['Vehicle Number'])
    entry_time = list(details['Entry Time'])

    log_details=read_log_details()

    log_entry_time=list(log_details['Entry Time'])

    exit=str(datetime.datetime.now())
    exit=exit[:-7]
    exit_time=exit[11:13]
    exit_date=exit[8:10]

    exit_slot_num=exit_slot_value.get()
    if exit_slot_num.isdigit()==True:
        if int(exit_slot_num) in filled_slots:
            entry_time_exit_vehicle=entry_time[int(exit_slot_num)]
            entry_time_exit_vehicle_time=entry_time_exit_vehicle[11:13]
            entry_time_exit_vehicle_date=entry_time_exit_vehicle[8:10]

            days=int(exit_date)-int(entry_time_exit_vehicle_date)
            duration=(int(exit_time)+(days*24))-int(entry_time_exit_vehicle_time)
            cost=duration*20

            log_exit_index=log_entry_time.index(entry_time_exit_vehicle)

            log_details.loc[log_exit_index,'Exit Time']=exit
            log_details.to_csv('parking_log.csv',index=False)

            details.loc[int(exit_slot_num),'Vehicle Number']=float('nan')
            details.loc[int(exit_slot_num),'Entry Time']=float('nan')

            details.to_csv('parking_details.csv',index=False)

            status_vehicle_exit='Exit successful, please pay fee of '+str(cost)+'/-'

            filled_slots.remove(int(exit_slot_num))
        else:
            status_vehicle_exit='Please enter vehicle slot number'
    else:
        status_vehicle_exit='Please enter valid slot number'
    status_exit.config(text=status_vehicle_exit)



def change_slots(*args):
    if default_type.get()=='Bike':
        new_slots=empty_bike_slots
    elif default_type.get()=='Car':
        new_slots=empty_car_slots
    
    default_slot.set('')
    slot_select['menu'].delete(0,'end')

    for choice in new_slots:
        slot_select['menu'].add_command(label=choice, command=tkinter._setit(default_slot,choice))


def read_details():
    details = pd.read_csv('parking_details.csv')
    return details

def read_log_details():
    log_details = pd.read_csv('parking_log.csv')
    return log_details

details = read_details()
log_details = read_log_details()

log_count = len(log_details)

slots = list(details['Slots'])
vehicle_type = list(details["Vehicle Type"])
vehicle_number = list(details['Vehicle Number'])
entry_time = list(details['Entry Time'])

only_vehicle_types = list(set(list(details["Vehicle Type"])))

all_bike_slots=[x for x, value in enumerate(vehicle_type) if value == 'Bike']
all_car_slots=[x for x, value in enumerate(vehicle_type) if value == 'Car']

empty_bike_slots=[]
empty_car_slots=[]

filled_slots=[]

for x in all_bike_slots:
    val = len(str(vehicle_number[x])) == 3 and type(vehicle_number[x]) == float and math.isnan(vehicle_number[x]) == True
    if val==True:
        empty_bike_slots.append(x)
    else:
        filled_slots.append(x)

for x in all_car_slots:
    val = len(str(vehicle_number[x])) == 3 and type(vehicle_number[x]) == float and math.isnan(vehicle_number[x]) == True
    if val==True:
        empty_car_slots.append(x)
    else:
        filled_slots.append(x)

secondary_vehicle_slots = empty_bike_slots

default_type=StringVar()
default_type.set(only_vehicle_types[0])


tabs=ttk.Notebook(window)
tabs.pack()

entry_tab=Frame(tabs,width=800,height=600,bg='#EFC097')
exit_tab=Frame(tabs,width=800,height=600,bg='#EFC097')
#display_tab=Frame(tabs,width=800,height=600,bg='#EFC097')

tabs.add(entry_tab,text='Entry')
tabs.add(exit_tab,text='Exit')
#tabs.add(display_tab,text='Display')

number_text=Label(entry_tab,text='Vehicle Number: ',padx=31,pady=20,background='#EFC097', font=('Arial',17))
type_text=Label(entry_tab,text='Type of Vehicle:',padx=35,pady=20,background='#EFC097', font=('Arial',17))
slot_text=Label(entry_tab,text='Slot Number: ',padx=40,pady=20,background='#EFC097', font=('Arial',17))
status_entry=Label(entry_tab,text=status_vehicle_entry,padx=40,pady=20,background='#EFC097', font=('Arial',17))

entry_button=Button(entry_tab,text='Enter',padx=215,pady=20,command=vehicle_entry, font=('Arial',17))

number_input=Entry(entry_tab,width=11,justify=CENTER,font=('Arial', 32),borderwidth=3)


exit_slot_text=Label(exit_tab,text='Slot Number',padx=31,pady=20,background='#EFC097', font=('Arial',17))
status_exit=Label(exit_tab,text=status_vehicle_exit,padx=40,pady=20,background='#EFC097', font=('Arial',17))

exit_slot_value=Entry(exit_tab,width=9,justify=CENTER,font=('Arial', 32),borderwidth=3)

exit_button=Button(exit_tab,text='Clear',padx=215,pady=20,command=vehicle_exit, font=('Arial',17))


if default_type.get()=='Bike':
    secondary_vehicle_slots=empty_bike_slots
elif default_type.get()=='Car':
    secondary_vehicle_slots=empty_car_slots


default_slot=StringVar()
default_slot.set(secondary_vehicle_slots[0])


type_select=OptionMenu(entry_tab,default_type,*only_vehicle_types)
slot_select=OptionMenu(entry_tab,default_slot,*secondary_vehicle_slots)

type_select.config(width=20,height=2,font=('Arial',14))
slot_select.config(width=20,height=2,font=('Arial',14))

default_type.trace('w', change_slots)


number_text.place(relx=0.2,rely=0.1)
type_text.place(relx=0.2,rely=0.23)
slot_text.place(relx=0.2,rely=0.33)

number_input.place(relx=0.5,rely=0.1)
type_select.place(relx=0.5,rely=0.21)

slot_select.place(relx=0.5,rely=0.33)

entry_button.place(relx=0.2,rely=0.46)

status_entry.place(relx=0.5,rely=0.67, anchor= CENTER)



exit_slot_text.place(relx=0.2,rely=0.3)

exit_slot_value.place(relx=0.5,rely=0.3)

exit_button.place(relx=0.2,rely=0.43)

status_exit.place(relx=0.5,rely=0.65, anchor= CENTER)

window.mainloop()