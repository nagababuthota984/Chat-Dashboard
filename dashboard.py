import sys
import json
import datetime
import matplotlib.pyplot as plt
import random
import string
class Feature:
    
    contacts={
        "Nagababu":{"number":8464832529},
        "Sena Sowseelya":{"number":8179596420},
        "Priya":{"number":9014156789},
        "Venkatesh":{"number":9014195649},
        "Chandrika":{"number":9391636052},
        "Venu Madhav":{"number":6304594994},
        "Ravi Teja":{"number":9014456732},
        "Praneeth":{"number":8555097775},
        "Hulk":{"number":8000843281}
    }

    

    
    def countResetter(self):
        self.msgData = self.readData()
        self.today = str(datetime.date.today())  #current date
        self.allDates = []
        for name,messages in self.msgData["messageSpace"].items():
            for message,timestamp in messages["sent"].items():    #collects sent messages timestamps
                self.allDates.append(str(timestamp)[:10])
            for message,timestamp in messages["recieved"].items(): #collects recieved messages timestamp
                self.allDates.append(str(timestamp)[:10])
    
        if self.today not in self.allDates:
            for contact,details in self.msgData["dashboard"].items():
                details["daylimit"][1] = details["daylimit"][0]
                details["todaycount"] = 0
        self.writeData(self.msgData)
        
    def readData(self):
        f = open("data.json","r")
        fd = f.read()
        self.data = json.loads(fd)
        f.close()
        return self.data

    def writeData(self,data):
        f = open("data.json","w")
        data = json.dumps(data)
        f.write(data)
        f.close()

    def sendMessage(self):
        self.countResetter()            #checks whether to reset the today message count(i.e., day changed)
        print("Choose a contact from the list: ",list(Feature.contacts.keys()))
        self.contact=input("Enter contact name: ")
        if self.contact in list(Feature.contacts.keys()):
            self.msgData = self.readData()
            if self.msgData["dashboard"][self.contact]["daylimit"][1]>0:
                self.message = input("Enter message: ")
                self.timeStamp = datetime.datetime.now()
                self.msgData["messageSpace"][self.contact]["sent"][self.message]=str(self.timeStamp)   #to show chat details in a time sorted order later.
                self.msgData["dashboard"][self.contact]["totalCount"]+=1
                self.msgData["dashboard"][self.contact]["todaycount"]+=1
                self.msgData["dashboard"][self.contact]["daylimit"][1]-=1
                print("You : {0}\n---Message Sent---\nSuccesfully sent to {1}\n\n".format(self.message,self.contact))
                self.writeData(self.msgData)
            else:
                print("\nUnable to send.Daily message limit for this contact has been reached.\n")
        else:
            print("Contact doesn't exist.")

    def showContactList(self):      #Show avaialable contacts 
        print("-----Contact List-----\n")
        for name,details in Feature.contacts.items():
            print("Name:{0}\n\t-->Number:{1}".format(name,details["number"]))
        print()
        print("-----That's all-----\n")

    
    def showDashboard(self):#displays 
        #access data in data.json
        self.countResetter()
        self.overallDashboard = {}
        self.data = self.readData()
        self.todayDashboard = {}   #contact : todaycount
        for contact,details in self.data["dashboard"].items():
            self.todayDashboard[contact] = details["todaycount"]
    
        for name,details in self.data["dashboard"].items():
            self.overallDashboard[name]=details["totalCount"]
        
        
        #plotting today's dashboard
        self.x_axis = self.todayDashboard.keys()         
        self.y_axis = self.todayDashboard.values()
        
        fig = plt.figure(figsize = (10, 5))
        plt.bar(self.x_axis, self.y_axis, color ='maroon', width = 0.5)
        plt.xlabel("Contacts")
        plt.ylabel("Messages sent/recieved today")
        plt.title("Today's Dashboard")
        plt.show()

        #plotting overall dashboard
        self.x_axis = self.overallDashboard.keys()
        self.y_axis = self.overallDashboard.values()
        
        fig = plt.figure(figsize=(10, 5))
        plt.bar(self.x_axis,self.y_axis,color="green",width = 0.5)
        plt.xlabel("Contacts")
        plt.ylabel("Overall messages sent/recieved")
        plt.title("Overall Dashboard")
        plt.show()

    def setLimit(self):#updates the day message limit for a contact.
        self.data = self.readData()
        print("By default, 1000 messages are permitted per day for each contact.\n")
        self.contactName = input("Enter the contact name from the list below\n{0}".format(list(Feature.contacts.keys())))
        print("Current limit for {0} is {1} per day.".format(self.contactName,self.data["dashboard"][self.contactName]["daylimit"][0]))
        self.newLimit = int(input("Enter new day limit for this contact: "))
        self.data["dashboard"][self.contactName]["daylimit"][0] = self.newLimit
        self.writeData(self.data)
        print("Limit has now been set to {0} as {1} messages per day".format(self.contactName,self.data["dashboard"][self.contactName]["daylimit"][0]))
    def randomMsgReciever(self): #sends messages from users randomly.
        self.user = random.choice(list(Feature.contacts.keys()))
        self.toSend = ''.join((random.choice(string.ascii_lowercase) for letter in range(6)))
        self.currentTimestamp = datetime.datetime.now()
        self.msgData = self.readData()
        self.msgData["messageSpace"][self.user]["recieved"][self.toSend]=str(self.currentTimestamp)  
        self.msgData["dashboard"][self.user]["totalCount"]+=1
        self.msgData["dashboard"][self.user]["todaycount"]+=1
        self.msgData["dashboard"][self.user]["daylimit"][1]-=1
        print("{0} : {1}\n---Message Recieved---\n\n".format(self.user,self.toSend))
        self.writeData(self.msgData)                




#main code
while(True):
    print("Welcome to Dashboard!\nChoose any one of the options:\n1.Send a Message\n2.Recieve a Random Message\n3.Show Contact List\n4.Show My Dashboard\n5.Set Message Limit\n6.Quit")
    choice = int(input())
    f = Feature()
    if choice == 1:
        f.sendMessage()
    elif choice == 2:
        f.randomMsgReciever()
    elif choice == 3:
        f.showContactList()
    elif choice ==4:
        f.showDashboard()
    elif choice == 5:
        f.setLimit()
    else:
        sys.exit()
    