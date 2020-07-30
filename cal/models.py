from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

'''
Overridden the django's built-in Auth User Model with custom user model,
in which email is required for logging in instead of username.
'''


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AccountManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


'''
Set subjects and periods day-wise
for example-
            MONDAY
    Physics 8:30-9:30
    Biology 9:30-10:30

reference: https://stackoverflow.com/questions/30628006/django-model-for-time-table-like-objects
'''


class TimeTable(models.Model):
    DAYS_OF_THE_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    )
    day = models.CharField(max_length=15, null=False, blank=False, choices=DAYS_OF_THE_WEEK)

    class Meta:
        verbose_name = 'Day'
        verbose_name_plural = 'Days'
    def __str__(self):
        return self.day

class TimeTableItem(models.Model):

    SUBJECTS = (
    ('Math', 'Math'),
    ('Hindi','Hindi'),
    ('English', 'English'),
    ('Computer', 'Computer'),
    ('Physics','Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biology','Biology')
    )

    START_TIME = (
    ('8:30','8:30'),
    ('9:30','9:30'),
    ('10:30','10:30'),
    ('11:30','11:30'),
    ('2:00','2:00'),
    ('3:00','3:00'),
    ('4:00','4:00'),
    )

    END_TIME = (
    ('9:30','9:30'),
    ('10:30','10:30'),
    ('11:30','11:30'),
    ('12:30','12:30'),
    ('3:00','3:00'),
    ('4:00','4:00'),
    ('5:00','5:00')
    )


    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, choices= SUBJECTS)
    start_time = models.CharField(max_length=20, choices= START_TIME)
    end_time = models.CharField(max_length=20, choices= END_TIME)

    def __str__(self):
        return 'Subject:{}, Time:{}-{}'.format(self.subject, self.start_time, self.end_time)

    class Meta:
        ordering = ('start_time',)
