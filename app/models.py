from django.db import models

class Tasks(models.Model):
	created_date=models.DateTimeField(auto_now=True)
	username=models.CharField(max_length=191, null=True, blank=True)
	task=models.CharField(max_length=191, null=True, blank=True)
	completed=models.CharField(max_length=2, default='0')
	class Meta:
		db_table="Tasks"