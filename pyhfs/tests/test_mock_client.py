import unittest
import datetime

from pyhfs.tests.mock_session import MockSession
import pyhfs


class TestMockClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = pyhfs.Client(MockSession())

    def test(self):
        now = datetime.datetime.now()

        # All plants
        plants_raw = self.client.get_plant_list()

        # List of plant codes
        plants_code = [plant['plantCode'] for plant in plants_raw]

        # Realtime KPIs (with fake station)
        realtime = self.client.get_plant_realtime_data(
            plants_code + ['UnknownStationCode'])
        self.assertGreaterEqual(len(plants_code), len(realtime))

        # Hourly data
        self.client.get_plant_hourly_data(plants_code, now)

        # Daily data
        self.client.get_plant_daily_data(plants_code, now)

        # Monthly data
        self.client.get_plant_monthly_data(plants_code, now)

        # Yearly data
        self.client.get_plant_yearly_data(plants_code, now)

        # Alarms
        self.client.get_alarms_list(plants_code, datetime.datetime(2000, 1, 1), now)


if __name__ == '__main__':
    unittest.main()
