import csv
with open('data.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='|')
    spamwriter.writerow(['GPS_Coordinates'] + ['Accel_Z'] + ['Image_index'])
    for i in range(1000):
        spamwriter.writerow([i] + [i+1000] + [i+500])

print("hello")
