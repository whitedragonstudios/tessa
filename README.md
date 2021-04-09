# tessa
The Exchange Server Smart Assistant 
TESSA is an all in one home server and smart asistant solution. It intergrates Samba Server, Pi-Hole, Google Assistant, and various web api's to deliver to you all the information you need to start your day. Because most of those programs are not my code they will not be featured here. What is featured here is a GUI that displays weather, news, system status, and sensor data to the user. The Tessa hardware consists of a Raspberry Pi 4, external harddrive, 12 position switch, lcd touchscreen, and BME 680 sensor. 
For testing purposes if you would like to use the tessa program without the physcial hardware please see "MAKE IT WORK" 




MAKE IT WORK
1) The core of tessa's functions draw on a config file which (for now) you will need to download. Eventually I will be publishing a setup script that will guide users through the setup process. Which will create the config file for you. Since that isn't implimented you will need to download "default_tessa_config.json". Once downloaded rename it to "tessa_config.json" and place it in a directory "~/TESSA/config/". You can modify this path on line 700. 
2) If you do not have a BME 680 sensor you can change lines 184-188: "bme_temp = 80", "bme_humidity =  30", "bme_pressure = 1019", "bme_altitude = 100", "raw_gas = 108042.0". This will give the sensor output static values but will not interfer with any other functions. Comment out the origonal code if you intend to attach a sensor at some point.
3) If you do not have a 12 position swtich attached you will need to manually set the switch position [sw07= "HIGH"] on line 714. Then comment out line 968 the "Switch_I/O" function call. This will perminately enable the next and back buttons on each page. You can then use those to navigate between pages.
4) In the def f6_storage_report(): fuction, on line 407 you will need to modify "hdd = [path to a hdd on your computer]"
5) In the def sys_report(): function on line 114 you will need to modify "temp_cpu = psutil.sensors_temperatures()['cpu_thermal'][0][1]" to point to a sensor location on your computer. See psutil documentation to help find its address. Alternativly you could just change it to a int or float number that will remain static.
6) Tessa uses two web api's (openweathermap.org and newsapi.org) to deliver data to the user. If you would like the program to work you will to get api keys from these websites. They are free and super easy to sign up for. You can manully add those to the tessa_config.json file or via buttons on the settings page, "Change Weather Key", "Change News Key".
Once these changes have been made you should get full functionallity out of tessa without the hardware its designed to use. PLEASE comment if you encounter other hardward com errors. 
