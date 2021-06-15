from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        #Length of first_name
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters long'

        #length of last_name
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name bust be at least 2 characters long'

        #Email matches format
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = 'You must enter an email'
        elif not email_regex.match(postData['email']):
            errors['email'] = 'Must be a valid email'

        #Email Unique
        current_users = User.objects.filter(email = postData['email'])
        if len(current_users) > 0:
            errors['dupilcate'] = 'That email is already in use'

        #password was entered
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'

        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = 'Your passwords do not match'
        return errors

    def login_validator(self,postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        # email has been entered
        if len(postData['email']) == 0:
            errors['email'] = 'Email must be entered'
        #password has been entered
        if len(postData['password']) < 8:
            errors['password'] = 'An 8 character password must be entered'
        # email and password match
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = 'Email and password do not match'
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    objects = UserManager()

class ConManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #postData == request.POST
        if len(postData['destination']) < 2:
            errors['destination'] = 'Title must be at least 2 characters long'
        if len(postData['plan'] )< 10:
            errors['plan'] = 'Plan must be at least 10 characters long'
        return errors

# Create your models here.
class Con(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ConManager()