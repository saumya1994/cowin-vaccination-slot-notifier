import os
import time
import requests
import schedule
import datetime
from twilio.rest import Client
from configparser import ConfigParser


base_path = os.path.dirname(os.path.abspath(__file__))
config = ConfigParser()
conf_path = os.path.join(base_path, 'config.ini')
config.read(conf_path)
cowin_args = config['cowin']
twilio_args = config['twilio']

account_sid = str(twilio_args['account_sid'])
auth_token = str(twilio_args['auth_token'])
client = Client(account_sid, auth_token)

message_text_primary = '*Vaccination slot availability notification*\n\n\n'
send_message_flag = False

def get_slot_availability(cowin_args):
    district_id = cowin_args['district_id']
    beneficiary_age = int(cowin_args['beneficiary_age'])

    global send_message_flag
    global message_text_primary

    curr_date = datetime.datetime.today()
    date_list = [curr_date + datetime.timedelta(days=x) for x in range(5)]
    date_str_list = [x.strftime("%d-%m-%Y") for x in date_list]
    for date in date_str_list:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_id, date)
        response = requests.get(URL)
        if response.ok:
            available_centers = response.json()
            num_centers = len(available_centers['centers'][0:])  
            for itr in range(0, num_centers):
                name = available_centers['centers'][itr]['name']
                address = available_centers['centers'][itr]['address']
                sessions = available_centers['centers'][itr]['sessions']
                for itr, session in enumerate(sessions):
                    session_num = str(itr)
                    date = session['date']
                    available_capacity = session['available_capacity']
                    min_age_limit = session['min_age_limit']
                    vaccine = session['vaccine']
                    slots = str(session['slots'])
                    if available_capacity > 0 and beneficiary_age >= min_age_limit:
                        center_info = 'Vaccination slot available in *{}*\n\nAddress: {}\n\nDate: {}\n\nAvailable capacity: {}\n\nVaccine: {}\n\nSlots: {}'.format(name, address, date, str(available_capacity), vaccine, slots)
                        message_text_primary = message_text_primary + '\n\n\n\n' + center_info
                        send_message_flag = True
    else:
        print('[INFO] No vaccination slot found')
        send_message_flag = False

    return send_message_flag, message_text_primary


def send_whatsapp_message(twilio_args, message_text):
    twilio_number = twilio_args['twilio_number']
    personal_number = twilio_args['personal_number']
    message = client.messages.create( 
                        from_ = twilio_number,  
                        body = message_text,
                        to = personal_number
                    )

def main(cowin_args, twilio_args):
    print('[INFO] Checking for vaccination slot availability')
    send_message_flag, message_text = get_slot_availability(cowin_args)
    message_text_length = len(message_text)
    latest_api_call = datetime.datetime.now()
    if send_message_flag == True:
        if message_text_length <= 1600:
            print('[INFO] Triggering WhatsApp message')
            send_whatsapp_message(twilio_args, message_text)
            print('[INFO] Vaccination slot availability notification sent on WhatsApp number')
        elif message_text_length > 1600:
            total_splits = message_text_length//1600
            for itr in range(0, total_splits):
                from_chr = 1600 * itr
                to_chr = from_chr + 1600
                message_split = message_text[from_chr:to_chr]
                print('[INFO] Triggering WhatsApp message')
                send_whatsapp_message(twilio_args, message_split)
                print('[INFO] Vaccination slot availability notification sent on WhatsApp number')
    print('[INFO] Latest API call was made on {}'.format(latest_api_call))
    

if __name__=='__main__':
    send_whatsapp_message(twilio_args, 'You have been subscribed to vaccination slot availability notification service. You will receive a notification when a slot opens up in a center near you. Reply stop if you want to stop this notification service.')
    main(cowin_args, twilio_args)
    schedule.every(1).minutes.do(main, cowin_args, twilio_args)
    while 1:
        schedule.run_pending()
        time.sleep(1)
    