from django.db import models

class csvdata(models.Model):
    data_id = models.CharField(max_length=500,default="")
    name=models.CharField(max_length=500,default="")
    domain = models.CharField(max_length=500,default="")
    year_founded = models.IntegerField(default=0)
    industry = models.CharField(max_length=500,default="")
    size_range = models.CharField(max_length=500,default="")
    country = models.CharField(max_length=500,default="")
    linkdin_url = models.CharField(max_length=500,default="")
    current_employee_estimate = models.IntegerField(default=0)
    total_employee_estimate = models.IntegerField(default=0)
    city = models.CharField(max_length=500,default="")
    state = models.CharField(max_length=500,default="")

    def __str__(self) -> str:
        return self.name
    