# Pesc-api

Simple python module which provide access to data from [ikus.pesc.ru](https://ikus.pesc.ru/).
Before you use the wrapper you need to register on the [site](https://ikus.pesc.ru/login).

## Authentication

```python
>>> from pesc import PescClient
>>> client = PescClient()
>>> client.auth('sa@prg.re', 'xxx-xxx-xxx-xxx')
{'authenticationSuccess': True}
```

## Accounts

```python
>>> accounts = client.accounts
>>> account = accounts[0]
```

### Bills

```python
>>> bills = account.get_bills(date_from='30.12.2010', date_to='01.01.2016')
>>> bills[0]
{'billId': 130098827, 'period': '01-01-2016', 'billNumber': 52, 'sum': 0.31}
```

### Payments

```python
>>> payments = accounts[0].get_payments(date_from='01.01.2018', date_to='30.05.2018')
>>> payments[0]
{'date': '09-01-2018', 'sum': 1020.74, 'type': 'Счет', 'charge': 1020.74, 'fine': 0.0, 'period': '01-01-2018', 'checkExists': True, 'status': 'DONE'}
```

## Meters

```python
>>> meters = accounts[0].meters
>>> meter = meters[0]
>>> meter.info
{'meterId': 4512623, 'meterNumber': '031296508', 'meterModel': 'ЦЭ2726-12', 'installationDate': '06-06-2011', 'installationPlace': 'КВАРТИРА', 'owner': 'Абонент', 'precision': '1,0', 'voltage': '220', 'current': '5-60', 'calibrationInterval': None, 'tarifficationPlan': 'Двухтарифный', 'relationType': {'relationTypeText': 'Индивидуальный', 'relationTypeCode': 'INDIVIDUAL'}, 'meterState': {'meterStateText': 'Исправный', 'meterStateCode': 'WORKING'}, 'meterType': {'meterTypeText': 'Обычный ПУ', 'meterTypeCode': 'REGULAR'}, 'accountStatus': None, 'numberOfDigitsInScale': 6, 'numberOfScales': 2, 'scales': ['DAY', 'NIGHT']}
```

### Indications

Get indications

```python
>>> indications = meter.get_indications(date_from='01.01.2018', date_to='30.05.2018')
>>> indications[0]
{'type': 'Заявленные показания', 'date': '22-09-2018', 'scaleValues': [{'scale': 'DAY', 'value': 14867}, {'scale': 'NIGHT', 'value': 7092}]}
```

Post indication

```python
>>> meter.post_indication(day=105, night=10)
```