import requests
import json
serverIP= 'http://gxp4ab7yqzq45vaf.onion'
### OPTIONS ###
r=requests.get(serverIP)

keepAlive=True
state=0

while(keepAlive):
     state=int(raw_input(
"""
/////////////////
// 1) Refresh  //
// 2) Send     //
// 3) Quit     //
/////////////////
"""))
     
     if state==1:
        user_name = raw_input("\n\nEnter Username: ")
        r= requests.get(serverIP+"""?user='"""+user_name+"""'""")
        print(serverIP+"""?='"""+user_name+"""'""")
        print(r)
        print("STATE 1 DONE\n")
        
     if state==2:
         sender = raw_input("\nEnter Username: ")
         reciever = raw_input("\nTo who: ")
         message = raw_input("\nMessage: ")
         pload = {'message':message, 'sender': sender, 'reciever': reciever}
         r= requests.post(serverIP+'/post/', data=pload)
         print(r.text)
         print("state2")

     if state==3:
        print("\nClosing . . .")
        keepAlive=False;
