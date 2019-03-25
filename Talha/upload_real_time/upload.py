import pymysql



data_t = [
    ["1.jpg","image_processed.jpg",4,50.4776842,-104.6371096],
    ["2.jpg","image_processed.jpg",4,50.4776842,-104.6371096]
]


conn = pymysql.connect(host='162.241.253.63', user ='roadqual_admin',password='admin', db='roadqual_capstone')    

def close_connection():
    cur.close()
    conn.close()
    

def upload_mysql(data):

    listValue = ""
    for i in range(len(data[0])):
        listValue += "("
        for j in range(len(data)):
            if(j==0):
                listValue += "\""+str(data[j][i])+"\", "
            elif(j==1):
                listValue += "\""+str(data[j][i])+"\", "
            elif(j==4):
                listValue += "'"+str(data[j][i])+"'"
            else:
                listValue += str(data[j][i])+", "
        if(i==len(data[0])-1):
            listValue += ")"
        else:
            listValue+="), "
    sql = ("INSERT INTO data_r_pi (originalImage, streetName, iri, gpslat,gpslong)  VALUES "+ listValue)

    cur = conn.cursor()
    cur.execute(sql)



    
