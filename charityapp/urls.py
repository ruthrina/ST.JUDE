from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('get-involved/', views.get_involved, name='get_involved'),
    path('donate/', views.donate, name='donate'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('educational-support/', views.educational_support, name='educational_support'),
    path('spiritual-guidance/', views.spiritual_guidance, name='spiritual_guidance'),
    path('health-wellness/', views.health_wellness, name='health_wellness'),
    path('moral-development/', views.moral_development, name='moral_development'),
    path('community-outreach/', views.community_outreach, name='community_outreach'),
    path('emergency-relief/', views.emergency_relief, name='emergency_relief'),
     path('get-involved/', views.get_involved, name='get_involved'),
    path('donate/', views.donate, name='donate'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('partnership/', views.partnership, name='partnership'),
    path('fundraise/', views.fundraise, name='fundraise'),
    path('gifts/', views.gifts, name='gifts'), 
    path('order/', views.order, name='order'),      
    path('submit-order/', views.submit_order_request, name='submit_order'),
    path('pesapal-ipn/', views.pesapal_ipn, name='pesapal_ipn'),
    path('payment-status/<str:order_tracking_id>/', views.check_payment_status, name='check_payment_status'),
    
  
    
   
   
]
