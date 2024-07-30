from django.db import models

class Bank(models.Model):
    bank_code = models.CharField(max_length=10, primary_key=True, default='')
    bank_name = models.CharField(max_length=100, default='')
    legal_address = models.CharField(max_length=255, default='')
    profit = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return self.bank_name

class ATM(models.Model):
    atm_number = models.CharField(max_length=10, primary_key=True, default='')
    address = models.CharField(max_length=255, default='')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.atm_number

class Clients(models.Model):
    card_number = models.CharField(max_length=20, primary_key=True, default='')
    full_name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.full_name

class Operations(models.Model):
    card_number = models.ForeignKey('Clients', on_delete=models.CASCADE, null=True)
    atm_number = models.ForeignKey(ATM, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time = models.TimeField()
    comission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    add_take = models.BooleanField(default=True)

    def __str__(self):
        return self.amount

#