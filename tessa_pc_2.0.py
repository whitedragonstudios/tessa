import os
import datetime
import psutil
import requests
import json
import webbrowser
import textwrap
from tkinter import *
#from PIL import ImageTk
#import PIL
# TO DO: Add background pictures

# Define Functions FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
# Universal Functions
def load_config():
    # loads config file from ~/TESSA/config/tessa_config.json
    try: 
        file_handle = open(config_path, 'r')
        config_file = json.loads(file_handle.read())
        file_handle.close 
    except: 
        print("ERROR: (load_config) reading >>> tessa_config.json")
        # If there is a problem loading GUI will return some info in proper format
        config_file = {"city":"Error Loading", "country":"", "longitude":0.0, "latitude":0.0, "source":"Error Loading", "source list": ["Error", "Loading"], "denied list": [""], "news key":"", "weather key":"", "updated":""}
    # print("U *** CONFIG LOADED")
    return config_file

def save_config(new_key, new_value):
    # loads config file and returns a dictionary with config data
    config_file = load_config()
    # writes new data based on key and values passed to it. 
    # writes directly to key of tessa_config.json
    try:
        config_file[new_key] = new_value
        config_file[updated] = datetime.datetime.now().strftime("%m/%d/%y %H:%M")
        config_file = json.dumps(config_file)
        file_handle = open(config_path,"w")
        file_handle.write(config_file)
        file_handle.close()
    except:
        print("ERROR: (save_config) writing to >>> tessa_config.json")
    # print("U  *** CONFIG SAVED")
    return config_file

# API Request Functions
def get_gps(location):
    # only used to get GPS coordiantes needed for get weather api call.
    # this call is only made when you change locations in the menu
    try: 
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': weather_key, 'q': location, "units":"imperial"}
        GPS_response = requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print("ERROR: (get_gps) api request >>>", e)
    # print("A  >>> GPS_response RETURNED")
    return GPS_response

def get_weather(lon, lat):
    # calls weather api and returns dict with weather data
    # requires lon and lat from get_gps function. 
    try: 
        url = 'https://api.openweathermap.org/data/2.5/onecall?'
        params = {'lat':lat,'lon':lon,'APPID':weather_key,"units":"imperial"}
        WEATHER_response = requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print("ERROR: (get_forecast) api request >>>", e)
    # print("A  >>> WEATHER_response RETURNED")
    return WEATHER_response

def get_news(mode):
    # calls news api. Is called twice for a typical refresh
    # mode feeds country or source parameter for request.
    # country is determined by your location in tessa_config.json
    # while source can be changed on the menu screen.
    if mode == "country": req = ('country=%s' %country)
    if mode == "source": req = ('sources=%s' %news_source)
    try: 
        url = ('http://newsapi.org/v2/top-headlines?'
            '%s&apiKey=%s' %(req, news_key))
        NEWS_response = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print("ERROR: (get_news) api request >>>", e)
    # print("A  >>> NEWS_response - %s - RETURNED" %mode)
    return NEWS_response

# Multi Page Functions
def open_url(button_url):
    # function allows you to click and open news articles
    try:
        webbrowser.open(button_url, new=2, autoraise=True)
    except webbrowser.Error as e:
        print("ERROR: (open_url) launch url >>>", e)
    # print("CF --- open_url RUN")

def wind_direction(wind_dir):
    # translates wind direction degrees from the api request into
    # cardianal directions. Used in forecast and enviormental pages.
    try:
        wind_float = float(wind_dir)
        if wind_float in range(23, 66): cardinal = 'NE'
        elif wind_float in range(67, 112): cardinal = 'E'
        elif wind_float in range(113, 156): cardinal = 'SE'
        elif wind_float in range(157, 202): cardinal = 'S'
        elif wind_float in range(203, 246): cardinal = 'SW'
        elif wind_float in range(247, 292): cardinal = 'W'
        elif wind_float in range(293, 336): cardinal = 'NW'
        else: cardinal = 'N' # 0-22 and 337-360
    except:
        # if for any reason wind direction can't be translated it apears blank.
        cardinal = ""
        print("ERROR: (wind_direction) assigning >>> wind_dir")
    # print("CF --- wind_direction RUN")
    return cardinal

def temp_alert(temp, label):
    # changes label colors based on tempurature. starts blue ends red
    if temp >= 80: 
        # if temps are critical changes text to warning
        label.config(text="Warning: %d°C" %temp)
        label['bg'] = '#ff0000'
    elif temp >= 75.0: label['bg'] = '#ff4000'
    elif temp >= 70.0: label['bg'] = '#ff8000'
    elif temp >= 65.0: label['bg'] = '#ffbf00'
    elif temp >= 60.0: label['bg'] = '#ffff00'
    elif temp >= 56.0: label['bg'] = '#bfff00'
    elif temp >= 53.0: label['bg'] = '#80ff00'
    elif temp >= 50.0: label['bg'] = '#40ff00'
    elif temp >= 47.0: label['bg'] = '#00ff00'
    elif temp >= 44.0: label['bg'] = '#00ff40'
    elif temp >= 41.0: label['bg'] = '#00ff80'
    elif temp >= 38.0: label['bg'] = '#00ffbf'
    elif temp >= 35.0: label['bg'] = '#00ffff'
    elif temp >= 32.0: label['bg'] = '#00bfff'
    elif temp >= 29.0: label['bg'] = '#007fff'
    elif temp >= 26.0: label['bg'] = '#0040ff'
    else: label['bg'] = '#0000ff'
    # print("CF --- temp_alert RUN")

