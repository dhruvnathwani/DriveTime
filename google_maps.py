import googlemaps
import datetime
import json
import time
from textwrap import wrap
import matplotlib.pyplot as plt
import matplotlib
from pygeocoder import Geocoder
matplotlib.get_cachedir()


key = ''

#get the coordinates for a given address
def address_to_coordinates(address):

    isvalid = False

    while not isvalid:

        try:
            locator = googlemaps.Client(key = key)
            #geolocator = Nominatim()

            address_conversion = locator.geocode(address)

            dump = json.dumps(address_conversion)
            final = json.loads(dump)

            #print(final)

            coordinates = final[0]['geometry']['location']

            latitude = coordinates['lat']
            longitude = coordinates['lng']

            coordinate_set = str(latitude) + ',' + str(longitude)

            isvalid = True

        except:

            print("Please input a valid address")
            address = address_input()







    return coordinate_set


#Get the drive time by feeding coordinates from address_to_coordinates function
def get_drive_time(start_coordinates,end_coordinates,time):

    gmaps = googlemaps.Client(key = key)

    #now = datetime.now()

    directions_result = gmaps.directions(start_coordinates,end_coordinates,departure_time=time)

    #print(directions_result[0]['legs'][0]['distance']['text'])

    #print(directions_result[0]['legs'][0]['duration']['text'])

    min = directions_result[0]['legs'][0]['duration']['text']

    time = str(min).split()[0]

    return time


#let the user choose the day of the week
def next_weekday(weekday):
    days_ahead = weekday - int(datetime.datetime.today().weekday())
    if days_ahead <=0:
        days_ahead += 7
    return weekday + days_ahead
#int(datetime.timedelta(days_ahead))

def day_of_week_transaltor(day_of_week):

    if str.lower(day_of_week) == "sunday":
        return 6
    elif str.lower(day_of_week) == "monday":
        return 0
    elif str.lower(day_of_week) == "tuesday":
        return 1
    elif str.lower(day_of_week) == "wednesday":
        return 2
    elif str.lower(day_of_week) == "thursday":
        return 3
    elif str.lower(day_of_week) == "friday":
        return 4
    elif str.lower(day_of_week) == "saturday":
        return 5



#Get the time the user wants to arrive
def time_selector():
    isvalid = False
    while not isvalid:
        try:
            Time_you_want_to_arrive_input = datetime.datetime.strptime(input("What time would you like to arrive? (Please specify time in HHMM format using 24 hour time (ex. 0800 for 8:00 AM or 1400 for 2:00 PM)): "),"%H%M")

            Time_you_want_to_arrive = Time_you_want_to_arrive_input.strftime("%I:%M %p")

            print("You want to arrive at: " + str(Time_you_want_to_arrive))


            #Time_you_want_to_arrive = Time_you_want_to_arrive.time()
            isvalid = True
        except:
            print("Please enter correct time in HHMM format")

    #convert time to epoch to feed into google maps

    #day_of_week = input("What day do you want to leave? ")

    #day_of_week = day_of_week_transaltor(day_of_week)

    #day_of_week = next_weekday(day_of_week)

    year = int(datetime.datetime.now().strftime("%Y"))
    month = int(datetime.datetime.now().strftime("%m"))
    date = int(datetime.datetime.now().strftime('%d'))
    seconds = int(datetime.datetime.now().strftime('%S'))
    wday = int(datetime.datetime.today().weekday())
    #wday = int(day_of_week)
    yday = int(datetime.datetime.today().timetuple().tm_yday)
    isdst = int(time.localtime().tm_isdst)

    

    broken = wrap(str(Time_you_want_to_arrive_input),2)

    hour = int(broken[5])
    minutes1 = str(broken[6].split(":")[1])
    minutes2 = str(broken[7].split(":")[0])
    minute = int(str(minutes1) + str(minutes2))
   

    t = (year,month,date,hour,minute,seconds,wday,yday,isdst)

    
    epoch = time.mktime(t)
    

    current_epoch = time.time()

    #because google doesn't like values of time in the past, this will push up the current epoch by a day
    if epoch < current_epoch:
        new_date = str(datetime.date.today() + datetime.timedelta(days=1))

        date = int(str(new_date).split("-")[2])



        t = (year,month,date,hour,minute,seconds,wday,yday,isdst)

        epoch = time.mktime(t)

  

    return epoch

#After a new time to leave has been calculated, this function takes that time and converts into epoch (google api friendly) translated time
def epoch_converter(time):

    converted_time = time.timestamp()
    return converted_time


