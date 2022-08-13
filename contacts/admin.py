from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.forms import forms, fields
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe

from Kankotri.utils import FilterUserAdmin
from contacts.models import Contact, Sender, User
from guests.models import Person


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass


@admin.register(Sender)
class SenderAdmin(FilterUserAdmin):
    fields = ('name',)


def ImportForm(issuperuser):
    class F(forms.Form):
        file = fields.FileField()

    class F2(F):
        side = fields.ChoiceField(choices=((i.id, i.username) for i in User.objects.all()))

    return F2() if issuperuser else F()


@admin.register(Contact)
class ContactAdmin(FilterUserAdmin):
    list_display = ('name', 'phone', 'added',)
    fields = ('name', 'phone', 'added',)
    search_fields = ('name', 'phone',)
    readonly_fields = ('added',)
    sortable_by = ('added',)

    change_list_template = "entities/imported_changelist.html"

    def added(self, instance):
        try:
            person = Person.objects.filter(phone=instance.phone).all()[0]
            return mark_safe(f'<a href="/admin/guests/person/{person.id}/">{person}')
        except IndexError:
            return mark_safe(f'<a href="/admin/guests/person/add/?name={instance.name}&phone={instance.phone}">Add</a>')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_file),
        ]
        return my_urls + urls

    def import_file(self, request):
        if request.method == "POST":

            file = open(request.FILES["file"].temporary_file_path(), 'r')
            data = {}
            for line in file:
                black_list = ['BEGIN', 'VERSION', 'CHARSET']
                end_tag = ['END']
                name_tag = ["N"]
                first_name_tag = ['FN']
                numbers_tag = ['TEL', 'CELL']

                if [ele for ele in black_list if (ele in line)]:
                    continue

                # NAMES
                if [ele for ele in name_tag if (ele in line)] and not [ele for ele in first_name_tag if (ele in line)]:
                    namer = line.split(':')
                    lenghtOfnamer = len(namer)
                    if lenghtOfnamer == 2:
                        if namer[-1].strip() != 'VCARD':
                            data['name'] = namer[-1].strip()
                    else:
                        joinNamers = ''.join(namer[1:])
                        if joinNamers.strip() != 'VCARD':
                            data['name'] = joinNamers.strip()

                # NUMBERS
                if [ele for ele in numbers_tag if (ele in line)]:
                    namer = line.split(':')
                    lenghtOfnamer = len(namer)
                    if lenghtOfnamer == 2:
                        data['phone'] = namer[-1].strip()
                    else:
                        joinNamers = namer[1:]

                        for i in range(len(joinNamers)):
                            joinNamers[i] = joinNamers[i].strip()
                        data['phone'] = joinNamers

                # FIRST NAMES
                if [ele for ele in first_name_tag if (ele in line)]:
                    namer = line.split(':')
                    lenghtOfnamer = len(namer)
                    if lenghtOfnamer == 2:
                        data['first name'] = namer[-1].strip()
                        if len(namer[-1]) > 9:
                            if namer[-1].isnumeric():
                                data['Cell'] = int(namer[-1].strip())
                    else:
                        joinNamers = ''.join(namer[1:])
                        data['first name'] = joinNamers.strip()

                        if len(joinNamers) > 9:
                            if joinNamers.isnumeric():
                                data['Cell'] = int(joinNamers.strip())

                # END
                if [ele for ele in end_tag if (ele in line)]:
                    print(data)
                    if 'phone' in data and data['phone']:
                        phone = ''.join(i for i in data['phone'] if i.isnumeric()).lstrip('0')
                        if len(phone) == 10:
                            phone = '91' + phone
                        new = Contact(name=data['first name' if 'first name' in data else 'name'],
                                      phone=phone,
                                      side_id=request.POST['side'] if request.user.is_superuser else request.user.id)
                        new.save()
                    data = {}

            self.message_user(request, "Your file has been imported")
            return redirect("..")
        form = ImportForm(request.user.is_superuser)
        payload = {"form": form}
        return render(
            request, "admin/import_form.html", payload
        )
