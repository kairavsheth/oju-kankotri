from django.db import models


class Event(models.Model):
    side = models.ForeignKey('contacts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    date = models.DateTimeField()
    venue = models.CharField(max_length=256)
    location = models.URLField()

    def __str__(self):
        return self.name


class Family(models.Model):
    side = models.ForeignKey('contacts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name


class Group(models.Model):
    side = models.ForeignKey('contacts.User', on_delete=models.CASCADE)
    alias = models.CharField(max_length=16)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.alias + ' - ' + self.family.name


class Person(models.Model):
    side = models.ForeignKey('contacts.User', on_delete=models.CASCADE)
    title = models.IntegerField(choices=((0, ''), (1, 'Mr.'), (2, 'Mrs.'), (3, 'Family')))
    senior = models.BooleanField('Senior for Shri/Smt')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.BigIntegerField(null=True, blank=True)
    sender = models.ForeignKey('contacts.Sender', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='invitations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expected = models.BooleanField()

    class Meta:
        unique_together = ['person', 'event']
