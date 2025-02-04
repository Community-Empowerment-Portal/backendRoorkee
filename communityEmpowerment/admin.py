from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group, Permission
from .models import (
    State, Department, Organisation, Scheme, Beneficiary, SchemeBeneficiary, 
    Benefit, Criteria, Procedure, Document, SchemeDocument, Sponsor, ProfileField, ProfileFieldChoice, ProfileFieldValue, CustomUser,
    SchemeSponsor, CustomUser, Banner, Tag, SchemeReport, WebsiteFeedback, SchemeFeedback, Category
)
from django.db.models import Count
from django.db.models import Min


admin.site.site_header = "Community Empowerment Portal Admin Panel"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to your Admin Panel"

admin.site.register(State)
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('category_display', 'tag_count', 'related_tags_display', 'weight')
    list_filter = ('category',)
    search_fields = ('category',)
    ordering = ["category"]
    # inlines = [TagInline]
    def related_tags_display(self, obj):
        # Get all tags related to the same category as the current tag
        related_tags = Tag.objects.filter(category=obj.category)
        related_tag_names = ", ".join([tag.name for tag in related_tags])
        return related_tag_names

    related_tags_display.short_description = "Related Tags"
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        valid_categories = ["scholarship", "job", "sc", "st", "obc", "minority"]
        # return (
        #     queryset.filter(category__in=valid_categories)
        #     .order_by('category')
        #     .distinct('category')  
        # )
        valid_category_objects = Category.objects.filter(name__in=valid_categories)

        return (
            queryset.filter(category__in=valid_category_objects)  # Use ForeignKey filtering
            .order_by('category')
            .distinct('category')
        )

    def category_display(self, obj):
        return obj.category

    category_display.admin_order_field = 'category'
    category_display.short_description = 'Category'

    def tag_count(self, obj):
        return obj.__class__.objects.filter(category=obj.category).count()
    
    tag_count.short_description = "Tag Count"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        tag_instance = self.get_object(request, object_id)  # Get the current Tag instance
        
        # Fetch all related tags in the same category as the current tag
        related_tags = Tag.objects.filter(category=tag_instance.category).exclude(id=tag_instance.id)  # Exclude the current tag itself
        
        # Limit the number of related tags shown initially (e.g., show 5 tags)
        initial_related_tags = related_tags[:5]
        
        # Example custom data (you can replace this with any data you need)
        custom_data = ["Custom info", "Other related data", "Example list item"]

        # Add the related tags and custom data to the extra context
        if extra_context is None:
            extra_context = {}

        extra_context['related_tags'] = initial_related_tags  # Add initial related tags to the context
        extra_context['custom_data'] = custom_data  # Add any custom data you want to show
        extra_context['all_related_tags'] = related_tags  # Add all related tags (for the "See All" option)

        # Call the super method to render the change view with the extra context
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Tag, TagAdmin)
admin.site.register(Department)
admin.site.register(Organisation)
admin.site.register(SchemeBeneficiary)
admin.site.register(Benefit)
admin.site.register(Criteria)
admin.site.register(Procedure)
admin.site.register(SchemeDocument)
admin.site.register(SchemeSponsor)


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_active','groups')
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','user_permissions', 'groups')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
#         ),
#     )
#     readonly_fields = ('date_joined',)
#     search_fields = ('username', 'email')
#     ordering = ('username',)


# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Banner)
class BannerAdmin(ImportExportModelAdmin):
    list_display = ['title', 'is_active']
    search_fields = ['title']

class SchemeResource(resources.ModelResource):
    class Meta:
        model = Scheme
        fields = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')
        export_order = ('id', 'title', 'department__department_name', 'introduced_on', 'valid_upto', 'funding_pattern', 'description', 'scheme_link')

@admin.register(Scheme)
class SchemeAdmin(ImportExportModelAdmin):
    resource_class = SchemeResource
    list_display = ('title', 'department', 'introduced_on', 'valid_upto', 'funding_pattern')
    search_fields = ('title', 'description')
    list_filter = ('department', 'introduced_on', 'valid_upto', 'funding_pattern')

@admin.register(SchemeReport)
class SchemeReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'scheme_id', 'created_at'] 
    list_filter = ['created_at'] 

@admin.register(WebsiteFeedback)
class WebsiteFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'description', 'created_at'] 
    list_filter = ['created_at']

@admin.register(SchemeFeedback)
class SchemeFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheme', 'feedback', 'rating', 'created_at')
    search_fields = ('user__username', 'scheme__title', 'feedback')
    list_filter = ('created_at', 'rating')



admin.site.register(Permission)

    
# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('category', 'name', 'is_active')
#     list_filter = ('category', 'is_active')  # Filter by category
#     search_fields = ('name',)
    
class ProfileFieldChoiceInline(admin.TabularInline):
    model = ProfileFieldChoice
    extra = 0
    fields = ('value', 'is_active')
    readonly_fields = ('value',)
    can_delete = False
    def has_add_permission(self, request, obj=None):
        """Prevent adding new choices inline."""
        return False


@admin.register(ProfileField)
class ProfileFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_active','position',)
    list_filter = ['is_active', 'field_type']
    list_editable = ['is_active', 'position']
    readonly_fields = ['name', 'field_type', 'placeholder', 'min_value', 'max_value']
    inlines = [ProfileFieldChoiceInline]
    def has_add_permission(self, request):
        """Disallow adding new fields."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deleting fields."""
        return False

@admin.register(ProfileFieldValue)
class ProfileFieldValueAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'value')

class ProfileFieldInline(admin.TabularInline):
    model = ProfileFieldValue
    extra = 0
    readonly_fields = ('field', 'value') 

    def has_add_permission(self, request, obj):
        return False 

    def has_delete_permission(self, request, obj=None):
        return False

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_email_verified')
    list_filter = ('is_active', 'is_staff', 'is_email_verified','groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ['name']}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ['last_login']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    inlines = [ProfileFieldInline]



admin.site.register(CustomUser, CustomUserAdmin)
