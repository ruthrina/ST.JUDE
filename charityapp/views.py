from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactMessage
from .models import HelpingHand,CharityEvent,BlogPost,Testimonial, CharityGallery
from .forms import VolunteerForm, PartnershipApplicationForm
from django.contrib import messages
from datetime import datetime
from dateutil.parser import parse
from django.utils import timezone  # Import timezone for handling timezones
import logging
import requests
from django.core.cache import cache
import requests
import json
import logging
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Donation
from django.http import HttpResponse, JsonResponse




def home(request):
    hands = HelpingHand.objects.all()  # Get all HelpingHand objects
    events = CharityEvent.objects.order_by('date')  # Fetch events sorted by date
    blogs = BlogPost.objects.all()  # Get all blog objects

    # Create a range of stars based on the rating
    testimonials = Testimonial.objects.all()
    for testimonial in testimonials:
        testimonial.stars = range(1, testimonial.rating + 1)  # Pass a range for stars

    return render(request, 'home.html', {
        'hands': hands,
        'events': events,
        'blogs': blogs,
        'testimonials': testimonials
    })


def about(request):
    return render(request, 'about.html')

def programs(request):
    return render(request, 'programs.html')

def get_involved(request):
    return render(request, 'get_involved.html')


def events(request):
    events = CharityEvent.objects.order_by('date')  # Fetch events sorted by date
    return render(request, 'event.html', {        
        'events': events,        
    })


def gallery(request):
    media_items = CharityGallery.objects.all()
    return render(request, 'gallery.html', {'media_items': media_items})


def contact(request):
    return render(request, 'contact.html')


# Views for 'What We Do' sub-sections
def educational_support(request):
    return render(request, 'what_we_do/educational_support.html')

def spiritual_guidance(request):
    return render(request, 'what_we_do/spiritual_guidance.html')

def health_wellness(request):
    return render(request, 'what_we_do/health_wellness.html')

def moral_development(request):
    return render(request, 'what_we_do/moral_development.html')

def community_outreach(request):
    return render(request, 'what_we_do/community_outreach.html')

def emergency_relief(request):
    return render(request, 'what_we_do/emergency_relief.html')


# CHARITY

def get_involved(request):
    return render(request, 'charity/get_involved.html')

def donate(request):
    return render(request, 'charity/donate.html')




def fundraise(request):
    return render(request, 'charity/fundraise.html')

def gifts(request):
    return render(request, 'charity/gifts.html')

def order(request):
    return render(request, 'charity/order.html')

def contact(request):
    success_message = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save the contact form submission to the database
            ContactMessage.objects.create(name=name, email=email, message=message)

            # Set the success message to trigger the alert
            success_message = "Your message has been sent successfully. Thank you!"

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'success_message': success_message})

def volunteer_view(request):
    form = VolunteerForm()
    if request.method == "POST":
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your application has been submitted successfully!")
            form = VolunteerForm()  # Reset form after successful save

    return render(request, "charity/volunteer.html", {"form": form})

def partnership(request):
    if request.method == "POST":
        form = PartnershipApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your interest! We’ll get back to you soon.")
            return redirect('partnership')  # Redirect to clear form data
    else:
        form = PartnershipApplicationForm()  # Ensure a fresh form

    return render(request, "charity/partnership.html", {"form": form})



# Set up logger
logger = logging.getLogger(__name__)

# =========================== GET ACCESS TOKEN =========================== #
def get_access_token():
    """Fetches and caches the Pesapal access token"""
    # Try to get the token from cache first
    token = cache.get("pesapal_access_token")
    expiry_time = cache.get("pesapal_access_token_expiry")

    # Check if token exists and is not expired
    if token and expiry_time and timezone.now() < expiry_time:
        return token

    # If token is expired or not found, fetch a new one
    return fetch_new_token()

