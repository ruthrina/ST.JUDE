from django.db import models

from django.urls import reverse

# Create your models here.



class HelpingHand(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='helping_hands/')

    def __str__(self):
        return self.title


class CharityEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='event_images/')
    join_url = models.URLField(blank=True, null=True)  # For Join Now button

    def __str__(self):
        return self.title
    

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog_images/")
    content = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=255, default="Admin")
    comments_count = models.IntegerField(default=0)
    link = models.URLField(default='https://example.com') 

    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    image = models.ImageField(upload_to='testimonials/')
    content = models.TextField()
    rating = models.IntegerField(default=5)  # Rating from 1 to 5 stars

    def __str__(self):
        return self.name
    
class CharityGallery(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/',  blank=True, null=True)
    video = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"




class VolunteerApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    skills = models.TextField()
    availability = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"




class PartnershipApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    organization = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return self.name

# models.py
from django.db import models

class Donation(models.Model):
    order_tracking_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=50, default="PENDING")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Donation by {self.donor_name} (Status: {self.payment_status})"
