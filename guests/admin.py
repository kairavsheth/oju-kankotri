from django.contrib import admin

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
    model = Person
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GroupInline(admin.StackedInline):
    model = Group
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'date', 'venue', 'location')
    inlines = (InvitationsInline2,)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    fields = ('name',)
    inlines = (GroupInline,)
    list_display = ('name',)
    sortable_by = ('name',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = ('family', 'alias',)
    inlines = (PersonInline,)
    list_display = ('family', 'alias')
    list_filter = ('family',)
    sortable_by = ('family', 'alias')
    autocomplete_fields = ('family',)
    search_fields = ('alias',)


@admin.action(description='Invites sent')
def invites_sent(modeladmin, request, queryset):
    queryset.update(sent=True)


@admin.action(description='Mark as not Sent')
def invites_unsent(modeladmin, request, queryset):
    queryset.update(sent=False)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = ('sent', 'title', 'name', 'senior', 'group', 'phone', 'sender',)
    inlines = (InvitationsInline,)
    list_display = ('title', 'name', 'senior', 'group', 'family_id', 'phone', 'sent',)
    list_filter = ('sender', 'sent',)
    sortable_by = ('name', 'group',)
    autocomplete_fields = ('group',)
    search_fields = ('name', 'phone',)
    actions = (invites_sent,)

    @admin.display
    def family_id(self, obj):
        return obj.group.family.id


admin.site.site_header = 'DigiKankotri Admin'