def sys_report():
    # gets sys info formats it into strings to display on labels
    # Variable values
    gb = 1000000000
    cpu_percent = psutil.cpu_percent(1)
    cpu_speed = psutil.cpu_freq().current
    temp_cpu = psutil.sensors_temperatures()['cpu_thermal'][0][1]
    ram_percent = psutil.virtual_memory().percent
    ram_used = psutil.virtual_memory().used / gb
    ram_free = psutil.virtual_memory().free / gb
    ram_total = psutil.virtual_memory().total / gb
    swap_percent = psutil.swap_memory().percent
    swap_free = psutil.swap_memory().free / gb
    swap_used = psutil.swap_memory().used / gb
    swap_total = psutil.swap_memory().total / gb
    # String formating
    cpu_string = "CPU: %d%%\nClock: %d Mhz" %(cpu_percent, cpu_speed)
    C_temp_string = "Temperature\n%.02f°C" %temp_cpu
    # F_temp_string = " CPU: %d°F " %((temp_cpu * 1.8) + 32)
    ram_string = "Free: %.03f GB \nUsed: %.03f GB \nTotal: %.03f GB" %(ram_free, ram_used, ram_total)
    swap_string = "Free: %.03f GB\nUsed: %.03f GB\nTotal: %.03f GB" %(swap_free, swap_used, swap_total)
    # Function Calls --- pass source hardware and label name
    f6_sys_alerts(cpu_percent, cpu_data)
    f6_sys_alerts(ram_percent, ram_sum)
    f6_sys_alerts(swap_percent, ram_sum)
    temp_alert(temp_cpu, temp_data)
    # Label text assignments
    cpu_data['text'] = cpu_string
    temp_data['text'] = C_temp_string
    ram_sum['text'] = "RAM: %s%%" %ram_percent
    ram_data['text'] = ram_string
    swap_sum['text'] = "SWAP: %s%%" %swap_percent
    swap_data['text'] = swap_string
    # print("CF <<< SYS STAT UPDATED")

def page_turn(index, direction):
    if direction == "jump":
        screen_index = index
    if direction == "back":
        screen_index = index - 1
    if direction == "next":
        screen_index = index + 1
    pages_list[screen_index].tkraise()

