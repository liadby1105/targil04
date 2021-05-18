#MATALA04 - liad ben yechiel

import requests, json
cities=str()
with open('dests.txt','r',encoding = 'utf8') as file:
    cities = file.read().splitlines()
    
    
handle=open('dests.txt','r', encoding='utf-8') #open file
city_names=dict()
counter=0
for line in handle:#entring the city names into dictionary by numbers for name the 3 top farthest cities
    city_names[counter]=line
    counter=counter+1


farthest1=0 #reset the farthest distance
farthest2=0
farthest3=0
city1='' ##reset the city names
city2=''
city3=''

api_key = "AIzaSyDCk9wSMp7t9x5p7PJQLe8W3AKGxwWwKxc"
url1 ='https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
origin ='תל אביב'
dict_destinations={}
farthest=[] 
for dest in cities:
    try:
        response_distance = requests.get(url1 + "origins=" + origin + "&destinations=" + dest + "&key=" + api_key)
        distance = response_distance.json()["rows"][0]["elements"][0]["distance"]["text"]
        seconds = response_distance.json()["rows"][0]["elements"][0]["duration"]["value"]
        hours= int(int(seconds)/3600)
        minutes= int((int(seconds)-(hours*3600))/60)
        duration= str(hours) + ' hours ' + "and " + str(minutes) + " minutes"
        farthest.append(distance)
        address = dest
        url2 ='https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (address, api_key)
        response_geo = requests.get(url2)
        latitude = response_geo.json()['results'][0]['geometry']['location']['lat']
        longitude = response_geo.json()['results'][0]['geometry']['location']['lng']   
        detailsPerCity = (distance, duration) + (latitude, longitude) 
        dict_destinations[dest] = detailsPerCity # dictionary with cities as keys and tuples as values
    except:
        print('There is no place such' , dest) #solving the problem if the place in the list not real/not found.
        continue
    
for key in dict_destinations:  
    print(key+': ') #print the name of the city that is also used as a key
    print(dict_destinations[key]) #print the dictionary including the requiring sections
    
import re #libary that i found in the internet thats helps fix strings.
distances_list = [] 
distance_patt = re.compile(r"([^km]+)") # finding the string (km) and delete it.
for i in farthest:
    include_km = distance_patt.search(i)
    if include_km:
        distances_list.append(i[include_km.span()[0]:include_km.span()[1]].replace(' ','').replace(',','')) #deleting the "," from the distance

distances_list = [float(i) for i in distances_list] # converting to int

for i in range(len(distances_list)): #finding the 3 top farthest cities from tel aviv and their names.
    if distances_list[i]>farthest1:
        farthest3=farthest2
        farthest2=farthest1
        farthest1=distances_list[i]
        city3=city2
        city2=city1
        city1=city_names[i]
    elif distances_list[i]>farthest2:
        farthest3=farthest2
        farthest2=distances_list[i]
        city3=city2
        city2=city_names[i]
        #city3=city_names[i-1]
    elif distances_list[i]>farthest3:
        farthest3=distances_list[i]
        city3=city_names[i]

print('\n' ,'הערים הרחוקות מתל אביב:', #print the results.
      '\n','1)', city1.strip(),' = ', farthest1, 'קילומטרים'
      '\n','2)', city2.strip(),' = ', farthest2, 'קילומטרים'
      '\n','3)', city3.strip(),' = ', farthest3, 'קילומטרים')