from django.contrib import admin
from .models import HelpingHand,CharityEvent,BlogPost, Testimonial,CharityGallery,ContactMessage,VolunteerApplication, PartnershipApplication

# Register your models here.

admin.site.register(HelpingHand)
admin.site.register(CharityGallery)

@admin.register(CharityEvent)
class CharityEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time')
    search_fields = ('title', 'description')
    list_filter = ('date',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author", "comments_count")
    search_fields = ("title", "author")

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'rating')  # Fields to display in list view
    search_fields = ('name', 'profession', 'content')  # Enable search by name, profession, and content

admin.site.register(Testimonial, TestimonialAdmin)

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email')



@admin.register(PartnershipApplication)
class PartnershipApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'organization')  # Display these fields in the admin list
    search_fields = ('name', 'email', 'organization')  # Enable search functionality
    list_filter = ('organization',)  # Add a filter for organization


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')

admin.site.register(ContactMessage, ContactMessageAdmin)





