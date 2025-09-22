from django.db import models
from django.utils import timezone
from user.models import Profile

class Intensity(models.Model):
    id = models.AutoField(primary_key=True)
    intensity = models.CharField(max_length=10)
    description = models.CharField(max_length=30)
    def __str__(self):
        return self.intensity

exercise_types = [
    ('Cardio', 'Cardio'),
    ('Calisthenics', 'Calisthenics')
]

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    exercise = models.CharField(max_length=30)
    type = models.TextField(choices=exercise_types, default='Cardio')
    def __str__(self):
        return self.exercise
    
class PhisicalActivity(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    time = models.IntegerField()
    type = models.TextField(choices=exercise_types, default='Cardio')
    intensity = models.ForeignKey(Intensity,on_delete=models.CASCADE)
    def __str__(self):
        return f"Activity({self.id})"
    
class Diet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    need_cal = models.IntegerField()
    eaten_cal = models.IntegerField()
    def __str__(self):
        return f"Diet({self.id})"
    
class Cali(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    series = models.IntegerField()
    rep = models.IntegerField()
    extra = models.IntegerField()
    def __str__(self):
        return f"Cali({self.id})"
    
class Cardio(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.IntegerField(null= True, blank =True)
    def __str__(self):
        return f"Cardio({self.id})"
    
class Body(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    waist = models.DecimalField(max_digits=10, decimal_places=2)
    bicept = models.DecimalField(max_digits=10, decimal_places=2)
    leg = models.DecimalField(max_digits=10, decimal_places=2)
    BMI = models.DecimalField(max_digits=10, decimal_places=2)
    muscle_mass = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    fat_mass = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    body_water = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    visceral_fat = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    metabolic_age = models.IntegerField(default = 0)

    def __str__(self):
        return f"Body({self.id})"
    

class Maximals(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    entry_date = models.DateTimeField(default=timezone.now)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    max = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Cardio({self.id})"