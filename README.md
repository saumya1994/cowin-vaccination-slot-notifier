# Vaccination Slot Availability Notification Service

## Overview of this project
India has been facing multiple challanges amid second wave of COVID-19. This project is intended to help fellow citizens of India on finding a vaccination slot at the earliest.

If you are from India and struggling to find a vaccination slot, worry not and use this project to your benefit. WhatsApp is in our daily life. So why not use it for our benefit in finding a vaccination slot? Follow along and setup a WhatsApp notification service to get notified on the vaccination slot availability in your area at the earliest.
</br></br>

## Dependencies

### Python packages
1. twilio
2. scheduler
3. configparser

### Third-party accounts
1. Twilio
2. Heroku (optional)
</br></br>

## Usage


### **Basic Setup**
Step 1. Fork/clone this project </br>
Step 2. Head over to [DISTRICTS LOOKUP](DISTRICT-LOOKUP.md) file and find out district id of your district (You know how to use command/ctrl + F) </br>
Step 4. Head over to [config](config.ini) file and update **district_id** and **beneficiary_age** in the [cowin] section </br></br>

### **WhatsApp notification service setup**
Step 1. Sign up for a twilio account using this [link](www.twilio.com/referral/3HiRr6) </br>
Step 2. Head over to *Programmable Messaging > Try it Out > Try Whatsapp* on Twilio. Save your twilio contact number on phone and send join code *(In my case, it is **join sheet-uncle**)* as a WhatsApp message to your number. You have now setup a WhatsApp sandbox. 
</br>
![](./screenshots/twilio_whatsapp_sandbox.png)</br>
Step 3. Head over to Console Dashboard on Twilio. Copy **ACCOUNT SID** and **AUTH TOKEN** and paste it in the [twilio] section of the [config](config.ini) file. Also, update the twilio number and your personal WhatsApp number in the same section of the config file.

### **Run it**

### Running the project locally </br>
Step 1. Install the packages mentioned in requirements.txt file with *pip* </br>
Step 2. Run the python file *vaccination_slot_notifier.py* </br>
Keep it running in the backbround

Command line users can run the following commands
```
$ pip install -r requirements.txt
$ python vaccination_slot_notifier.py
```


However, running this project locally is not a great idea. Deploy and run it in Heroku to keep the notification service up at all times.

### Heroku deployment (optional) </br>
Step 1. Sign up for a Heroku account [here](https://signup.heroku.com/login) </br>
Step 2. Click on **Create New App** and choose a simple name for the deployment *(In my case it is **vaccine-slot-notifier**. You can have give any name other than this)*. Click on **create app** </br>
![](./screenshots/heroku_project.png)
Step 3. In the deployment method, click on **Connect to GitHub** > search for the repository name from GitHub and click on **connect** that is against the repository name of this project. Scroll down to the bottom once you connect and click on **Enable Automatic Deploys** and click on **Deploy Branch** </br>
![](./screenshots/heroku_deployment.png)

Project is now deployed on Heroku. One final step is to start execution of the program in Heroku Dyno.

Head over to **Resources** > Click on **Edit dyno formation** > Toggle the swith that is against the program and **click confirm** </br>
![](./screenshots/heroku_run.png)

Program will now remain active at all times in Heroku Dyno. You should be receiving notification service status on WhatsApp status.

You will be notified when vaccination slot is available in your area. Booking the slot and taking a jab is on you!

## License
The source code used to format and display the content of this project is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
