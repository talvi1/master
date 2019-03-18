import pymysql



data_t = [
    ["1.jpg","image_processed.jpg",4,50.4776842,-104.6371096],
    ["2.jpg","image_processed.jpg",4,50.4776842,-104.6371096]
]






def upload_mysql(data):
    conn = pymysql.connect(host='162.241.253.63', user ='roadqual_admin',password='admin', db='roadqual_capstone')
    listVlaue = ""
    for i in range(len(data[0])):
        listVlaue += "("
        for j in range(len(data)):
            if(j==0):
                listVlaue += "\""+str(data[j][i])+"\", "
            elif(j==1):
                listVlaue += "\""+str(data[j][i])+"\", "
            elif(j==4):
                listVlaue += "'"+str(data[j][i])+"'"
            else:
                listVlaue += str(data[j][i])+", "
        if(i==len(data[0])-1):
            listVlaue += ")"
        else:
            listVlaue+="), "
    #sql = ("SELECT * FROM data_r_pi")
    print(listVlaue)
    sql = ("INSERT INTO data_r_pi (originalImage, processedImage, iri, gpslong,gpslat)  VALUES "+ listVlaue)

    cur = conn.cursor()
    cur.execute(sql)


    cur.close()
    conn.close()
    
    