def fetch_new_token():
    """Fetch a new token from Pesapal and cache it"""
    # URL to get the access token
    url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # The request body with your Pesapal credentials
    data = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
    }

    try:
        # Send the POST request to get the token
        response = requests.post(url, headers=headers, json=data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            token_data = response.json()

            # Get the token and expiry date
            new_token = token_data.get("token")
            expiry_date = token_data.get("expiryDate")

            if new_token:
                # Calculate expiration time based on expiryDate
                expiry_datetime = parse(expiry_date)
                cache.set("pesapal_access_token", new_token, timeout=calculate_timeout(expiry_date))
                cache.set("pesapal_access_token_expiry", expiry_datetime, timeout=calculate_timeout(expiry_date))

                return new_token
            else:
                logger.error("Pesapal token response missing 'token' key: %s", token_data)
                return None
        else:
            # Log if the request failed
            logger.error("Failed to get Pesapal access token. Response: %s", response.text)
            return None
    except Exception as e:
        # Log any errors that occurred during the request
        logger.error("Error occurred while requesting Pesapal token: %s", str(e))
        return None

def calculate_timeout(expiry_date):
    """Calculate the timeout for the cached token based on expiryDate."""
    # Parse the expiryDate from the API response (this will be an aware datetime)
    expiry_datetime = parse(expiry_date)

    # Get the current time with timezone info
    current_time = timezone.now()  # Use timezone-aware datetime

    # Calculate the time difference in seconds
    time_diff = (expiry_datetime - current_time).total_seconds()

    # Ensure timeout is not negative (if the token has expired)
    return max(time_diff, 0)


import logging
import uuid
import requests
from django.http import JsonResponse
from django.shortcuts import redirect

# Logger
logger = logging.getLogger(__name__)

# Pesapal URLs
PESAPAL_ORDER_URL = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest"

def submit_order_request(request):
    """ Submits an order request to Pesapal with dynamic user input """

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # Get token
    token = get_access_token()
    if not token:
        return JsonResponse({"error": "Failed to retrieve access token"}, status=400)

    # Retrieve user input from form
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    email_address = request.POST.get("email_address", "").strip()
    phone_number = request.POST.get("phone_number", "").strip()
    amount = request.POST.get("amount", "").strip()
    city = request.POST.get("city", "").strip()
    start_date = request.POST.get("start_date", "").strip()  # Format: dd-MM-yyyy
    end_date = request.POST.get("end_date", "").strip()      # Format: dd-MM-yyyy
    frequency = request.POST.get("frequency", "").strip() 

    # Validate required fields
    if not all([first_name, last_name, email_address, phone_number, amount, city]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    # Generate unique order ID
    order_id = f"DON-{uuid.uuid4().hex[:8]}"  # e.g., DON-4a7b8c9d

    # Prepare dynamic order data
    order_data = {
        "id": order_id,  # Unique Order ID
        "currency": "UGX",
        "amount": float(amount),
        "description": "Donation to Charity",
        "callback_url": "https://st-thaddeous.onrender.com/donate/",
        "redirect_mode": "TOP_WINDOW",
        "notification_id": "1443cc38-06f0-474b-847f-dc11ef586fe8",
        "branch": "Main Branch",
        "billing_address": {
            "email_address": email_address,
            "phone_number": phone_number,
            "country_code": "UG",
            "first_name": first_name,
            "last_name": last_name,
            "city": city
        },
         "account_number": f"{order_id}",  # You can link the account number to the order ID or invoice ID
        "subscription_details": {
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency  # DAILY, WEEKLY, MONTHLY, YEARLY
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(PESAPAL_ORDER_URL, headers=headers, json=order_data)
        if response.status_code == 200:
            data = response.json()
            payment_url = data.get("redirect_url")

            if payment_url:
                return redirect(payment_url)  # Redirect user to Pesapal payment page
            else:
                logger.error("Missing redirect_url: %s", data)
                return JsonResponse({"error": "Failed to retrieve payment URL"}, status=400)
        else:
            logger.error("Pesapal order request failed: %s", response.text)
            return JsonResponse({"error": "Failed to create order", "details": response.json()}, status=400)
    except Exception as e:
        logger.error("Error submitting order request: %s", str(e))
        return JsonResponse({"error": "Internal server error"}, status=500)


from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from .models import Donation

@csrf_exempt
def pesapal_ipn(request):
    """Handles Pesapal IPN updates"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_tracking_id = data.get("OrderTrackingId")
            status = data.get("status")

            # Update the donation record
            donation = Donation.objects.filter(order_tracking_id=order_tracking_id).first()
            if donation:
                donation.payment_status = status
                donation.save()
                return JsonResponse({"message": "IPN Received"}, status=200)
            else:
                return JsonResponse({"error": "Donation not found"}, status=404)
        except Exception as e:
            logger.error("Error processing IPN: %s", str(e))
            return JsonResponse({"error": "Invalid data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

PESAPAL_TRANSACTION_STATUS_URL = "https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus"

def check_payment_status(request, order_tracking_id):
    """Checks payment status via Pesapal API"""
    
    token = get_access_token()
    if not token:
        return JsonResponse({"error": "Failed to retrieve access token"}, status=400)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(f"{PESAPAL_TRANSACTION_STATUS_URL}?orderTrackingId={order_tracking_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")

            # Update donation status
            donation = Donation.objects.filter(order_tracking_id=order_tracking_id).first()
            if donation:
                donation.payment_status = status
                donation.save()
                return JsonResponse({"status": status})
            else:
                return JsonResponse({"error": "Donation not found"}, status=404)
        else:
            return JsonResponse({"error": "Failed to fetch status"}, status=response.status_code)
    except Exception as e:
        logger.error("Error fetching transaction status: %s", str(e))
        return JsonResponse({"error": "Internal server error"}, status=500)
    

import requests
from django.conf import settings
from django.utils import timezone
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Base URL for Pesapal (use production or sandbox depending on environment)
BASE_URL = "https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus"

def get_transaction_status(order_tracking_id):
    """Get the status of a transaction based on the OrderTrackingId."""
    # Get the access token
    token = get_access_token()

    if not token:
        logger.error("Failed to retrieve access token.")
        return None

    # Construct the request URL with the OrderTrackingId
    url = f"{BASE_URL}?orderTrackingId={order_tracking_id}"

    # Set headers for the GET request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request to Pesapal to fetch transaction status
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            transaction_data = response.json()

            # Log the response for debugging
            logger.info("Pesapal GetTransactionStatus Response: %s", transaction_data)

            # You can now process the payment status and update your system accordingly
            status_code = transaction_data.get("status_code")
            payment_status = transaction_data.get("payment_status_description")
            amount = transaction_data.get("amount")
            payment_method = transaction_data.get("payment_method")
            currency = transaction_data.get("currency")
            confirmation_code = transaction_data.get("confirmation_code")
            payment_account = transaction_data.get("payment_account")

            # Example of handling different payment statuses
            if status_code == 1:  # COMPLETED
                logger.info("Payment completed successfully.")
                # Store transaction details in your system as needed
            elif status_code == 2:  # FAILED
                logger.error("Payment failed: %s", payment_status)
            elif status_code == 3:  # REVERSED
                logger.warning("Payment was reversed.")
            else:  # INVALID
                logger.error("Invalid payment status: %s", payment_status)

            # Return the transaction details or payment status
            return transaction_data

        else:
            logger.error("Failed to get transaction status. Response: %s", response.text)
            return None

    except requests.exceptions.RequestException as e:
        logger.error("Error occurred while fetching transaction status: %s", str(e))
        return None

def handle_callback(request):
    """Handle the callback from Pesapal after the customer makes a payment."""
    order_tracking_id = request.GET.get('OrderTrackingId')

    if order_tracking_id:
        transaction_status = get_transaction_status(order_tracking_id)
        if transaction_status:
            # Process the payment status (e.g., update order, send confirmation, etc.)
            # Return a response based on the status
            return HttpResponse(f"Transaction status: {transaction_status.get('payment_status_description')}")
        else:
            return HttpResponse("Error fetching transaction status.", status=500)
    else:
        return HttpResponse("OrderTrackingId is missing.", status=400)


def ipn_response(order_tracking_id, merchant_reference):
    """Respond to Pesapal IPN to confirm receipt of the payment notification."""
    ipn_response_data = {
        "orderNotificationType": "IPNCHANGE",
        "orderTrackingId": order_tracking_id,
        "orderMerchantReference": merchant_reference,
        "status": 200  # 200 means the request was successfully received
    }
    
    return JsonResponse(ipn_response_data)


import logging
import requests
from django.http import JsonResponse
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Pesapal Production URL (use Sandbox in development environment)
PESAPAL_TRANSACTION_STATUS_URL = "https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus"

def get_transaction_status(request, order_tracking_id):
    """
    Get the status of a transaction based on the orderTrackingId.
    This endpoint queries the Pesapal API to check the payment status.
    """
    # Get the access token (assuming you have a method for this)
    token = get_access_token()
    
    if not token:
        return JsonResponse({"error": "Failed to retrieve access token"}, status=400)

    # Construct the request URL with the OrderTrackingId
    url = f"{PESAPAL_TRANSACTION_STATUS_URL}?orderTrackingId={order_tracking_id}"

    # Set headers for the GET request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        # Make the GET request to Pesapal to fetch transaction status
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            transaction_data = response.json()

            # Process the payment status (e.g., COMPLETED, FAILED)
            payment_status = transaction_data.get("payment_status_description")
            status_code = transaction_data.get("status_code")
            amount = transaction_data.get("amount")
            payment_method = transaction_data.get("payment_method")
            currency = transaction_data.get("currency")
            confirmation_code = transaction_data.get("confirmation_code")
            payment_account = transaction_data.get("payment_account")

            # Log the transaction details
            logger.info(f"Payment Status: {payment_status} (Status Code: {status_code})")

            # Return the transaction details
            return JsonResponse({
                "payment_status": payment_status,
                "status_code": status_code,
                "amount": amount,
                "payment_method": payment_method,
                "currency": currency,
                "confirmation_code": confirmation_code,
                "payment_account": payment_account
            })
        else:
            # If the request failed, log and return error
            logger.error(f"Failed to get transaction status. Response: {response.text}")
            return JsonResponse({"error": "Failed to get transaction status"}, status=400)

    except Exception as e:
        logger.error(f"Error fetching transaction status: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)
    
