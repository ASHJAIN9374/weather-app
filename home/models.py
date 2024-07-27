from django.db import models

# Create your models here.
class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    maxtemp_c = models.FloatField()
    mintemp_c = models.FloatField()

    class Meta:
        unique_together = ('city', 'date')

    def __str__(self):
        return f"{self.city} on {self.date}"
class UserSearch(models.Model):
    username=models.CharField(max_length=300)
    city=models.CharField(max_length=300)
    date = models.DateTimeField()
    class Meta:
        unique_together = ('username', 'city')
