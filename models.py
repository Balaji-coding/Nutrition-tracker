from django.db import models
from datetime import date

# # Create your models here.
# class userinput(models.Model):
#     content =models.TextField()
#     timestamp =models.TextField()

#     def __str__(self):
#         return self.content
class register(models.Model):
    name =models.CharField(max_length=100)
    email =models.EmailField(unique=True, default="default@example.com")
    password =models.CharField(max_length=100)
    unique_id =models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class foodlist(models.Model):
    unique = models.ForeignKey(register, on_delete=models.SET_NULL,null=True)
    date =models.DateField(default=date.today)
    item =models.CharField(max_length=100)
    calories =models.DecimalField(max_digits=10,decimal_places=2,default=0)
    fat=models.DecimalField(max_digits=10,decimal_places=2)
    fat_saturated=models.DecimalField(max_digits=10,decimal_places=2)
    protein=models.DecimalField(max_digits=10,decimal_places=2)
    sodium=models.DecimalField(max_digits=10,decimal_places=2)
    potassium=models.DecimalField(max_digits=10,decimal_places=2)
    cholesterol=models.DecimalField(max_digits=10,decimal_places=2)
    carbohydrates=models.DecimalField(max_digits=10,decimal_places=2)
    fiber=models.DecimalField(max_digits=10,decimal_places=2)
    sugar=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
     return (self.date)
    

class user_details(models.Model):
       email =models.ForeignKey(register,on_delete=models.SET_NULL,null=True,to_field='email')
       weight =models.FloatField()
       height =models.FloatField()
       age =models.PositiveIntegerField()
       gender=models.CharField(max_length=50)
       activity_level =models.CharField(max_length=50)
       goal =models.CharField(max_length=13)
       bmr =models.FloatField()
       tdee =models.FloatField()
       your_calorie_goal =models.FloatField()
       protien_min =models.FloatField()
       protien_max =models.FloatField()
       lower_fat =models.FloatField()
       upper_fat =models.FloatField()
       potassium =models.FloatField()
       fiber =models.CharField(max_length=10)
       suger =models.FloatField()
       


       def __str__(self):
          return self.height

class user_command(models.Model):
    name = models.ForeignKey(register, on_delete=models.SET_NULL, null=True, related_name='user_commands_by_name')
    email = models.ForeignKey(register, on_delete=models.SET_NULL, null=True, related_name='user_commands_by_email')
    command = models.CharField(max_length=300)

    def __str__(self):
        return self.command
    
class WaterIntake(models.Model):
    email =models.EmailField(default="default@example.com")
    date = models.DateField(auto_now_add=True)
    glasses_drank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.email} - {self.date} - {self.glasses_drank} glasses"

