from django.contrib import admin
from .models import * 
from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe
admin.site.register((CustomUser,UserActivity,UserProfile,AddressGlobal))

class StateAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'price', 'created_at', 'updated_at')
    list_display_links = ('indented_title',)

    def indented_title(self, obj):
        """
        This method adds indentation to the title of each item in the list_display.
        """
        return mark_safe(
            '<div style="text-indent:{}px">{}</div>'.format(
                obj.level * 20,
                obj.name
            )
        )


admin.site.register(State,StateAdmin)