from django.db import models

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)  # Explicitly declare the primary key
    wallet_id = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    transaction_currency = models.CharField(max_length=50)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_timestamp = models.DateTimeField()
    transaction_status = models.CharField(max_length=50)
    user_phone_number = models.CharField(max_length=20)
    sender_mobile_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'transaction_table'
        managed = False
