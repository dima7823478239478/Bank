from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BankForm, ATMForm, ClientsForm, OperationsForm
from .models import Bank, ATM, Clients, Operations
from decimal import Decimal


def index_page(request):
    return render(request, 'index.html')

class BankListView(ListView):
    model = Bank
    template_name = 'bank_list.html'
    context_object_name = 'banks'




class BankDetailView(DetailView):
    model = Bank
    template_name = 'bank_detail.html'
    context_object_name = 'bank'
    slug_field = 'bank_code'
    slug_url_kwarg = 'bank_code'



class ATMListView(ListView):
    model = ATM
    template_name = 'atm_list.html'
    context_object_name = 'atms'

class ATMDetailView(DetailView):
    model = ATM
    template_name = 'atm_detail.html'
    context_object_name = 'atm'
    slug_field = 'atm_number'
    slug_url_kwarg = 'atm_number'

class ClientListView(ListView):
    model = Clients
    template_name = 'client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Clients
    template_name = 'client_detail.html'
    context_object_name = 'client'
    slug_field = 'card_number'
    slug_url_kwarg = 'card_number'

class OperationListView(ListView):
    model = Operations
    template_name = 'operation_list.html'
    context_object_name = 'operations'

class OperationDetailView(DetailView):
    model = Operations
    template_name = 'operation_detail.html'
    context_object_name = 'operation'
    pk_url_kwarg = 'operation_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operation = self.get_object()
        context['client'] = operation.card_number  # Передаем экземпляр клиента в контекст
        return context





def create_bank(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_list')
    else:
        form = BankForm()
    return render(request, 'bank_form.html', {'form': form})

def edit_bank(request, bank_code):
    bank = Bank.objects.get(bank_code=bank_code)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            return redirect('bank_list')
    else:
        form = BankForm(instance=bank)
    return render(request, 'bank_form.html', {'form': form})

def delete_bank(request, bank_code):
    bank = Bank.objects.get(bank_code=bank_code)
    bank.delete()
    return redirect('bank_list')




def create_atm(request):
    if request.method == 'POST':
        form = ATMForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atm_list')
    else:
        form = ATMForm()
    return render(request, 'atm_form.html', {'form': form})

def edit_atm(request, atm_number):
    atm = ATM.objects.get(atm_number=atm_number)
    if request.method == 'POST':
        form = ATMForm(request.POST, instance=atm)
        if form.is_valid():
            form.save()
            return redirect('atm_list')
    else:
        form = ATMForm(instance=atm)
    return render(request, 'atm_form.html', {'form': form})

def delete_atm(request, atm_number):
    atm = ATM.objects.get(atm_number=atm_number)
    atm.delete()
    return redirect('atm_list')

def create_client(request):
    if request.method == 'POST':
        form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientsForm()
    return render(request, 'client_form.html', {'form': form})

def edit_client(request, card_number):
    client = Clients.objects.get(card_number=card_number)
    if request.method == 'POST':
        form = ClientsForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientsForm(instance=client)
    return render(request, 'client_form.html', {'form': form})

def delete_client(request, card_number):
    client = Clients.objects.get(card_number=card_number)
    client.delete()
    return redirect('client_list')


def create_operation(request):
    if request.method == 'POST':
        form = OperationsForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            client = operation.card_number
            atm_bank = operation.atm_number.bank
            client_bank = client.bank
            commission_amount = Decimal('0')

            if client_bank != atm_bank:
                commission_amount = operation.amount * Decimal('0.12')

            if operation.add_take and client.account < (operation.amount + commission_amount):
                messages.error(request, 'Недостаточно средств на счете для снятия денег с учетом комиссии.')
                return render(request, 'operation_form.html', {'form': form})

            if operation.add_take:
                client.account -= (operation.amount + commission_amount)
            else:
                client.account += operation.amount

            client.save()

            if commission_amount > 0:
                operation.comission = commission_amount
                atm_bank.profit += commission_amount
                atm_bank.save()

            operation.save()
            return redirect('operation_list')
    else:
        form = OperationsForm()
    return render(request, 'operation_form.html', {'form': form})

def edit_operation(request, operation_id):
    operation = Operations.objects.get(id=operation_id)
    old_operation = Operations.objects.get(id=operation_id)
    client = old_operation.card_number
    atm_bank = old_operation.atm_number.bank
    old_commission = old_operation.comission

    if request.method == 'POST':
        form = OperationsForm(request.POST, instance=operation)
        if form.is_valid():
            # Восстанавливаем старое значение на счете клиента и банке
            if old_operation.add_take:
                client.account += old_operation.amount
                if old_commission > 0:
                    client.account += old_commission
                    atm_bank.profit -= old_commission
                    atm_bank.save()
            else:
                client.account -= old_operation.amount
                if old_commission > 0:
                    client.account += old_commission
                    atm_bank.profit -= old_commission
                    atm_bank.save()

            operation = form.save(commit=False)
            commission_amount = Decimal('0')

            if operation.card_number.bank != operation.atm_number.bank:
                # Рассчитываем комиссию
                commission_amount = operation.amount * Decimal('0.12')

            # Проверка, достаточно ли средств на счете для снятия денег, включая комиссию
            if operation.add_take and client.account < (operation.amount + commission_amount):
                messages.error(request, 'Недостаточно средств на счете для снятия денег с учетом комиссии.')
                return render(request, 'operation_form.html', {'form': form})

            # Обновляем счет клиента в зависимости от add_take
            if operation.add_take:
                client.account -= (operation.amount + commission_amount)
            else:
                client.account += operation.amount


            client.save()  # Сохраняем изменения в клиенте

            if commission_amount > 0:
                operation.comission = commission_amount
                atm_bank.profit += commission_amount  # Добавляем комиссию к прибыли банка
                atm_bank.save()

            operation.save()  # Сохраняем операцию
            return redirect('operation_list')
    else:
        form = OperationsForm(instance=operation)

    return render(request, 'operation_form.html', {'form': form})

def delete_operation(request, operation_id):
    operation = Operations.objects.get(id=operation_id)
    client = operation.card_number
    atm_bank = operation.atm_number.bank
    commission_amount = operation.comission

    # Восстанавливаем значение на счете клиента перед удалением операции
    if operation.add_take:
        client.account += operation.amount
        if commission_amount > 0:
            client.account += commission_amount
            atm_bank.profit -= commission_amount
            atm_bank.save()
    else:
        client.account -= operation.amount
        if commission_amount > 0:
            client.account += commission_amount
            atm_bank.profit -= commission_amount
            atm_bank.save()

    client.save()  # Сохраняем изменения в клиенте
    operation.delete()  # Удаляем операцию
    return redirect('operation_list')