def address_input():

    street_address = input("Please input street address (ex. 21 jump street (no need for city and state, that will be next!)): ")
    city = input("Please input city: ")
    state = input("Please input state: ")
    #zip = input("Please input zipcode: ")

    address = str(street_address)+", "+str(city)+", "+str(state)

    print("-----------------------------------")

    print("Your address is: " + str(address))

    return address



#Beginning of script
print("Let's get some information first....")

print("Please fill in the details for your starting address below")

print('-------------------------------------------------------------------')

start_address = address_input()

start_coordinates = address_to_coordinates(start_address)

print('---------------------------------------------------------------------')

print('Please fill in the details for your destination address below')


print('---------------------------------------------------------------------')

end_address = address_input()

end_coordinates = address_to_coordinates(end_address)



#Get time user wants to arrive and store that as arrival time
arrival_time = time_selector()

#allow user to enter for what day of the week they are interested in finding data for
#day_of_week = pass


#Get the drive time assuming the person is leaving at the arrival time, this is just for establishing a baseline of how long to subtract from the departure time

#it will take this many minutes to get to wok assuming you leave at the time you wanted to arrive
baseline_drive_time = int(get_drive_time(start_coordinates,end_coordinates,arrival_time))


#reformat the arrival time into a datestamp form so that we can subtract time from it
arrival_time_datestamp = datetime.datetime.fromtimestamp(arrival_time)


#subtract that drive time from when they said they wanted to arrive (ex. if the drive was 10 minutes and they need to be there by 8 am, subtract 10 minutes from 8 am)
modified_departure_time = arrival_time_datestamp - datetime.timedelta(minutes=baseline_drive_time)

#convert the modified departure time into epoch using the epoch converter
departure_time = epoch_converter(modified_departure_time)

#feed the departure time into the google maps api to get a new drive time
new_drive_time = int(get_drive_time(start_coordinates,end_coordinates,departure_time))


#reformat departure time to datestamp time so we can work with it
departure_time_datestamp = datetime.datetime.fromtimestamp(departure_time)


#add the drive time to the new departure time
final_arrival_time = departure_time_datestamp + datetime.timedelta(minutes = new_drive_time)



#while the final arrival time is higher then when you want to arrive, make the calculation on drive time but keep subtracting 1 minute
while final_arrival_time > arrival_time_datestamp:

    #subtract 1 minute from the modified departure time to see if it gets you there before the arrival time
    modified_departure_time = modified_departure_time - datetime.timedelta(minutes = 1)

    departure_time = epoch_converter(modified_departure_time)

    new_drive_time = int(get_drive_time(start_coordinates,end_coordinates,departure_time))

    final_arrival_time = modified_departure_time + datetime.timedelta(minutes = new_drive_time)

    print (final_arrival_time)

else:

    readable_time = modified_departure_time.strftime("%I:%M %p")

    print("In order to get to your destination on time, you must leave at " + str(readable_time))
    print("Your drive will take " + str(new_drive_time) + " minutes")



#Now show the exponential commute time growth as traffic increases


answer = input("Curious to see what the incremental traffic trends are like for your driving time within a certain window? Enter Y/N. ")


if str(answer).lower() == "y":

    minute_window = input("How many minutes do you want the window to be? (ex. do you want to look at traffic over 5 minutes, 10 minutes? Not sure? 10 minutes is a good place to start.) ")

    minute_window = str(minute_window).split(" ")[0]

    minute_window = int(minute_window)


    modified_departure_time = modified_departure_time - datetime.timedelta(minutes = minute_window)

    new_drive_time = int(get_drive_time(start_coordinates,end_coordinates, modified_departure_time))

    final_arrival_time = modified_departure_time + datetime.timedelta(minutes = new_drive_time)

    drive_times = []
    departure_times = []


    incremental = 1

    if minute_window > 20:
        incremental = 5

    print ('Now collecting traffic data to see trends, sit tight!')

    while final_arrival_time < arrival_time_datestamp:

        modified_departure_time = modified_departure_time + datetime.timedelta(minutes = incremental)

        new_drive_time = int(get_drive_time(start_coordinates,end_coordinates, modified_departure_time))

        final_arrival_time = modified_departure_time + datetime.timedelta(minutes = new_drive_time)

        drive_times.append(new_drive_time)
        departure_times.append(modified_departure_time.strftime("%I:%M %p"))

    figure = plt.figure(num = 1, figsize=(20,5))

    plt.bar(departure_times,drive_times)

    plt.xlabel('Departure Time')
    plt.ylabel("Driving Time")

    plt.show()



print('Done!')


input()
