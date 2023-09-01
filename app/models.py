from django.db import models

class csvdata(models.Model):
    data_id = models.CharField(max_length=500,default="")
    name=models.CharField(max_length=150,default="")
    domain = models.CharField(max_length=200,default="")
    year_founded = models.IntegerField(default=0,db_index=True)
    industry = models.CharField(max_length=100,default="")
    size_range = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    linkdin_url = models.CharField(max_length=200,default="")
    current_employee_estimate = models.IntegerField(default=0)
    total_employee_estimate = models.IntegerField(default=0)
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,default="")
    
    class Meta:
        indexes = [models.Index(fields=['name','year_founded','industry','country','city','state'])]

    def __str__(self) -> str:
        return self.name