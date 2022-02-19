from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters."
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters."
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm']:
            errors['mismatch'] = "Your passwords do not match"
        return errors

    def log_val(self, postData):
        errors = {}
        current_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Please Enter Email"
        if len(postData['password']) < 8:
            errors['password'] = "Add at least 8 or more characters"
        elif bcrypt.checkpw(postData['password'].encode(), current_user[0].password.encode()) != True:
            errors['password'] = "Email and Password do not match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()



class ShowManger(models.Manager):
    def show_val(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must be at least 3 characters."
        if len(postData['network']) < 3:
            errors['network'] = "Network must be at least 3 characters."
        if len(postData['description']) < 3:
            errors['description'] = "Description must be at least 3 characters."
        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='shows', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManger()