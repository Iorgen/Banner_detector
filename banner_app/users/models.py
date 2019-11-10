# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default=' ')
    second_name = models.CharField(max_length=50, default=' ')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return "Пользователь: %s %s" % (self.second_name, self.first_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
