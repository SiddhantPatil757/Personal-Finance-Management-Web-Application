from django.db import models


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'income'
        managed = False

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Fuel', 'Fuel'),
        ('Rent', 'Rent'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Healthcare', 'Healthcare'),
        ('Entertainment', 'Entertainment'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
        ('Wallet', 'Wallet'),
    ]

    id = models.AutoField(primary_key=True)
    date = models.DateField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'expenses'
        managed = False

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Saving(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'savings'
        managed = False

    def __str__(self):
        return f"Saving - {self.amount}"


class Budget(models.Model):

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Fuel', 'Fuel'),
        ('Rent', 'Rent'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Healthcare', 'Healthcare'),
        ('Entertainment', 'Entertainment'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=7)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'budget'
        managed = False

    def __str__(self):
        return f"{self.category} - {self.month}"


class Goal(models.Model):
    id = models.AutoField(primary_key=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'goal'
        managed = False

    def __str__(self):
        return f"Goal - {self.target_amount}"