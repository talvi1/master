import pymysql
conn = pymysql.connect(host='162.241.253.63', user ='roadqual_admin',password='admin', db='roadqual_capstone')


data = [
    ["image_origina.jpg","image_processed.jpg",4,50.4776842,-104.6371096,"2019-02-24"],
    ["image_origina.jpg","image_processed.jpg",4,50.4776842,-104.6371096,"2019-02-24"],
    ["image_origina.jpg","image_processed.jpg",4,50.4776842,-104.6371096,"2019-02-24"],
    ["image_origina.jpg","image_processed.jpg",4,50.4776842,-104.6371096,"2019-02-24"],
    ["image_origina.jpg","image_processed.jpg",4,50.4776842,-104.6371096,"2019-02-24"]

]


listVlaue = ""

for i in range(len(data)):
    listVlaue += "("
    for j in range(len(data[i])):
        if(j==0):
            listVlaue += "\""+data[i][j]+"\", "
        elif(j==1):
            listVlaue += "\""+data[i][j]+"\", "
        elif(j==5):
            listVlaue += "'"+data[i][j]+"'"
        else:
            listVlaue += str (data[i][j])+", "
        print(data[i][j], end=' ')
    if(i==len(data)-1):
        listVlaue += ")"
    else:
        listVlaue+="), "
    print()

print()
print(listVlaue) 
#sql = ("SELECT * FROM data_r_pi")
sql = ("INSERT INTO data_r_pi (originalImage, processedImage, iri, gpslat,gpslog,dateRecorded )  VALUES "+ listVlaue)
print(sql)
cur = conn.cursor()
cur.execute(sql)



print()

for row in cur:
    print(row)

cur.close()
conn.close()

