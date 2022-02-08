import json

import requests


def get_payments_info(oktmmf, ifns):
    data = {
        'c': 'next',
        'step': 1,
        'npKind': 'fl',
        'ifns': ifns,
        'oktmmf': oktmmf,
    }
    url = 'https://service.nalog.ru/addrno-proc.json'
    response = requests.post(url, data=data)
    if response.status_code == requests.codes['ok'] and response.text:
        payment_data = json.loads(response.text)['payeeDetails']
        result_data = {
            'Получатель платежа': payment_data['payeeName'],
            'ИНН получателя': payment_data['payeeInn'],
            'КПП получателя': payment_data['payeeKpp'],
            'Банк получателя': payment_data['bankName'],
            'БИК': payment_data['bankBic'],
            'Корр. счет №': payment_data['correspAcc'],
            'Счет №': payment_data['payeeAcc'],
        }
        return result_data
    else:
        raise Exception(f'Response status: {response.status_code}, body: {response.text}')


if __name__ == '__main__':
    # Берем нужные значения ОКТМО и ИФНС
    oktmmf = 40913000
    ifns = 7840
    # Записываем нужный нам словарь
    result = get_payments_info(oktmmf, ifns)
    print(result)
