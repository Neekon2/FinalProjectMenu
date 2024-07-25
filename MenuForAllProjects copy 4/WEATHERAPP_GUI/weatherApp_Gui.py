from tabnanny import check
from tkinter import *
from tkinter import messagebox
import requests
from PIL import ImageTk, Image
from time import strftime
from datetime import datetime

w = Tk()
w.geometry('800x400')
w.title("Weather App")
w.resizable(0,0)

try:
    def weather_data(query):
        res = requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&units=metric&appid=a83c18cd432ec49ad4c0732c22bb5608')
        return res.json()

    Frame(w, width=800, height=50, bg='#353535').place(x=0, y=0)

    # Search bar
    imgSearch = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/search.PNG"))
    def on_entry(e):
        e1.delete(0,'end')
    def on_leave(e):
        if e1.get()=='':
            e1.insert(0, 'Search City')

    e1 = Entry(w, width= 21, fg = 'white', bg= '#353535', border=0)
    e1.config(font=('Calibry', 12))
    e1.bind("<FocusIn>", on_entry)
    e1.bind("<FocusOut>", on_leave)
    e1.insert(0, 'Search City')
    e1.place(x=620, y=15)

    # Date Format
    a = datetime.today().strftime('%B')
    b = (a.upper())
    q = datetime.now().month

    now = datetime.now()
    c = now.strftime('%B')
    month = c[0:3]

    today = datetime.today()
    date = today.strftime("%d")

    def label(a):
        Frame (width=500, height=50, bg="#353535").place(x=0, y=0)

        l1 = Label(w, text=str(a), bg="#353535", fg = "white")
        l1.config(font=("Calibry", 18))
        l1.place(x=20, y=8)

        city = a
        query = 'q=' + city
        w_data = weather_data(query)
        result = w_data

        try:
            check = '{}'.format(result['main']['temp'])
        except:
            messagebox.showinfo("", "City not found!")

        c = (int(float(check)))
        description=("{}".format(result['weather'][0]['description']))
        weather = ("{}".format(result['weather'][0]['main']))
        #print(weather)

        global imgWeather

        if c>10 and weather=="Haze" or weather=="Clear":
            Frame(w,width=800, height=350, bg="#f78954").place(x=0, y=50)
            imgWeather = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/sunny1.PNG"))
            Label(w, image=imgWeather, border=0).place(x=170, y=130)
            bcolor = "#f78954"
            fcolor = "white"

        elif c>10 and weather=="Clouds":
            Frame(w,width=800, height=350, bg="#7492b3").place(x=0, y=50)
            imgWeather = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/cloudy1.PNG"))
            Label(w, image=imgWeather, border=0).place(x=170, y=130)
            bcolor = "#7492b3"
            fcolor = "white"
        
        elif c<=10 and weather=="Clouds":
            Frame(w,width=800, height=350, bg="#7492b3").place(x=0, y=50)
            imgWeather = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/cloudcold.PNG"))
            Label(w, image=imgWeather, border=0).place(x=170, y=130)
            bcolor = "#7492b3"
            fcolor = "white"

        elif c>10 and weather=="Rain":
            Frame(w,width=800, height=350, bg="#60789e").place(x=0, y=50)
            imgWeather = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/rain1.PNG"))
            Label(w, image=imgWeather, border=0).place(x=170, y=130)
            bcolor = "#60789e"
            fcolor = "white"

        elif c<=10 and weather=="Fog" or weather=="Clear":
            Frame(w,width=800, height=350, bg="white").place(x=0, y=50)
            imgWeather = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/cold.PNG"))
            Label(w, image=imgWeather, border=0).place(x=170, y=130)
            bcolor = "white"
            fcolor = "black"

        else:
            Frame(w,width=800, height=350, bg="white").place(x=0, y=50)
            label = Label(w, text=weather, border=0, bg='white')
            label.configure(font=(("Calibry", 18)))
            label.place(x=160, y=130)
            bcolor = "white"
            fcolor = "black"

        w_data = weather_data(query)
        result = w_data

        h = ("Humidity: {}".format(result['main']['humidity']))
        p = ("Pressure: {}".format(result['main']['pressure']))
        tempMax = ("MAX Temp: {}".format(result['main']['temp_max']))
        tempMin = ("MIN Temp: {}".format(result['main']['temp_min']))
        wSpeed = ("Wind Speed: {} m/s".format(result['wind']['speed']))


        l2 = Label(w, text=str(month + " " + date), bg=bcolor, fg=fcolor)
        l2.config(font=("Calibry", 25))
        l2.place(x=330, y=335)

        l3 = Label(w, text=str(h + "%"), bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 12))
        l3.place(x=510, y=95)

        l3 = Label(w, text=str(p + "hPa"), bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 12))
        l3.place(x=510, y=135)

        l3 = Label(w, text=str(tempMin) + "°C", bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 12))
        l3.place(x=510, y=175)

        l3 = Label(w, text=str(tempMax) + "°C", bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 12))
        l3.place(x=510, y=215)

        l3 = Label(w, text=str(wSpeed), bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 12))
        l3.place(x=510, y=255)

        l3 = Label(w, text=str(c) + "°C", bg=bcolor, fg=fcolor)
        l3.config(font=("Calibry", 42))
        l3.place(x=330, y=150)
        
    label(a="Los Angeles")

    def cmd1():
        b = str(e1.get())
        label(str(b))

    Button(w, image=imgSearch, command=cmd1, border=0).place(x=750, y=10)

except:
    
    Frame(w, width=800, height=400, bg='white').place(x=0, y=0)
    global imgNoInternet
    imgNoInternet = ImageTk.PhotoImage(Image.open("/Users/nikkonickerson/Desktop/MenuForAllProjects/WEATHERAPP_GUI/nointernet.PNG"))

    Label(w, image=imgNoInternet, border=0).pack(expend = True)

w.mainloop()
