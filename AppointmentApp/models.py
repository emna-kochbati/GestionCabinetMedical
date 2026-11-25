from django.db import models
from django.core.validators import FileExtensionValidator  
from django.core.exceptions import ValidationError          
from django.utils import timezone                           
# Create your models here.
class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

class Appointment(models.Model):
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reason = models.TextField()
    duration_minute = models.IntegerField(default=30)      
    appointement_date = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    prescription = models.FileField(upload_to='prescriptions/', blank=True, validators=[FileExtensionValidator(['pdf'])])   # ←
    doctor = models.ForeignKey('AccountApp.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('AccountApp.Patient', on_delete=models.CASCADE)

    class Meta:                                             
        ordering = ['appointement_date']
        constraints = [models.UniqueConstraint(fields=['doctor', 'appointement_date'], name='unique_doctor_date')]

    def clean(self):                                       
        if self.pk and Appointment.objects.get(pk=self.pk).appointement_date == self.appointement_date: return
        if self.appointement_date <= timezone.now(): raise ValidationError("La date doit être dans le futur")