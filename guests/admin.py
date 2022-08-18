from django.contrib import admin

from Kankotri.utils import FilterUserAdmin
from guests.models import Event, Family, Person, Invitation, Group


class InvitationsInline(admin.StackedInline):
    model = Invitation
    fields = ('event', 'expected')


class InvitationsInline2(admin.TabularInline):
    model = Invitation
    fields = ('person', 'event', 'expected')
    readonly_fields = ('person',)

    def has_add_permission(self, request, obj=None):
        return False


class PersonInline(admin.StackedInline):
    exclude = ('side',)
    model = Person
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GroupInline(admin.StackedInline):
    exclude = ('side',)
    model = Group
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(FilterUserAdmin):
    fields = ('name', 'date', 'venue', 'location')
    inlines = (InvitationsInline2,)


@admin.register(Family)
class FamilyAdmin(FilterUserAdmin):
    fields = ('name',)
    inlines = (GroupInline,)
    list_display = ('name',)
    sortable_by = ('name',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(FilterUserAdmin):
    fields = ('family', 'alias',)
    inlines = (PersonInline,)
    list_display = ('family', 'alias')
    list_filter = ('family',)
    sortable_by = ('family', 'alias')
    autocomplete_fields = ('family',)
    search_fields = ('alias',)


@admin.register(Person)
class PersonAdmin(FilterUserAdmin):
    fields = ('title', 'name', 'senior', 'group', 'phone', 'sender',)
    inlines = (InvitationsInline,)
    list_display = ('name', 'group',)
    list_filter = ('group',)
    sortable_by = ('name', 'group')
    autocomplete_fields = ('group',)
    search_fields = ('name', 'phone',)


admin.site.site_header = 'DigiKankotri Admin'
