from tkinter import *
import requests
import json
from keys import API_KEY
from keys import access_key
from tkinter import messagebox
from PIL import ImageTk, Image


class WeatherApp:
    def __init__(self, master):
        self.master = master
        master.geometry("400x250")
        master.resizable(width=False, height=False)
        master.title("Weather App")
        master.iconbitmap(r"icons\cloud_weather_22376.ico")
        master.configure(bg='#29546c')
        self.homeColour = "#29546c"
        self.mainWindowWidgets()

    def mainWindowWidgets(self):
        self.header_label = Label(self.master, text="Air Quality Search", font=('Courier', 20),
                                  bg=self.homeColour, fg="white")
        self.header_label.grid(row=0, column=0, columnspan=2)

        self.header_label2 = Label(self.master, text="Weather Search", font=('Courier', 20),
                                   bg=self.homeColour, fg="white")
        self.header_label2.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        # ZipCode field
        self.zipcode_label = Label(self.master, text="ZipCode:", font=('Courier', 14), bg=self.homeColour, fg="white")
        self.zipcode_entry = Entry(self.master, font=('Courier', 12), width=25)
        self.zipcode_label.grid(row=1, column=0, pady=4, padx=10)
        self.zipcode_entry.grid(row=1, column=1, pady=4)

        # ZipCode Button
        self.zipCode_button = Button(self.master, text="Search", width=10, command=self.searchZipCode)
        self.zipCode_button.grid(row=2, column=1, ipadx=30)

        # City field
        self.city_label = Label(self.master, text="City:", font=('Courier', 14), bg=self.homeColour, fg="white")
        self.city_entry = Entry(self.master, font=('Courier', 12), width=25)
        self.city_label.grid(row=4, column=0, padx=10, pady=4)
        self.city_entry.grid(row=4, column=1)

        # City Button
        self.zipCode_button = Button(self.master, text="Search", width=10, command=self.searchCity)
        self.zipCode_button.grid(row=5, column=1, ipadx=30)

    def searchZipCode(self):
        # print(self.zipcode_entry.get())
        ZipCodeFrame = Toplevel()
        ZipCodeFrame.title("Air Quality")
        ZipCodeFrame.geometry("450x60")
        ZipCodeFrame.iconbitmap(r"icons\sun-and-rain_icon-icons.com_54243.ico")
        ZipCodeFrame.resizable(width=False, height=False)

        url = "http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" \
              "{}&distance=100&API_KEY={}".format(self.zipcode_entry.get().strip(), API_KEY)
        try:
            self.api_request = requests.get(url)
            data = json.loads(self.api_request.content)
            self.city = data[0]['ReportingArea']
            self.quality = data[0]['AQI']
            self.category = data[0]['Category']['Name']

            if self.category == "Good":
                self.weatherColor = "#0C0"
            elif self.category == "Moderate":
                self.weatherColor = "#FFFF00"
            elif self.category == "Unhealthy for Sensitive Groups":
                self.weatherColor = "#ff9900"
            elif self.category == "Unhealthy":
                self.weatherColor = "#FF0000"
            elif self.category == "Very Unhealthy":
                self.weatherColor = "#990066"
            elif self.category == "Hazardous":
                self.weatherColor = "#660000"

            ZipCodeFrame.configure(bg=self.weatherColor)

        except Exception as e:
            data = "Error"
        # print(self.city, self.quality, self.category)

        if self.zipcode_entry.get() == "":
            messagebox.showerror("Empty Field", "Please input ZipCode in the field")
            ZipCodeFrame.destroy()
            self.clear_field()

        elif data == "Error":
            messagebox.showerror("Wrong ZipCode", "Please limit ZipCode to US")
            ZipCodeFrame.destroy()
            self.clear_field()

        else:
            airQualityLabel = Label(ZipCodeFrame,
                                    text="{} Air Quality {} {}".format(self.city, self.quality, self.category),
                                    font=('Helvetica', 15), bg=self.weatherColor)
            airQualityLabel.grid(row=0, column=0, padx=5, pady=10)
            self.clear_field()

    def searchCity(self):
        cityFrame = Toplevel()
        cityFrame.title("Weather App")
        cityFrame.geometry("520x240")
        cityFrame.iconbitmap(r"icons\sun-and-rain_icon-icons.com_54243.ico")
        cityFrame.resizable(width=False, height=False)
        cityFrame.configure(bg='#16394c')
        self.bgColor = '#16394c'

        try:
            params = {
                'access_key': access_key,
                'query': self.city_entry.get()
            }
            api_result = requests.get('http://api.weatherstack.com/current', params)
            data = json.loads(api_result.content)

            self.city_name = data['location']['name']
            self.country = data['location']['country']
            if self.country == 'United States of America':
                self.country = 'USA'
            self.region = data['location']['region']
            self.temperature = data['current']['temperature']
            self.weather_icons = data['current']['weather_icons'][0]
            self.wind = data['current']['wind_speed']
            self.pressure = data['current']['pressure']
            self.precip = data['current']['precip']
            self.weather_description = data['current']['weather_descriptions'][0]

            url = self.weather_icons
            self.resp = requests.get(url, stream=True).raw

            # print(self.city_name,self.country,self.region,self.temperature,self.weather_icons,self.wind,self.pressure,
            # self.precip,self.weather_description)

        except Exception as e:
            data = 'error'

        if self.city_entry.get() == "":
            messagebox.showerror("Empty Field", "Please input a City in the field")
            cityFrame.destroy()
            self.clear_field()

        elif data == 'error':
            messagebox.showerror("Wrong City", "Please input correct City")
            cityFrame.destroy()
            self.clear_field()

        else:
            self.location_label = Label(cityFrame, text='{}, {}'.format(self.city_name, self.country),
                                        font=('Courier', 14), bg=self.bgColor, fg="white", anchor=CENTER)
            self.location_label.grid(row=0, column=1, pady=(20, 10), sticky=NSEW)

            # Icon frame
            self.myImg = ImageTk.PhotoImage(Image.open(self.resp))
            self.iconLabel = Label(cityFrame, padx=10, pady=10, image=self.myImg)
            self.iconLabel.grid(row=1, column=0, pady=(15, 15), padx=(10, 0))
            self.weatherDescription = Label(cityFrame, text="{}".format(self.weather_description), font=('Courier', 14),
                                            bg=self.bgColor, fg="white")
            self.weatherDescription.grid(row=2, column=0)
            self.tempreatureLabel = Label(cityFrame, text="{}°C".format(self.temperature), font=('Courier', 16),
                                          bg=self.bgColor, fg="white")
            self.tempreatureLabel.grid(row=1, column=1)

            windLabel = Label(cityFrame, text="Wind: {}kmph".format(self.wind), font=('Courier', 12),
                              bg=self.bgColor, fg="white")
            windLabel.grid(row=1, column=2, sticky=W)

            precipitationLabel = Label(cityFrame, text="precip: {}mm".format(self.precip), font=('Courier', 12),
                                       bg=self.bgColor, fg="white")
            precipitationLabel.grid(row=2, column=2, sticky=W)

            pressureLabel = Label(cityFrame, text="Pressure: {}mb".format(self.pressure), font=('Courier', 12),
                                  bg=self.bgColor, fg="white")
            pressureLabel.grid(row=3, column=2, sticky=W)
            self.clear_field()

    def clear_field(self):
        self.zipcode_entry.delete(0, END)
        self.city_entry.delete(0, END)


root = Tk()
app = WeatherApp(root)
root.mainloop()
