import vobject
from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.forms import forms, fields
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.safestring import mark_safe

from contacts.models import Contact, Sender, User
from guests.models import Person


class PersonInline(admin.TabularInline):
    fields = ('title', 'senior', 'name', 'group', 'phone',)
    model = Person
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass


@admin.register(Sender)
class SenderAdmin(FilterUserAdmin):
    fields = ('name',)
    inlines = (PersonInline,)


class ImportForm(forms.Form):
    file = fields.FileField()


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
            return mark_safe(f'<a href="/admin/guests/person/{person.id}/">{person.name} by {person.sender.name}</a>')
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

            with open(request.FILES["file"].temporary_file_path(), 'r') as file:
                indata = file.read()
                vc = vobject.readComponents(indata)
                vo = next(vc, None)
                while vo is not None:
                    if 'fn' in vo.contents and 'tel' in vo.contents:
                        phone = ''.join(i for i in vo.contents['tel'][0].value if i.isnumeric()).lstrip('0')
                        if len(phone) == 10:
                            phone = '91' + phone
                        Contact(name=vo.contents['fn'][0].value, phone=phone).save()
                    vo = next(vc, None)

            self.message_user(request, "Your file has been imported")
            return redirect("..")
        form = ImportForm()
        payload = {"form": form}
        return render(
            request, "admin/import_form.html", payload
        )
