from django.db import models
import re

class UserManager(models.Manager):
    def reg_validator(self, post_data):
        errors = {}
        if len(post_data["fname"]) < 2:
            errors['fname'] = "First Name must be at least 2 character!"
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last Name must be at least 2 character!"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = "Passwords do not match!"
        return errors
        
    def login_validator(self, post_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        if len(post_data['password']) < 8:
            errors['password'] = "Email or Password is incorrect please try again!"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=23)
    lname = models.CharField(max_length=23)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # fav_recipe = specific recipe user selected to save
    # user_recents = list of recipes user has visited
