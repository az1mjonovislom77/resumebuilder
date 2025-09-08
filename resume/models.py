from django.db import models
from django.core.validators import FileExtensionValidator


class Template(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True, blank=True)
    selected = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    html_file = models.FileField(
        upload_to="templates/",
        validators=[FileExtensionValidator(['html'])],
        null=True, blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/product/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'svg', 'webp'])
    ], null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fullname"]

    def __str__(self):
        return self.fullname


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.position} at {self.company_name}"


class Education(models.Model):
    id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution_name}"


class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.level})"
