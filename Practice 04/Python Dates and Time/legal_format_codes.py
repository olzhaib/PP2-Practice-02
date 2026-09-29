import datetime

#weekday short version
x = datetime.datetime.now()
print(x.strftime("%a"))

#Weekday, full version
x = datetime.datetime.now()
print(x.strftime("%A"))

#Weekday as a number 0-6, 0 is Sunday
x = datetime.datetime.now()
print(x.strftime("%w"))

#Day of month 01-31
x = datetime.datetime.now()
print(x.strftime("%d"))

#Month name, short version
x = datetime.datetime.now()
print(x.strftime("%b"))

#Month name, full version
x = datetime.datetime.now()
print(x.strftime("%B"))

