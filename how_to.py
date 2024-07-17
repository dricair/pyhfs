import pyhfs
import os
import logging
from datetime import datetime, timezone


def how_to(user: str, password: str):
    '''
    Demonstrates how to log in FusionSolar, query plants list and hourly data.
    '''

    try:
        with pyhfs.ClientSession(user=user, password=password) as client:
            plants = client.get_plant_list()
            print('Plants list:\n' + str(plants))

            # Extract list of plant codes
            plants_code = [plant['plantCode'] for plant in plants]

            # Query latest hourly data for all plants
            hourly = client.get_plant_hourly_data(
                plants_code, datetime.now(timezone.utc))
            print('Hourly KPIs:\n' + str(hourly))

    except pyhfs.LoginFailed:
        logging.error(
            'Login failed. Verify user and password of Northbound API account.')
    except pyhfs.FrequencyLimit:
        logging.error('FusionSolar interface access frequency is too high.')
    except pyhfs.Permission:
        logging.error(
            'Missing permission to access FusionSolar Northbound interface.')


if __name__ == '__main__':
    user = os.environ.get('FUSIONSOLAR_USER', None)
    password = os.environ.get('FUSIONSOLAR_PASSWORD', None)
    if user is None or password is None:
        raise Exception("Please set FUSIONSOLAR_USER and FUSION_SOLARPASSWORD to allow login")
    how_to(user=user, password=password)
