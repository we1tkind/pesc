# -*- coding: utf-8 -*-
"""
pesc.client

"""

import json
from datetime import datetime
import requests

ROOT_URL = 'https://ikus.pesc.ru'


class PescObject:
    """
    This is base class.

    """
    def __init__(self, session=requests.Session()):
        self.session = session


class PescMeter(PescObject):
    """
    This class for electric meter.

    """
    def __init__(self, session, account_id, provider, service_type,
                 meter_id, meter_number):
        super().__init__(session=session)
        self.account_id = account_id
        self.provider = provider
        self.service_type = service_type
        self.api_url = ROOT_URL + '/application/accounts'
        self.meter_id = meter_id
        self.meter_number = meter_number

    @property
    def info(self):
        url = '/'.join((self.api_url, self.provider,
                        'meters', str(self.meter_id)))
        headers = {'content-type': 'application/json; charset=utf-8'}
        response = self.session.get(url, headers=headers)
        return response.json()

    def get_indications(self, date_from=datetime.now().strftime('01-01-%Y'),
                        date_to=datetime.now().strftime('%d-%m-%Y')):
        url = '/'.join((self.api_url, self.provider, 'indications'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'meterId': self.meter_id,
                'dateFrom': date_from,
                'dateTo': date_to}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    def post_indication(self, day=0, night=0):
        url = '/'.join((self.api_url, self.provider, 'indication/new'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'account': {'accountNumber': self.account_id},
                'serviceType': self.service_type,
                'meterId': self.meter_id,
                'indication': [{'scale': "DAY", 'value': day},
                               {'scale': "NIGHT", 'value': night}]
                }
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    def __repr__(self):
        return 'Meter {} from account {}'.format(self.meter_number,
                                                 self.account_id)


class PescAccount(PescObject):
    """
    This is class for consumer account.

    """
    def __init__(self, session, account_id, provider_name, service_type):
        super().__init__(session=session)
        self.api_url = ROOT_URL + '/application/accounts'
        self.account_id = account_id
        self.provider = provider_name
        self.service_type = service_type

    def get_bills(self, date_from=datetime.now().strftime('01-01-%Y'),
                  date_to=datetime.now().strftime('%d-%m-%Y')):
        url = '/'.join((self.api_url, self.provider, 'bills'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'dateFrom': date_from, 'dateTo': date_to,
                'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    def get_payments(self, date_from=datetime.now().strftime('01-01-%Y'),
                     date_to=datetime.now().strftime('%d-%m-%Y')):
        url = '/'.join((self.api_url, self.provider, 'payments'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'account': {'accountNumber': self.account_id},
                'period': {'dateFrom': date_from, 'dateTo': date_to},
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    def get_meters(self):
        url = '/'.join((self.api_url, self.provider, 'meters'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return [PescMeter(self.session, self.account_id,
                          self.provider, self.service_type,
                          meter['meterId'], meter['meterNumber'])
                for meter in response.json()]

    @property
    def meters(self):
        return self.get_meters()

    @property
    def status(self):
        url = '/'.join((self.api_url, self.provider, 'status'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    @property
    def debt(self):
        url = '/'.join((self.api_url, self.provider, 'debt'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    @property
    def active_payments(self):
        url = '/'.join((self.api_url, self.provider, 'activePayments'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()

    @property
    def address(self):
        url = '/'.join((self.api_url, self.provider, 'address'))
        headers = {'content-type': 'application/json; charset=utf-8'}
        data = {'accountNumber': self.account_id,
                'serviceType': self.service_type}
        response = self.session.post(url, data=json.dumps(data),
                                     headers=headers)
        return response.json()['address']

    def __repr__(self):
        return 'Account {} at {}'.format(self.account_id, self.address)


class PescClient(PescObject):
    """
    This is class for access data.

    """
    def __init__(self, session_path=None):
        super().__init__()
        self.api_url = ROOT_URL + '/application'
        self.username = None
        self.password = None

    def auth(self, username, password):
        """
        Authentication function.

        Parameters
        __________
        username: str
            username
        password: str
            password

        Returns
        _______
        dict
            {'authenticationSuccess': True} or
            {'errors': [{'code': 3, 'message': 'Неверный пароль'}]}
        """
        self.username = username
        self.password = password
        url = self.api_url + '/authentication'
        data = {'username': username,
                'password': password}
        response = self.session.post(url, data=data)
        return response.json()

    def check_auth(self):
        """
        Function for checking auth info.

        Returns
        _______
        dict
            {'email': 'null@prg.re', 'emailConfirmed': True, 'phoneConfirmed': True,
             'superUserMode': False, 'guideViewed': True, 'phoneExists': True,
             'hasPersonalInfo': True} or
            {'errors': [{'code': 5, 'message': 'Неавторизованный доступ'}]}
        """
        url = self.api_url + '/checkAuthentication'
        response = self.session.get(url)
        return response.json()

    def get_accounts(self):
        url = self.api_url + '/accounts'
        response = self.session.get(url)
        return [PescAccount(self.session,
                            account['accountNumber'],
                            account['providerName'],
                            account['serviceName'])
                for account in response.json()['ELECTRICITY']]

    @property
    def accounts(self):
        return self.get_accounts()

    @property
    def notifications(self):
        url = self.api_url + '/notifications'
        response = self.session.get(url)
        try:
            notifications = response.json()
        except json.decoder.JSONDecodeError:
            notifications = response.text
        return notifications

    def logout(self):
        """
        Function for logout.

        Return
        ______
        dict
            {'logoutSuccess': True}
        """
        url = self.api_url + '/logout'
        response = self.session.get(url)
        return response.json()
