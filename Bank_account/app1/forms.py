from django import forms
from .models import Bank, ATM, Clients, Operations

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = '__all__'
        labels = {
            'bank_code': 'Код банка',
            'bank_name': 'Название банка',
            'legal_address': 'Адрес банка'


        }
class ATMForm(forms.ModelForm):
    class Meta:
        model = ATM
        fields = '__all__'
        labels = {
            'atm_number': 'Номер банкомата',
            'address': 'Адрес банкомата',
            'bank': 'Номер банка'


        }

class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        labels = {
            'card_number': 'Номер карты',
            'full_name': 'ФИО',
            'address': 'Адрес проживания',
            'bank':'Номер банка',
            'account':'Счет'


        }

class OperationsForm(forms.ModelForm):
    class Meta:
        model = Operations
        fields = '__all__'
        exclude = ['comission']
        labels = {
            'card_number': 'ФИО клиента',
            'atm_number': 'Номер банкомата',
            'date': 'Дата (Формата: Год-Месяц-Число)',
            'time': 'Время (Формата: Часы-Минуты-Секунды)',
            'comission': 'Комиссия',
            'amount':'Сумма',
            'add_take':'Снять деньги',


        }