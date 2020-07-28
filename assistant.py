#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import smtplib
import sys
import pyowm
import random
import operator

engine=pyttsx3.init('sapi5')     #for recognize voice using inbuild voice of windows
inbuild_voice=engine.getProperty('voices')
#print(inbuild_voice[1].id)
engine.setProperty('voice',inbuild_voice[1].id)

def voice(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        voice("Good Morning")
    elif hour>=12 and hour<16:
        voice("Good afternoon")
    elif hour>=16 and hour<23:
        voice("Good evening")
    elif hour>=23 and hour<24:
        voice("GOOD NIGHT!!! PLEASE GO TO SLEEP")
    
    voice("Hi !!! I am your assistant.....How can I help you?????")
    
def command():
    rec1=sr.Recognizer()
    MC=sr.Microphone(device_index=None) 
    with MC as source:
        rec1.pause_threshold=1
        print("Start listening!!!!!.... Now tell ME")
        audio=rec1.listen(source)    #for listening to the microphone, stops executing when it hear nothing
    try:
        print("recognizing!!....")
        query=rec1.recognize_google(audio, language="en-IN")
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Please say it again....I couldn't recognize your voice")
        return "None"
    return query

def get_operator(op):
    return {
        '+':operator.add,
        '-':operator.sub,
        'x':operator.mul,
        'divided':operator.__truediv__,
        'Mod':operator.mod,
        'mod':operator.mod,
        '^':operator.xor,
        }[op]

def evaluate_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator(oper)(op1, op2)


wish()
username="Your email"
password="Your password"
rec1=sr.Recognizer()
while True:

    query=command().lower()
    if 'wikipedia' in query:
        voice("Searching in wikipedia")
        query=query.replace("wikipedia","")
        results=wikipedia.summary(query,sentences=5)
        voice("According to wikipedia")
        voice(results)
        print(results)
    elif "open youtube" in query:
        wb.open("youtube.com")
        
    elif "open google" in query:
        wb.open("google.com")
        
    elif "open stack overflow" in query:
        wb.open("stackoverflow.com")  
        
    elif "open whatsapp" in query:
        wb.open("https://web.whatsapp.com/")
    
    elif "play music" in query:
        m_dir="D:\\Song_testing"
        song=os.listdir(m_dir)
        print(song)
        i=random.randint(0,len(song))
        os.startfile(os.path.join(m_dir,song[i]))
    elif "the time" in query:
        time_now=datetime.datetime.now().strftime("%H:%M:%S")
        voice(f"the time is {time_now}")
        print(time_now)
    elif "open program" in query:
        application="C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
        os.startfile(application)
    elif "google search" in query:
        try:
            
            voice("Searching in Google")
            query=query.replace("google search","")
            print(query)
            #text=rec1.recognize_google(query)
            URL="https://www.google.com/search?q="
            Search_url=URL+query
            wb.open(Search_url)
        except Exception as e:
            print("Cannot be recognized ")
    elif "search in youtube" in query:
        try:
            
            voice("Searching in youtube")
            query=query.replace("search in youtube","")
            print(query)
            #text=rec1.recognize_google(query)
            URL="https://www.youtube.com/results?search_query="
            Search_url=URL+query
            wb.open(Search_url)
        except Exception as e:
            print("Cannot be recognized ")   
        
    elif "search in fb" in query:
        try:
            voice("Searching in FB")
            query=query.replace("search in fb","")
            print(query)
            #text=rec1.recognize_google(query)
            URL_1="https://www.facebook.com/search/top/?q="
            URL_2="&epa=SEARCH_BOX"
            Search_url=URL_1+query+URL_2
            wb.open(Search_url)
        except Exception as e:
            print("Cannot be recognized ")
            
    elif "what\'s up" in query or 'how are you' in query:
            status = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am full of energy', 'I am ready to take your command']
            voice(random.choice(status)) 
            
    elif "current weather " in query:
        try:
            list_wind=[]
            list_temp=[]
            query=query.replace("current weather of","")
            owm=pyowm.OWM('API KEY')
            observation=owm.weather_at_place('query')
            w=observation.get_weather()
            #print(w.get_wind())
            for i,j in w.get_wind().items():
                list_wind.append(j)
            voice(f"the wind speed is {list_wind[0]} and the degree of wind is {list_wind[1]}")
            voice(f"the humidity of {query} is {w.get_humidity()}")
            #print(w.get_temperature('celsius'))
            for i,j in w.get_temperature('celsius').items():
                list_temp.append(j)
            voice(f"the temparature is{list_temp[0]} and the minimum and maximum temparature is{list_temp[1]} and {list_temp[2]}")
            print(f"CITY:\t{query} \nwind speed:\t{list_wind[0]} \ndegree of wind:\t{list_wind[1]} \nhumidity:\t{w.get_humidity()} \ntemparature:\t{list_temp[0]}")
        except Exception as e:
            print("Cannot be recognized")
    elif "send email" in query:
        try:
            dict1={"mail list with name"}
            #print(dict1)
            voice('Whom you want to send Mail?')
            recipient=command()
            recipient=recipient.lower()
            print(recipient)
            reciever=dict1.get(recipient)
            print(reciever)
            mail=smtplib.SMTP('smtp.gmail.com', 587)     
            mail.ehlo()       
            mail.starttls()   
            mail.login(username, password)
            voice("what will I send??")
            mail_body=command()     
            print(mail_body)
            mail.sendmail(username, reciever, mail_body)        
            mail.close()           
            voice("Email has been sent.")
        except Exception as e:
            print("Cannot recognize your voice")

    elif "quit" in query:
        os._exit(0)

    elif "calculate" in query:
        print(query)
        query=query.replace("calculate","")
        answer=(evaluate_expr(*(query.split())))
        voice(answer)
        print("the answer is",answer)    

