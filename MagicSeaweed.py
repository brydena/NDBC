import requests
import math
import datetime

def get_distance(lat1,lng1,lat2,lng2): #Get the difference between two lat/long locations in radians
	dLat = lat2-lat1
	dLng = lng2-lng1
	a=(math.sin(dLat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLng/2)**2)
	return(6373.0*(2*math.atan2(math.sqrt(a),math.sqrt(1-a))))


r = requests.get('https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt')
if r.status_code == 200:
	print("Data retrieved correctly")
else:
	print("Data incorrectly retrieved, please check URL")
	exit()
lines = r.text.split('\n')
data = [line for line in lines]
arr = []
for a in data:
	arr.append(a.split()) #Got in all the data required and each is at its correct place
arr = [[a.replace('MM','Not recorded') for a in row] for row in arr]
lat  = input("Please enter latitude in degrees: ")
long = input("Please enter longitude in degrees: ")

latInRad = math.radians(float(lat))
longInRad = math.radians(float(long))
nearBouys = []
for a in arr[2:-1]:
	buoyDateTime = datetime.datetime(int(a[3]), int(a[4]), int(a[5]), hour=int(a[6]),minute=int(a[7]))
	d = datetime.datetime.utcnow() - buoyDateTime
	if d.days == 0 and d.seconds < 10800: #Less than 3 hours old
		latBouyRad = math.radians(float(a[1]))
		longBouyRad = math.radians(float(a[2]))
		distance = get_distance(latInRad,longInRad,latBouyRad,longBouyRad)
		if distance < 160.934: #100miles in km
			nearBouys.append(a)

numBouys = len(nearBouys)
print("The number of observations within 100 miles and the past 3 hours is: %d." % numBouys)
	
for a in nearBouys:
	print("Buoy Reference: {}".format(a[0]))
	print("Latitude (degrees): {}".format(a[1]))
	print("Longitude (degrees): {}".format(a[2]))
	print("Time (UTC): {}".format(datetime.datetime(int(a[3]), int(a[4]), int(a[5]), hour=int(a[6]),minute=int(a[7]))))
	print("Wind Direction (degrees): {}".format(a[8]))
	print("Wind Speed (m/s): {}".format(a[9]))
	print("Wave height (m): {}".format(a[11]))
	print("Average period (s): {}".format(a[13]))
	print("Atmospheric pressure (hPa): {}".format(a[15]))
	print("Air Temperature (degC): {} \n".format(a[17]))
	
	

