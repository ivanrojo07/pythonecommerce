from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager
)

class UserManager(BaseUserManager):
	def create_user(self,email,password=None,is_active=True, is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user_obj = self.create_user(
			email,
			password=password,
			is_staff=True
		)
		return user_obj

	def create_superuser(self, email, password=None):
		user_obj = self.create_user(
			email,
			password=password,
			is_staff=True,
			is_admin=True
		)
		return user_obj

# Create your models here.

class User(AbstractBaseUser):
	email = models.EmailField(max_length=255,unique=True)
	active = models.BooleanField(default=True)#can login
	staff = models.BooleanField(default=False)#staff user non superuser
	admin = models.BooleanField(default=False)#superuser
	timestamp = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'email' #username
	# REQUIRED_FIELDS = ['email','password']

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email
	
	@property
	def is_staff(self):
		return self.staff
	
	@property
	def is_admin(self):
		return self.admin
	
	@property
	def is_active(self):
		return self.active

	objects = UserManager()


# class Profile(models.Model):
# 	user = models.OneToOneField(User)


class GuestEmail(models.Model):
	email = models.EmailField()
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.email