from django.contrib import admin


class FilterUserAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = self.fields
        if request.user.is_superuser:
            fields += ('side',)
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.side = request.user
        obj.save()

    def get_queryset(self, request):
        # For Django < 1.6, override queryset instead of get_queryset
        qs = super(FilterUserAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(side=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            # the changelist itself
            return True
        return obj.side == request.user
