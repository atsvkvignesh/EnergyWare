import mysql.connector as mc
import os 
import datetime 
import smtplib
x=datetime.datetime.now()

try:
    os.system(" figlet energywere")
except:
    pass

datal=[] # store needed info
sum_ele=0 #total ele prodused 
sum_non_r=0 #totsl non renu
sum_r=0.0 #total renu
month=""

# % conversion 

sum_non_renu=0
sum_renu=0
total_sum=0.0
co=mc.connect(host="127.0.0.1",user='root',passwd='mysql12600',database='energy_w')

if co.is_connected():
    print("connected to sql DB")
curobj=co.cursor()

curobj.execute("select sum(pow_units) from volt_info where pow_type='non-renu'")
data=curobj.fetchall()

for i in data:
    sum_non_renu=i[0]

curobj.execute("select sum(pow_units) from volt_info where pow_type='renu'")
data=curobj.fetchall()
for i in data:
    sum_renu=i[0]

curobj.execute("select sum(pow_units) from volt_info")
data=curobj.fetchall()

for i in data :
    total_sum=i[0]



per_sum_table1_nonrenu=(sum_non_renu/total_sum)*100
per_sum_table1_renu=(sum_non_renu/total_sum)*100

print(per_sum_table1_nonrenu , "{^_^}" ,per_sum_table1_renu )




curobj.execute("insert into elec value("+str(per_sum_table1_nonrenu)+",'non_r')")
curobj.execute("insert into elec value("+str(per_sum_table1_renu)+",'renu')")



curobj.execute('select *from elec')
data=curobj.fetchall()
for i in data:
    datal+=[[i[0],i[1]]]

print(datal)

''' 
algo 
find the % or renu and non renu 

sum both then (x/sum)*100

'''

for j in datal:
    sum_ele+=j[0]
    if j[1]=="non_r":
        sum_non_r+=j[0]
    else :
        sum_r+=j[0]

#to cal %

per_renu=(sum_r/sum_ele)#*100 # % of renu elect
per_non_renu=(sum_non_r/sum_ele)#*100  # % of non renu

#trns_pow_intake=int(intput("enter pow supplied to trans:"))  # will be collected from electricy meter
usrid=int(input("enter user id:"))
pow_used=float(input("enter pow used :")) # will be collecte from electricity meter 

#pow_usr_renu=int(input("enter renu energy for users:"))

usr_use_renu=pow_used*(per_renu)
usr_use_non_renu=pow_used*(per_non_renu)  #absulite value of units used 

# to cal % of runu and non rnu from user 
user_pro=float(input("enter user produced volt :"))
#per_user_pro=(user_pro/pow_used)
usr_use_renu=usr_use_renu+user_pro
usr_use_non_renu=usr_use_non_renu-user_pro

per_non_renewable=(usr_use_non_renu/pow_used)*100

per_renewable=(usr_use_renu/pow_used)*100
print("Percentage of power generated from renewable source:",per_renewable) 



x=datetime.datetime.now()
if len(str(x.month))==1:
    month="0"+str(x.month)
else :
    month=str(x.month)
date=str(x.year)+"-"+month+"-"+str(x.day)

qury="insert into intimation values({} , {} ,{},'{}') ".format(usrid,per_renewable,per_non_renewable,date)
print(qury)
curobj.execute(qury)

#if x.hour==17 and x.date==28: #can be chnaged by usr
server=smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login("ceramapleheart2802@gmail.com","bozlwcpopkgdealk")
curobj.execute("SELECT AVG(per_renu) FROM intimation")
data=curobj.fetchall()
for i in data :
    intmsg=float(i[0])
if intmsg<20.0:
    subject="EB intimation"
    body="Hi there here is your renewable energy useage for last 28days "+str(intmsg)+"'%' of total electricity consumption is from renewable sources. Please try and save the environment. "
    msg=f'Subject: {subject}\n\n{body}'
elif intmsg<30.0:
    subject="EB intimation"
    body="Hi there here is your renewable energy useage for last 28days "+str(intmsg)+"'%' of total electricity consumption is from renewable sources. Good job in saving the planet "
    msg=f'Subject: {subject}\n\n{body}'
elif intmsg<90.0:
    subject="EB intimation"
    body="hi there here is your renewable energy useage for last 28days "+str(intmsg)+"'%' of total electricity consumption is from renewable sources. You do care about the planet ! "
    msg=f'Subject: {subject}\n\n{body}'
else :
    subject="EB intimation"
    body="hi there here is your renewable energy useage for last 28days "+str(intmsg)+"'%' of total electricity consumption is from renewable sources. You are the best and deserve a medal ! "
    msg=f'Subject: {subject}\n\n{body}'

server.sendmail("ceramapleheart2802@gmail.com","shreevigneshkhumar@gmail.com",msg)
print("mail sent")
