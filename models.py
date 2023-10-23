import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Shuttle(models.Model):
    """Model representing a Shuttle."""

    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    color = models.CharField(max_length=100)

    class Meta:
        ordering = ['capacity', 'color']

    def get_absolute_url(self):
        """Returns the URL to access a particular shuttle instance."""
        return reverse('shuttle_detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class ShuttleSchedule(models.Model):
    """Model representing a Shuttle_schedule."""

    schedule_time = models.TimeField()
    schedule_date = models.DateField()
    shuttle_id = models.ForeignKey('Shuttle', on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = ['schedule_date', 'schedule_time']

    def get_absolute_url(self):
        """Returns the URL to access a particular shuttle schedule instance."""
        return reverse('ShuttleSchedule', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}'


class Ticket(models.Model):
    """Model representing a Shuttle_schedule."""
    # // customer_id, purchased_date, payment_status, shuttle_schedule_id
    ticket_number = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     help_text='Unique ID for this particular ticket purchased')
    purchased_date = models.DateField()
    shuttle_schedule_id = models.ForeignKey('ShuttleSchedule', on_delete=models.RESTRICT, null=True)
    payment_status = models.CharField(max_length=25)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['purchased_date', 'payment_status']

    def get_absolute_url(self):
        """Returns the URL to access a particular shuttle schedule instance."""
        return reverse('Ticket', args=[str(self.ticket_number)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.ticket_number}'


class PaymentDetails(models.Model):
    """Model representing a PaymentStatus."""

    PAID = 'PAID'
    CANCELED = 'CANCELED'
    PENDING = 'PENDING'
    NO_STATUS = 'NO_STATUS'
    PAYMENT_STATUS_OPTIONS = (
        (PAID, 'Paid'),
        (CANCELED, 'Cancelled'),
        (PENDING, 'Pending'),
        (NO_STATUS, 'No_status'),
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_OPTIONS,
        default=NO_STATUS,
    )

    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                      help_text='Unique ID for this particular transaction')
    payment_method = models.CharField(max_length=100)
    amount = models.IntegerField()
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['payment_status', 'payment_method', 'amount']

    def get_absolute_url(self):
        """Returns the URL to access a particular shuttle instance."""
        return reverse('shuttle_detail', args=[str(self.transaction_id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.transaction_id}'