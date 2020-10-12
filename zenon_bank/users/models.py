from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #for department
    Computer_Engineer = 'CPE'
    Electrical_Engineer = "EE"
    Mechanical_Engineer = "MECH"

    #for gender
    Male = "Male"
    Female= "Female"
    


    department = models.CharField(
        max_length=4,
        choices=[
            (Computer_Engineer, "Computer Engineer"),
            (Electrical_Engineer, "Electrical Engineer"),
            (Mechanical_Engineer, "Mechanical Engineer"),
        ],   
        default=Computer_Engineer,
    )  

    phone_number = models.CharField(max_length=10)
    
    gender = models.CharField(
        max_length=6,
        choices=[
            (Male, "Male"),
            (Female, "Female")
        ],
        default= Male
    )

    biography= models.TextField()

    def __str__(self):
        return f"username: {self.user.username}, phone_number={self.phone_number}"




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default="default.png", upload_to="profile_images")


    def __str__(self):
        return str(self.user.username) + " Profile"
    
"""
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.profile_img.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_img.path)

"""




    