#Page Exclusive Functions
def f1_weather_report(weather_json):
    # takes weather api response and formats it to variables
    # plugs those variables into a string for label display
    try:
        conditions = weather_json['current']['weather'][0]['description']
        temp = weather_json['current']['temp']
        feel = weather_json['current']['feels_like']
        humidity = weather_json['current']['humidity']
        uvi = weather_json['current']['uvi']
        visibillity = int(weather_json['current']['visibility']* 0.000621)
        wind_speed = weather_json['current']['wind_speed']
        cardinal = wind_direction(weather_json['current']['wind_deg'])
        sunrise = datetime.datetime.fromtimestamp(weather_json['current']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(weather_json['current']['sunset']).strftime('%H:%M')
        # format string
        local = (("{}\n"+"Temp: {}°F\n"+"Feel: {}°F\n" +
                        "Humidity: {}%\n"+"UV Index: {}\n"+"Sight: {} mi\n"+"Wind: {} {} mph\n" +
                        "Sunrise: {}\n"+"Sunset: {}\n")
                        .format(conditions.title(), temp, feel, humidity, uvi, visibillity, 
                        cardinal, wind_speed, sunrise, sunset))
    except:
        local = "Error: weather data"
        print("ERROR: (format_weather) formating >>> local(str)")
    local_data['text'] = local
    # print("F1 <<< WEATHER UPDATED")

def f2_forecast_report(weather_json):
    # takes weather api response and formats it to variables
    # plugs those variables into a string for label display
    forecast_report = []
    # destroys old auto created labels before new ones are created
    for btn in fc_lable_list:
        btn.destroy()
    try:
        daily_list = weather_json['daily']
        # uses for loop to parse 8 list entries
        for index, item in enumerate(daily_list, start=1):
            timestamp = item['dt']
            date = datetime.datetime.fromtimestamp(timestamp).strftime('%a, %b %d \'%y')
            temp_high = item['temp']['max']
            temp_low = item['temp']['min']
            conditions = item['weather'][0]["description"].title()
            humidity = item['humidity']
            wind_speed = item['wind_speed']
            wind_dir = wind_direction(item['wind_deg'])
            uvi = item['uvi']
            single_forecast = ('''%s\n%s\nHigh: %s°F\nLow: %s°F\nHumidity: %s%%\nUV Index: %s\nWind: %s %0.1f mph''' % (date, conditions, temp_high, temp_low, humidity, uvi, wind_dir, wind_speed))
            forecast_report.append(single_forecast)
            if index == 8:
                break
    except:
        print('ERROR: (format_weather) formatting >>> forecast_report')
    # automatically creates labels for each entry in forecast list
    # row and column assignment is automatically handled as well.
    try:
        iterator = [1, 2, 3, 4, 5, 6, 7, 8]
        for addend, fcr in zip(iterator, forecast_report):
            fc_label = Label(f2_fc, bg=Hbg, font=Sf, padx=10, pady=10)
            fc_label.config(text=fcr, borderwidth=2, relief="groove", highlightbackground=Tbg)
            if addend > 4:
                L_row = 2
                L_col = addend - 4
            else: 
                L_row = 1
                L_col = addend
            fc_label.grid(row=L_row, column=L_col, sticky=N+S+W+E)
            fc_lable_list.append(fc_label)
    except:
        print("ERROR: (get_forecast) label creation >>> forecast_report)")
    # print("F2 <<< FORECAST UPDATED")

def f3_alert_report(weather_json):
    # takes weather api response extracts alerts if they exist
    alert_list = ''
    if 'alerts' not in weather_json:
        alert_list = "No Alerts"
        jump_alerts.config(text=" No Alerts " , bg=Hbg)
        # if no alerts enviormental page says no alerts and color is header color
        # print("F3 --- NO Alerts Found ---")
    else:
        # if alerts are present changes enviormental page to "weather alerts" and the color to red.
        jump_alerts.config(text=" Alerts " , bg='Red')
        # print("F3 --- Alerts Found ---")
        alerts = weather_json['alerts']
        # if alerts are present formats them to strings from display.
        try:
            for item in alerts:
                event = item['event']
                details = item['description']
                try:
                    details = details.replace('\n', ' ').replace('- ', '').replace('...', ' ')
                    info = dict(re.findall(r"[*] (WHAT|WHERE|WHEN) ([^*]+)", details))
                    what = textwrap.fill(f"{event.title()}: {info['WHAT']}", 68)
                    where = textwrap.fill(f"Where: {info['WHERE']}", 68)
                    when = textwrap.fill(f"When: {info['WHEN']}", 68)
                    single_alert = f"{what}\n{where}\n{when}\n\n"
                    alert_list += single_alert
                except: 
                    # sometimes alerts can't be parsed with regex. Then it displays raw text.
                    single_alert = textwrap.fill(details, 68)
                    alert_list += single_alert
                    # print("F3 ^^^ Alert not Formated")
        except (KeyError, ValueError):
            alerts = "Alerts Error"
            print('ERROR: (format_weather) formatting >>> alerts')
    alert_label['text'] = alert_list
    # print("F3 <<< ALERTS UPDATED")

def f4_headline_report():
    # takes news api response and formats it to variables
    # plugs those variables into a string for label display
    # headlines based on country saved to tessa_config.json
    headline_json = get_news("country")
    article_list = headline_json['articles']
    headline_list = []
    url_list = []
    counter = 1
    # destroys all button every time it is refreshed
    for btn in headline_button_list:
        btn.destroy()
    try:
        for item in article_list:
            source_id = item['source']['name']
            # print(source_id)
            if counter < 9 and source_id not in denied_list:
                counter += 1 
                headline_list.append(item['title'])
                url_list.append(item['url'])
    except: 
        print("ERROR: (f4_headline_report) appending >>> headline_list, url_list")
    # automatically creates buttons with article text and url link
    # if you click on them. row/column assignment automatic.
    try:
        iterator = [1, 2, 3, 4, 5, 6, 7, 8]
        for addend, headline, urlS in zip(iterator, headline_list, url_list):
            packaged = textwrap.fill(headline, 35)
            hl_button = Button(f4_hl, font=Sf, width=34, bg=Hbg, activebackground=Hbg, highlightbackground=Tbg)
            hl_button.config(command=(lambda urlS=urlS: open_url(urlS)), text=(packaged))
            if addend > 4:
                B_row = addend
                B_col = 2
            else: 
                B_row = addend + 4
                B_col = 0
            hl_button.grid(row=B_row, column=B_col, sticky=N+S+E+W, columnspan=2)
            headline_button_list.append(hl_button)
    except:
        print("ERROR: (f4_headline_report) generating buttons >>> headline_list")
    # print("F4 <<< HEADLINES UPDATED")

def f5_news_report():
    # takes news api response and formats it to variables
    # plugs those variables into a string for label display
    # source based on source saved to tessa_config.json
    # source can be selected via the settings menu
    news_json = get_news('source')
    article_list = []
    article_url = []
    article_number = 8
    # destroys all button every time it is refreshed
    for btn in news_button_list:
        btn.destroy()
    try:
        source_title['text'] = " - %s - " %(news_json['articles'][0]['source']['name'])
        articles_response = news_json['articles']
        for item in articles_response: 
            title = item['title']
            if article_number > 0:
                if len(title) > 14:
                    article_list.append(item['title'])
                    article_url.append(item['url'])
                    article_number += -1
                else:
                    print('Article too short - skipped')
                    article_number += 1
            else: 
                break
    except:
        print('ERROR: (f5_news_reports) formatting >>> article_list')
        article_list = ["ERROR: retrieving news articles"]
        article_url = ['www.google.com']
    # automatically creates buttons with article text and url link
    # if you click on them. row/column assignment automatic.
    try:
        iterator = [1, 2, 3, 4, 5, 6, 7, 8]
        for addend, article, url in zip(iterator, article_list, article_url):
            data = textwrap.fill(article , 35)
            a_button = Button(f5_news, width=34, bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
            a_button.config(command=(lambda url=url: open_url(url)),text=(data), font=Sf)
            if addend > 4:
                L_row = addend
                L_col = 2
            else: 
                L_row = addend + 4
                L_col = 0
            a_button.grid(row=L_row, column=L_col, sticky=N+S+W+E, columnspan=2)
            news_button_list.append(a_button)
    except:
        print("ERROR: (f5_news_reports) generating labels >>> article_list")
    # print("F5 <<< NEWS UPDATED")

def f6_storage_report():
    # collects memory data and displays to label.
    hdd = "/media/theexchange/Archive"
    gb = 1000000000
    tb = 1000000000000
    sd_percent = psutil.disk_usage("/").percent
    sd_free = psutil.disk_usage("/").free / gb
    sd_used = psutil.disk_usage("/").used / gb
    sd_total = psutil.disk_usage("/").total / gb
    sd_string = "Free: %.03f GB\nUsed: %.03f GB\nTotal: %.03f GB" %(sd_free, sd_used, sd_total)
    hdd_percent = psutil.disk_usage(hdd).percent
    hdd_free = psutil.disk_usage(hdd).free / tb
    hdd_used = psutil.disk_usage(hdd).used / tb
    hdd_total = psutil.disk_usage(hdd).total / tb
    hdd_string = "Free: %.03f TB\nUsed: %.03f TB\nTotal: %.03f TB" %(hdd_free, hdd_used, hdd_total)
    sd_sum['text'] = "SD:%s%%" %sd_percent
    sd_data['text'] = sd_string
    hdd_sum['text'] = "HDD:%s%%" %hdd_percent
    hdd_data['text'] = hdd_string
    f6_sys_alerts(sd_percent, sd_sum)
    f6_sys_alerts(hdd_percent, hdd_sum)
    # print("F6 <<< STORAGE UPDATED")

def f6_sys_alerts(hardware, label):
    # changes color of sys info labels based on usage %
    # parameters are the type of hardwars sd, hdd, etc. and 
    # the label to change color.
    if hardware >= 95.0: label['bg'] = '#ff0000'
    elif hardware >= 90.0: label['bg'] = '#ff4000'
    elif hardware >= 80.0: label['bg'] = '#ff8000'
    elif hardware >= 70.0: label['bg'] = '#ffbf00'
    elif hardware >= 60.0: label['bg'] = '#ffff00'
    elif hardware >= 50.0: label['bg'] = '#bfff00'
    elif hardware >= 40.0: label['bg'] = '#80ff00'
    elif hardware >= 30.0: label['bg'] = '#40ff00'
    elif hardware >= 20.0: label['bg'] = '#00ff00'
    elif hardware >= 10.0: label['bg'] = '#00ffff'
    else: label['bg'] = '#0000ff'
    # print("F6 --- sys_alerts RUN")

def f7_change_location(*args):
    # Settings menu change location. calls get_gps with the new location
    # then writes directly to the tessa_config.json file with data
    # from the api. 
    location = loc_entry.get()
    loc_entry.delete(0, END)
    response = get_gps(location)
    try:
        save_config('city', response['name'])
        save_config('country', response['sys']['country'])
        save_config('longitude', response['coord']['lon'])
        save_config('latitude', response['coord']['lat'])
    except:
        print("ERROR: (f7_change_location) saving  >>> tessa_config.json")
    # Reassigns global variables from the changed config file.
    global config_handle, city, country, lon, lat
    config_handle = load_config()
    city = config_handle['city']
    country = config_handle['country']
    lon = config_handle["longitude"]
    lat = config_handle["latitude"]
    weather_json = get_weather(lon, lat)
    f1_weather_report(weather_json)
    loc_current['text'] = ("%s, %s" %(city, country))
    # print("F7 <<< LOCATION CHANGED")

def f7_change_keys(type): 
    # opens an new window to enter the api keys. Type parameter
    # allows one function to change either weather or news key
    def key_save(key_type):
        # nested function saves the new key to config file. 
        new_api_key = api_key.get()
        api_key.delete(0, END)
        save_config(key_type, new_api_key)
        global weather_key, news_key
        config_handle = load_config()
        # loads config file and reassigns variables from there.
        weather_key = config_handle['weather key']
        news_key = config_handle['news key']
        # displays the key you entered for confirmation
        readback_title['text'] = ("New %s added:" %key_type)
        readback['text'] = config_handle[key_type]
        # print("F7 <<< API KEY CHANGED")
        
    # f7_change_keys Main setup
    cKey = Toplevel(root, bg=Abg)
    cKey.geometry("720x300")
    if type == 'W':
        cKey.title('Change Weather Key')
        header = "enter API key from openweathermap.org"
        key_type = 'weather key'
    if type == 'N':
        header = "enter API key from newsapi.org"
        cKey.title('Change News Key')
        key_type = 'news key'
    title = Label(cKey, text=header, font=Sf, padx=20, pady=20, bg=Abg)
    api_key = Entry(cKey, width=38, font=Sf)
    button_confirm = Button(cKey, text='Confirm', font=Sf, padx=20, pady=20)
    button_confirm.config(command=lambda:key_save(key_type))
    button_close = Button(cKey, text='Close', font=Sf, padx=20, pady=20)
    button_close.config(command=cKey.destroy)
    readback_title = Label(cKey,font=Sf, bg=Abg)
    readback = Label(cKey, font=Sf, bg=Abg)
    # Grid Assignments
    title.grid(row=0, column=0, columnspan=2, sticky=N)
    api_key.grid(row=1, column=0, columnspan=2, sticky=N)
    button_confirm.grid(row=2, column=0, sticky=N+S+W+E)
    button_close.grid(row=2, column=1, sticky=N+S+E+W)
    readback_title.grid(row=3, column=0, columnspan=2, sticky=N)
    readback.grid(row=4, column=0, columnspan=2, sticky=N)

def f7_change_news_list():
    # opens an new window to enter the news sources.
    def save_list():
        # nested function checks if the news source is already in the list
        # it if is it deletes it. If it isn't it adds it.
        # note there is no check for valid entries.
        entered_source = cNews_entry.get()
        cNews_entry.delete(0, END)
        if entered_source in news_source_list:
            news_source_list.remove(entered_source)
            save_config('source list', news_source_list)
            print("%s removed from list" %entered_source)
            cNews_confirm['text'] = "%s removed from list" %entered_source
        else:
            news_source_list.append(entered_source)
            save_config('source list', news_source_list)
            print("%s added to list" %entered_source)
            cNews_confirm['text'] = "%s added to list" %entered_source
        # destroys buttons so they can be refreshed after entering a new source.
        for btn in cns_button_list:
            btn.destroy()
        # runs f7_change_source_buttons to generate new buttons from config file list.
        f7_change_source_buttons()
    cNews = Toplevel(root, bg=Abg)
    cNews.geometry("600x350")
    cNews.title("Change News List")
    cNstring = textwrap.fill("Enter a news source id to add it to the menu screen. Get the news source's 'id' from newsapi.org. To remove a news source type it in the box exactly like it appears. You can have up to 16 new sources entered at a time. Selecting one will change the main news page.", 40)
    cNews_header = Label(cNews, text=cNstring, font=Sf, bg=Abg)
    cNews_entry = Entry(cNews, width=24, font=Nf)
    cNews_accept = Button(cNews, text="Accept", command=lambda: save_list())
    cNews_close = Button(cNews, text="Close", command=cNews.destroy)
    cNews_confirm = Label(cNews, font=Nf, bg=Abg)
    # Grid arrangment
    cNews_header.grid(row=0, column=0, columnspan=2)
    cNews_entry.grid(row=1, column=0)
    cNews_accept.grid(row=1, column=1)
    cNews_confirm.grid(row=2, column=0, columnspan=2)
    cNews_close.grid(row=3, column=0, columnspan=2)

def f7_change_source_buttons():
    # automatically creates buttons for each news source the user enters
    # clicking each button will change the news source page. 
    def CNS(cns_key, cns_value): # Change News Source
        # saves the source user clicks on to the news source key in config file.
        save_config(cns_key, cns_value)
        new_source = textwrap.shorten((cns_value.replace('-', ' ')), 16).upper().strip('[...]')
        menu_news_title['text'] = "  News Source: %s  " %new_source
        global news_source
        news_source = cns_value
        f5_news_report()
        # print("F7 --- New Source: %s" %new_source)

    try:
        iterator = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        for addend, title in zip(iterator, news_source_list):
            packed = textwrap.shorten((title.replace('-', ' ')), 16).upper().strip('[...]')
            cns_button = Button(news_frame,text=(packed), font=Sf, width=16, pady=6)
            cns_button.config(command=(lambda title=title: CNS('source', title)))
            if addend > 10:
                B_row = addend
                B_col = 1
            else: 
                B_row = addend + 8
                B_col = 0
            cns_button.grid(row=B_row, column=B_col)
            cns_button_list.append(cns_button)
    except:
        print("ERROR: (get_news) generating labels >>> article_list")
    # print("F7 <<< NEWS LIST UPDATED")

# Setup ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# sets path for where to find the tessa_config.json file 
usr_home = os.path.expanduser('~')
config_path = '{}/TESSA/config/tessa_config.json'.format(usr_home)
# various lists used to store automatically created buttons
fc_lable_list = []
headline_button_list = []
news_button_list = []
cns_button_list = []

# Fonts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Lf = ('Hack', 30) # large font
Tf = ('Arial', 24) # title font
Nf = ('Courier', 22) # standard font
Ff = ('DejaVu Sans Mono', 25) # fansy font
Sf = (('Courier', 18)) # mini font

# Colors <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
Abg = '#8fbde3' # all background colors 'cornflower blue'
Bbg = '#5dadee' # button active background 'dark cornflower blue'
Hbg = '#9fcef5' # header background color 'light cornflower blue'
Tbg = 'black' # text box color
Zbg = 'white' # alternative font color NOT used currently

# Config ===================================================================================
# Variables are loaded from tessa_config.json these values determine
# nearly all behavior of the entire program.
config_handle = load_config()
city = config_handle['city']
country = config_handle['country']
lon = config_handle["longitude"]
lat = config_handle["latitude"]
weather_key = config_handle['weather key']
news_source = config_handle['source']
news_source_list = config_handle['source list']
new_source = textwrap.shorten((config_handle["source"].replace('-', ' ')), 16).upper().strip('[...]') 
# TO DO: Simplify this code ^
# TO DO: change denied list over to approved list. Make approve list editable in settings
denied_list = config_handle['denied list']
news_key = config_handle['news key']
updated = config_handle['updated']

# TK Loop **********************************************************************************
root = Tk()
root.title("TESSA")
root.geometry('1024x600')
# root.iconbitmap('path')
root.configure(background=Abg)

# Top Level Frames @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
f0_empty = Frame(root)
f1_env = Frame(root, bg=Abg, width=1024, height=600)
f2_fc = Frame(root, bg=Abg, width=1024, height=600, padx=1)
f3_alert = Frame(root, bg=Abg, width=1024, height=600)
f4_hl = Frame(root, bg=Abg, width=1024, height=600, padx=6)
f5_news = Frame(root, bg=Abg, width=1024, height=600, padx=6)
f6_sys = Frame(root, bg=Abg, width=1024, height=600)
f7_set = Frame(root, bg=Abg, width=1024, height=600)
# Grid Top Level Frames ##########################################
f1_env.grid(row=0, column=0, sticky=N+S+E+W)
f2_fc.grid(row=0, column=0, sticky=N+S+E+W)
f3_alert.grid(row=0, column=0, sticky=N+S+E+W)
f4_hl.grid(row=0, column=0, sticky=N+S+E+W)
f5_news.grid(row=0, column=0, sticky=N+S+E+W)
f6_sys.grid(row=0, column=0, sticky=N+S+E+W)
f7_set.grid(row=0, column=0, sticky=N+S+E+W)
pages_list = [f0_empty, f1_env, f2_fc, f3_alert, f4_hl, f5_news, f6_sys, f7_set]

# F1 Enviorment F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1_F1
local_frame = Frame(f1_env, bg=Abg, padx=12, pady=10)
local_title = Label(local_frame,  font=Lf, bg=Hbg, borderwidth=2, relief="solid")
local_title.config(text=(" %s, %s " %(city, country)))
local_data = Label(local_frame, font=Lf, bg=Abg)
jump_frame = Frame(f1_env, bg=Abg, padx=12, pady=10)
jump_forecast = Button(jump_frame, bg=Hbg, text="Forecast", activebackground=Bbg, highlightbackground=Tbg)
jump_forecast.config(command=lambda: page_turn(2, "jump"), font=Lf)
jump_alerts = Button(jump_frame, bg=Hbg, text="Alerts", activebackground=Bbg, highlightbackground=Tbg)
jump_alerts.config(command=lambda: page_turn(3, "jump"), font=Lf)
jump_headlines = Button(jump_frame, bg=Hbg, text="Headlines", activebackground=Bbg, highlightbackground=Tbg)
jump_headlines.config(command=lambda: page_turn(4, "jump"), font=Lf)
jump_source = Button(jump_frame, bg=Hbg, text="News", activebackground=Bbg, highlightbackground=Tbg)
jump_source.config(command=lambda: page_turn(5, "jump"), font=Lf)
jump_system = Button(jump_frame, bg=Hbg, text="System", activebackground=Bbg, highlightbackground=Tbg)
jump_system.config(command=lambda: page_turn(6, "jump"), font=Lf)
jump_settings = Button(jump_frame, bg=Hbg, text="Settings", activebackground=Bbg, highlightbackground=Tbg)
jump_settings.config(command=lambda: page_turn(7, "jump"), font=Lf)
# F1 Enviorment Grid #########################################################################
local_frame.grid(row=0, column=0, sticky=N+S+W+E)
local_title.grid(row=0, column=1, padx=60, pady=10)
local_data.grid(row=1, column=1)
jump_frame.grid(row=0, column=1, sticky=N+S+W+E)
jump_forecast.grid(row=0, column=0, sticky=N+W+S+E)
jump_alerts.grid(row=1, column=0, sticky=N+W+S+E)
jump_headlines.grid(row=2, column=0, sticky=N+W+S+E)
jump_source.grid(row=3, column=0, sticky=N+W+S+E)
jump_system.grid(row=4, column=0, sticky=N+W+S+E)
jump_settings.grid(row=5, column=0, sticky=N+W+S+E)

# F2 Forecast F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2_F2
forecast_title = Label(f2_fc, padx=20, pady=5, font=Tf, bg=Hbg)
forecast_title.config(text="Forecast", borderwidth=2, relief="solid")
next_button = Button(f2_fc, text="Next", command=lambda: page_turn(2, "next"))
next_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(f2_fc, text="Back", command=lambda: page_turn(2, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
# F2 Forecast Grid #########################################################################
forecast_title.grid(row=0, column=2, pady=10, columnspan=2)
back_button.grid(row=0, column=0, columnspan=2)
next_button.grid(row=0, column=4)

# F3 Alerts F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3_F3
alerts_title = Label(f3_alert, padx=20, pady=5, font=Tf, bg=Hbg)
alerts_title.config(text="Severe Weather Alerts", borderwidth=2, relief="solid")
alert_label = Label(f3_alert, justify=LEFT, bg=Abg, font=Sf, padx=20, pady=10)
next_button = Button(f3_alert, text="Next", command=lambda: page_turn(3, "next"))
next_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(f3_alert, text="Back", command=lambda: page_turn(3, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
# F3 Alerts Grid ###########################################################################
alerts_title.grid(row=0, column=1, pady=10)
back_button.grid(row=0, column=0)
next_button.grid(row=0, column=2)
alert_label.grid(row=1, column=0, columnspan=3)

# F4 Headlines F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4_F4
news_sum_title = Label(f4_hl, font=Tf, bg=Hbg)
news_sum_title.config(text=" - Top Headlines - ", borderwidth=2, relief="solid")
next_button = Button(f4_hl, text="Next", command=lambda: page_turn(4, "next"))
next_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(f4_hl, text="Back", command=lambda: page_turn(4, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
# F4 Headlines Grid #########################################################################
news_sum_title.grid(row=0, column=1, padx=20, pady=10, columnspan=2)
back_button.grid(row=0, column=0)
next_button.grid(row=0, column=3, columnspan=2)

# F5 News F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5_F5
source_title = Label(f5_news, bg=Hbg, font=Tf, borderwidth=2, relief="solid")
next_button = Button(f5_news, text="Next", command=lambda: page_turn(5, "next"))
next_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(f5_news, text="Back", command=lambda: page_turn(5, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
# F5 News Grid ##############################################################################
source_title.grid(row=0, column=1, columnspan=2, pady=10)
back_button.grid(row=0, column=0)
next_button.grid(row=0, column=3, columnspan=2)

# F6 System Status F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6_F6
system_title = Label(f6_sys, font=Lf, bg=Hbg, borderwidth=2, relief="solid")
system_title.config(text="System Status")
ram_sum = Label(f6_sys, font=Ff, justify=LEFT, borderwidth=4, relief="sunken")
ram_data = Label(f6_sys, font=Ff, justify=LEFT, bg=Abg)
swap_sum = Label(f6_sys, font=Ff, justify=LEFT, borderwidth=4, relief="sunken")
swap_data = Label(f6_sys, font=Ff, justify=LEFT, bg=Abg)
sd_sum = Label(f6_sys, font=Ff, justify=LEFT, borderwidth=4, relief="sunken")
sd_data = Label(f6_sys, font=Ff, justify=LEFT, bg=Abg)
hdd_sum = Label(f6_sys, font=Ff,  justify=LEFT, borderwidth=4, relief="sunken")
hdd_data = Label(f6_sys, font=Ff, justify=LEFT, bg=Abg)
cpu_data = Label(f6_sys, font=Ff, justify=LEFT, borderwidth=4, relief="raised")
temp_data = Label(f6_sys, font=Ff, justify=CENTER, borderwidth=4, relief="sunken")
next_button = Button(f6_sys, text="Next", command=lambda: page_turn(6, "next"))
next_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(f6_sys, text="Back", command=lambda: page_turn(6, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
# F6 Sys Grid ################################################################################
back_button.grid(row=0, column=0)
system_title.grid(row=0, column=1)
next_button.grid(row=0, column=2)
ram_sum.grid(row=1, column=0, padx=10, pady=5)
ram_data.grid(row=2, column=0, padx=10, pady=5)
swap_sum.grid(row=1, column=1, padx=10, pady=5)
swap_data.grid(row=2, column=1, padx=10, pady=5)
#storage_title.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
sd_sum.grid(row=3, column=0, padx=10, pady=5)
sd_data.grid(row=4, column=0, padx=10, pady=5)
hdd_sum.grid(row=3, column=1, padx=10, pady=5)
hdd_data.grid(row=4, column=1, padx=10, pady=5)
cpu_data.grid(row=2, column=2,pady=5)
temp_data.grid(row=4, column=2, pady=5)

# F7 Settings F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7_F7
menu_title = Label(f7_set, font=Tf, bg=Hbg, borderwidth=2, relief="solid", padx=10, pady=10)
menu_title.config(text='Settings Menu')
# Setup Frame
setup_frame = Frame(f7_set, bg=Abg)
jump_home = Button(setup_frame, text="Home", command=lambda: page_turn(1, "jump"))
jump_home.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
back_button = Button(setup_frame, text="Back", command=lambda: page_turn(7, "back"))
back_button.config(bg=Hbg, activebackground=Bbg, highlightbackground=Tbg)
loc_header = Label(setup_frame, font=Tf, bg=Hbg, borderwidth=2, relief="solid")
loc_header.config(text='  Location  ')
loc_current = Label(setup_frame, text=("%s, %s" %(city, country)), font=Sf, bg=Abg)
loc_entry = Entry(setup_frame, width=20, font=Sf, justify=RIGHT)
loc_entry.bind('<Return>', f7_change_location)
loc_button = Button(setup_frame, text="Change\nLocation", font=('Courier', 10))
loc_button.config(command=f7_change_location)
news_source_list_button = Button(setup_frame, text="Change News List", font=Sf)
key_header = Label(setup_frame, font=Tf, bg=Hbg, borderwidth=2, relief="solid")
key_header.config(text="  Change API Keys  ")
key_weather_button = Button(setup_frame, text="Weather Key", ) 
key_weather_button.config(command=lambda: f7_change_keys('W'), font=Sf)
key_news_button = Button(setup_frame, text="News Key", font=Sf)
key_news_button.config(command=lambda: f7_change_keys('N'))
# News Frame
news_frame = Frame(f7_set, bg=Abg, padx=20)
menu_news_title = Label(news_frame, font=Sf, bg=Hbg, borderwidth=2, relief="solid")
menu_news_title.config(text=("  News Source: %s  " %new_source))
news_source_list_button.config(command=f7_change_news_list)
# Grid Setup Frame ###########################################################################
menu_title.grid(row=0, column=0, columnspan=3, pady=5)
# Setup Frame Grid
setup_frame.grid(row=1, column=0, sticky=N, padx=8)
back_button.grid(row=0, column=0, columnspan=2, sticky=N+W+S+E)
jump_home.grid(row=0, column=2, columnspan=2, sticky=N+W+S+E)
loc_header.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
loc_current.grid(row=2, column=0, columnspan=4)
loc_entry.grid(row=3, column=0, columnspan=3)
loc_button.grid(row=3, column=3)
news_source_list_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
key_header.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
key_weather_button.grid(row=6, column=0, columnspan=2)
key_news_button.grid(row=6, column=2, columnspan=2)
# Grid News Frame
news_frame.grid(row=1, column=1, sticky=N, padx=5)
menu_news_title.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Function Calls +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def refresher():
    # most important function. refreshes each page with new data every 30 minutes
    weather_json = get_weather(lon, lat)
    f1_weather_report(weather_json)
    f2_forecast_report(weather_json)
    f3_alert_report(weather_json)
    f4_headline_report()
    f5_news_report()
    f6_storage_report()
    f7_change_source_buttons()
    root.after(1800000, refresher) # 30 minute cycle
    print("|||||| REFRESHER %s" %datetime.datetime.now().strftime("%H:%M"))
def short_timer():
    # shorter version of the refresher function. for system information and sensor which need
    # shorter refresh cycles.
    sys_report()
    root.after(60000, short_timer) # one minute
    # print("   ||| SHORT Refresh")

f1_env.tkraise()
refresher()
short_timer()
root.mainloop()

# Version ----------------------------------------------------------------------------------
# STRUCTURE Tessa will being at v1.0 each page added will...
# inciment the decimal value. Alpha will be after v1.7. Beta will be v2.0

# 1.0
# combine all import values
# combine all variables
# combine all settings
# normalize all setting, variables
# restructure load and save functions for efficiency
# bring in cross page functions

# 1.1
# intergrated enviormental_1.1.py
# added and modified f1_sensor from health_check_1.1.py 
# f1_sensor now edits lables on F1 and F5
# modified format_weather to assign data to F1. 
# removed get_local_weather >>> obsolete

# 1.2 
# intergrated forecast_1.1.py
# added get_weather from forecast_1.1.py to format weather
# added alert icon on F1
# refactored fonts

# 1.3 
# intergrated alerts_1.1.py
# modified format weather to include alerts formating
# refactored fonts
# pulled page functions out of format_weather >>> f1_weather_report, f2_forecast_report...
# ...f3_alert_report. Each is not called in refresher. get weather is called in refresher...
# ... json returned is assigned to weather_json and passed throug each function.

# 1.4
# intergrated headline_1.1.py
# ajdusted get news to be passed a param so it can be used for...
# ...F4 and F5 
# normalized fonts

# 1.5
# intergrated news_1.1.py 
# refactored in function variables

# 1.6 
# intergated healthcheck_1.1.py
# refactored function names
# cleaned variables fonts and bg
# normalized print outputs

# 1.7 ALPHA VERSION
# intergrate settings_menu_1.1.py #
# added short_timer for sensor and sys stat updates.
# refactored settings_menu fonts and functions
# added global assignement config load and function calls withint settings functions
# moved grid arrangements to be with their page assignments
# general cleaning

# 1.8 ALPHA VERSION
# added GPIO setup
# added switch IO function to control page switching
# added switch variables, list and frame list

# 1.9 ALPHA VESRION
# Added auto rotation function.
# added next/back page buttons
# made system page not mounted on two seperate frames.
# changed menu titles and arrangment
# added timestamp to refresher
# fixed alerts to change back to neutral if no alerts

# Split off a PC only version
# Version removes the sensor and switch functions
# Adds GUI buttons to navigate between pages

# 2.0 PC ONLY
# Removed Rpi switch related functions. 
# Removed Rpi sensor related functions.
# Rearranged envorment page to have a quick navigation menu
# Added a home button to settings menu to go back to envormental page
# Finished turn_page function.
# Added date and time stamp to updated section on save config

# TO DO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# impliment multiple news source pages that can be stored at one time
# abstract screen resolution into config file and allow for scaling
# settings_menu.py >>> add buttons to change colors and fonts
# health_check.py >>> impliment actual alerting via email or pop-up for critical alerts.
# health_check.py >>> impliment setup script for finding HDD SD and temp sensor
# graphical tweaks all around
# abstract hdd location to config file
# change location not updating in real time
# add email alerts to temp_alert
# f5_news_report needs to route back to github help pages if there is an error.
# f5_storage_report automatically determine drive size. ei if tb or gb should be used
# f7_change_news_list add rubust error catching and compile complete source list to check valid entries against