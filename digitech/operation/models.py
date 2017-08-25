from django.db import models
from geoposition.fields import GeopositionField
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import admin
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    position = GeopositionField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("academics:timetable-item", kwargs={"slug": self.slug})
admin.site.register(Location)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    location = models.ForeignKey(Location, null=True, blank=True)
    description = models.TextField(default='More info ...')

    def __str__(self):
        return self.name
admin.site.register(Organization)


class PowerLine(models.Model):
    name = models.CharField(max_length=255)
    source = models.ForeignKey(Location,)
    voltage = models.IntegerField(default=0)
    description = models.TextField(default='More info ...')

    def __str__(self):
        return self.name
admin.site.register(PowerLine)


class Transformer(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    location = models.ForeignKey(Location, null=True, blank=True, related_name='location')
    power_line = models.OneToOneField(PowerLine, null=True, blank=True)
    input = models.IntegerField(null=True, blank=True)
    output = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField('Installation date ', null=True, blank=True)

    def __str__(self):
        return 'T{0}'.format(self.id)

admin.site.register(Transformer)


class Machinery(models.Model):
    name = models.CharField(max_length=50)
    no = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='machine_img',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    def __str__(self):
        return self.name

admin.site.register(Machinery)


class Rank(models.Model):
    title = models.CharField(null=True, blank=True, max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
admin.site.register(Rank)


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    id = models.CharField(max_length=15, primary_key=True, unique=True)
    rank = models.ForeignKey(Rank, null=True, blank=True)

    def __str__(self):
        return self.id

admin.site.register(Employee)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.ImageField(upload_to='project_img',
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("operation:project-detail", kwargs={"pk": self.id})
    # def get_absolute_url(self):
    #     return reverse("operation:project", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Project.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_project_receiver, sender=Project)
admin.site.register(Project)

