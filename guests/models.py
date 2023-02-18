from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=32)
    date = models.DateTimeField()
    venue = models.CharField(max_length=256)
    location = models.URLField()

    def __str__(self):
        return self.name


class Family(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Families"

    def __str__(self):
        return self.name


class Group(models.Model):
    alias = models.CharField(max_length=16)
    family = models.ForeignKey(Family, related_name='groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.alias + ' - ' + self.family.name

class Person(models.Model):
    title = models.IntegerField(choices=((0, ''), (1, 'Mr.'), (2, 'Mrs.'), (3, 'Family')))
    senior = models.BooleanField('Senior for Shri/Smt')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='persons')
    name = models.CharField(max_length=128)
    phone = models.BigIntegerField(null=True, blank=True)
    sender = models.ForeignKey('contacts.Sender', on_delete=models.CASCADE)
    sent = models.BooleanField()

    def __str__(self):
        title = {1: 'Shri ', 2: 'Smt. '}.get(self.title, '') if self.senior else \
            ['', 'Mr. ', 'Mrs. ', '(&) Family Member - '][self.title]
        return title + self.name


class Invitation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='invitations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expected = models.BooleanField()

    def __str__(self):
        return self.person.name + ' - ' + self.event.name

    class Meta:
        unique_together = ['person', 'event']
