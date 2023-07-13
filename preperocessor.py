import re 
import pandas as pd
def preprocess(data):
    pattern="\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[a-z]{2}\s"
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    l=[]
    for i in range(len(dates)):
        l.append(dates[i][:15]+dates[i][19:])
    l1=[]
    for i in dates:
        if "pm" in i :
            x=i.split(",")
            y=x[1].split(":")
            l1.append(x[0]+", "+(str(int(y[0])+12)+":"+y[1])[:5])
        if "am" in i:
            x=i.split(",")
            y=x[1].split(":")
            l1.append(x[0]+", "+(str(int(y[0])+12)+":"+y[1])[:5])
    df=pd.DataFrame({"user_message":messages})
    df["date"]=l1
    df.rename(columns={"message_date":"date"},inplace=True)
    users=[]
    messages=[]
    for message in df["user_message"]:
        entry=re.split("([\w\W]+?):\s",message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else :
            users.append("group_notification")
            messages.append(entry[0])
    df["user"]=users
    df["message"]=messages
    df["time"]=df["date"][:]
    df.drop(columns=["user_message"],inplace=True)
    l3=[]
    l4=[]
    l5=[]
    l6=[]
    l7=[]
    for i in df["date"]:
        v1=i.split(",")
        v2=v1[0].split("/")
        v3=v1[1].split(":")
        l3.append(v2[2])
        l4.append(v2[1])
        l5.append(v2[0])
        l6.append(v3[0])
        l7.append(v3[1])
    df["year"]=l3
    df["month_num"]=l4
    df["day"]=l5
    df["hour"]=l6
    df["minute"]=l7
    df["only_date"]=df["day"]+"-"+df["month_num"]+"-"+df["year"]
    df["date_time"]=pd.to_datetime(df["only_date"])
    df["day_name"]=df["date_time"].dt.day_name()
    
    df.drop(columns="date",inplace=True)
    l8=[]
    for i in df["month_num"]:
        if i=="01":
            l8.append("January")
        if i=="02":
            l8.append("February")
        if i=="03":
            l8.append("March")
        if i=="04":
            l8.append("April")
        if i=="05":
            l8.append("May")
        if i=="06":
            l8.append("June")
        if i=="07":
            l8.append("July")
        if i=="08":
            l8.append("August")
        if i=="09":
            l8.append("Sept")
        if i=="10":
            l8.append("Oct")
        if i=="11" :
            l8.append("Nov")
        if i=="12":
            l8.append("Dec")
    df["month"]=l8
    period=[]
    df["hour"].replace({" 24":" 0"},inplace=True)
    for hour in df["hour"]:
        if hour==" 23":
            period.append(str(hour)+"-"+str("00"))
        elif hour==" 0":
            period.append(str("00")+"-"+str(int(hour)+1))
        else :
            period.append(hour+"-"+str(int(hour)+1))
    df["period"]=period
    return df
