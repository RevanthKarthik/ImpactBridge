import ssl
import os
import requests
import logging
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib import messages
import random
from django.urls import reverse
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.shortcuts import render,redirect
from django.http import JsonResponse
import certifi
import base64
from datetime import datetime, timedelta
import string
from django.contrib.auth.decorators import login_required
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from django.http import HttpResponse
from users.models import kyc
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Donation,User,Media


  
from .models import Donation
logger = logging.getLogger(__name__)


def all_donations(request):
    context = {}
    
    # Fetch all donation posts
    context['donation_posts'] = Donation.objects.all()
        
        # Fetch urgent posts by category
    context['urgent_posts'] = Donation.objects.filter(category='medical_emergency')
    context['child_posts'] = Donation.objects.filter(category='child')
    context['elder_posts'] = Donation.objects.filter(category='elders')
    context['education_posts'] = Donation.objects.filter(category='education')

    context['healthandwellness'] = Donation.objects.filter(category='healthandwellness')
    context['poverty_posts'] = Donation.objects.filter(category='poverty')
    context['community_posts'] = Donation.objects.filter(category='community')
    context['humanity_posts'] = Donation.objects.filter(category='humanitarian')
    context['arts_posts'] = Donation.objects.filter(category='arts')
    context['women_posts'] = Donation.objects.filter(category='women')
    context['environment_posts'] = Donation.objects.filter(category='environment')
    context['hunger_posts'] = Donation.objects.filter(category='hunger')
    context['urgent_posts'] = Donation.objects.filter(category='medical_emergency')
        
        
        # Fetch first image associated with each donation
    donation_posts_with_images = []
    
    for post in context['donation_posts']:
            # Fetch all media objects associated with the current donation post
            media_objects = Media.objects.filter(donation_id=post.pk)

            # Fetch the first image associated with the current donation post
            first_image = Media.objects.filter(donation=post, media_type='image').first()

            if first_image:
                print(first_image.file.url)  # Debugging print statement

            # Append the donation post and first image tuple to the list
            donation_posts_with_images.append((post, first_image))

        # Assign the list to the context
    context['donation_posts_with_images'] = donation_posts_with_images
    return render(request, 'donations/donationsdisplay.html', context)

   

def home_view(request):
    context = {}
    
    # Fetch all donation posts
    context['donation_posts'] = Donation.objects.all()
    
    # Fetch urgent posts by category
    context['urgent_posts'] = Donation.objects.filter(category='medical_emergency')
    context['child_posts'] = Donation.objects.filter(category='child')
    context['elder_posts'] = Donation.objects.filter(category='elders')
    context['education_posts'] = Donation.objects.filter(category='education')

    context['healthandwellness'] = Donation.objects.filter(category='healthandwellness')
    context['poverty_posts'] = Donation.objects.filter(category='poverty')
    context['community_posts'] = Donation.objects.filter(category='community')
    context['humanity_posts'] = Donation.objects.filter(category='humanitarian')
    context['arts_posts'] = Donation.objects.filter(category='arts')
    context['women_posts'] = Donation.objects.filter(category='women')
    context['environment_posts'] = Donation.objects.filter(category='environment')
    context['hunger_posts'] = Donation.objects.filter(category='hunger')
    context['urgent_posts'] = Donation.objects.filter(category='medical_emergency')
    
    
    # Fetch first image associated with each donation
    donation_posts_with_images = []
   
    for post in context['donation_posts']:
        # Fetch all media objects associated with the current donation post
        media_objects = Media.objects.filter(donation_id=post.pk)

        # Fetch the first image associated with the current donation post
        first_image = Media.objects.filter(donation=post, media_type='image').first()

        if first_image:
            print(first_image.file.url)  # Debugging print statement

        # Append the donation post and first image tuple to the list
        donation_posts_with_images.append((post, first_image))

    # Assign the list to the context
    context['donation_posts_with_images'] = donation_posts_with_images

    
    return render(request, 'donations/home.html', context)

# Configure logging
logger = logging.getLogger(__name__)

def donation_detail_view(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    media_objects = Media.objects.filter(donation_id=pk)
    return render(request, 'donations/donation_detail.html', {'donation': donation, 'media_objects': media_objects})


def makeid(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def donate(request, donation_pk, user_pk):
    donation = get_object_or_404(Donation, pk=donation_pk)
    user = get_object_or_404(User, pk=user_pk) #author of the post
    
    user = request.user
    if request.method == 'POST':
        donation_amount = float(request.POST.get('donation_amount'))
        print(donation_amount)

        logger.info("Preparing to send a POST request to the external API.")

        # Generate a random order ID
        order_id = makeid(10) + "_" + str(random.randint(100, 10000))

    # Get the current datetime in UTC
        current_datetime_utc = datetime.utcnow()
    # Add one day to the current datetime
        date_plus_one_day = current_datetime_utc + timedelta(hours=6)

        logger.info(f"Generated order_id: {order_id}")
        logger.info(f"Date + 1 day: {date_plus_one_day}")

        # Convert the IST datetime to ISO8601 format
        ist_datetime_iso = date_plus_one_day.isoformat()+"+05:30"

        api_key = 'TEST1019726310159d84051d9684409136279101'
        api_secret = 'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76'
        auth_string = f"{api_key}:{api_secret}"
        b64_auth_string = base64.b64encode(auth_string.encode()).decode()
        date_plus_one_day_iso = (datetime.utcnow() + timedelta(days=1)).isoformat()
        
        
        return_url = request.build_absolute_uri(reverse('payment_status', kwargs={'order_id': order_id}))

        # Create the payload
        payload = {
            "order_id": order_id,
            "order_amount": donation_amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": f'{user.pk}',
                "customer_email": f'{user.email}',
                "customer_phone": f'{user.profilepersonal.phone_number}',
            },
            "order_meta": {
                "return_url" : 'https://google.com',
                
            },
            "order_expiry_time": ist_datetime_iso,
            "order_splits":
            [
                 {
                      "vendor_id": "26",
                      "percentage":100,

                 }
            ]
            
        }
        

        headers = {
            'Content-Type': 'application/json',
            'x-client-id': api_key,
            'x-client-secret': api_secret,
            'Accept': 'application/json',
            'x-api-version': '2023-08-01',
        }
        

        try:
            response = requests.post('https://sandbox.cashfree.com/pg/orders', json=payload, headers=headers, verify=certifi.where())
            response.raise_for_status()
            response_data = response.json()
           
            
            context = {
                'amount': response_data.get('order_amount', 'N/A'),
                'order_id': response_data.get('order_id', 'N/A'),
                'order_status': response_data.get('order_status', 'N/A'),
                'payment_session_id': response_data.get('payment_session_id', 'N/A'),
                'user':user,
                'donation_pk':donation_pk,
                'user_pk':user_pk
            }
           
            return render(request,'donations/payment_redirect.html',context)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {http_err.response.content}")
            context = {
                'amount': 100,
                'order_id': 'N/A',
                'order_status': 'FAILED',
                'error_message': http_err.response.content.decode(),
                'user':user,
                'donation_pk':donation_pk,
                'user_pk':user_pk
            }
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            context = {
                'amount': 100,
                'order_id': 'N/A',
                'order_status': 'FAILED',
                'error_message': str(e),
                'user':user,
                'donation_pk':donation_pk,
                'user_pk':user_pk
            }
    else:
        context = {
            'donation': donation,
            'user':user,
            'donation_pk':donation_pk,
            'user_pk':user_pk
        }

            

    return render(request, 'donations/cashfree_payment.html', context)

def payment_status(request , order_id):

    api_key = 'TEST1019726310159d84051d9684409136279101'
    api_secret = 'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76'
    auth_string = f"{api_key}:{api_secret}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
            'x-client-id': api_key,
            'x-client-secret': api_secret,
            'x-api-version': '2021-05-21',
        }
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
    try:
            # Use certifi for CA bundle
            response = requests.get(url, headers=headers, verify=certifi.where())
            response.raise_for_status()
            response_data = response.json()
            print(response_data)
            context = {
                'status': response_data.get('order_status', 'N/A'),
                'order_id': response_data.get('order_id', 'N/A'),
            }
    except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {http_err.response.content}")
            context = {
                'order_id': 'N/A',
                'order_status': 'FAILED',
                'error_message': http_err.response.content.decode()
            }
    except Exception as e:
            logger.error(f"An error occurred: {e}")
            context = {
                'order_id': 'N/A',
                'order_status': 'FAILED',
                'error_message': str(e)
            }
    return render(request,'donations/paymentstatus.html',context)


@login_required
def donation_postsss(request):
    # Fetch the kyc instance for the current logged-in user
        try:
            kyc_instance = get_object_or_404(kyc, user=request.user)
            
            # Access the vendor_id field
            vendor_id = kyc_instance.vendor_id
            
            # Log the vendor_id for debugging
            logger.debug(f'Vendor ID: {vendor_id}')

            api_key = 'TEST1019726310159d84051d9684409136279101'
            api_secret = 'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76'
            
            # Example API call using vendor_id (this is just for demonstration)
            headers = {
                'x-client-id':'TEST1019726310159d84051d9684409136279101',
                'x-client-secret':'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76',
                'x-api-version':'2022-09-01',
                'Content-Type':'application/json'
            }
            
            response = requests.get(
                f'https://sandbox.cashfree.com/pg/easy-split/vendors/vendor{vendor_id}',
                headers=headers,
                verify=certifi.where()
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            response_data = response.json()
            print(response_data)
            first_doc_status = response_data['related_docs'][0]['status']
            remarks = response_data['remarks']
            status = response_data['status']
            donation_post = Donation(user=request.user)

            if(status =='ACTIVE'):
                if request.method == 'POST':
                    print("here in post method")
                    title = request.POST.get('title')
                    description = request.POST.get('description')
                    story = request.POST.get('story')
                    category = request.POST.get('category')
                    end_date = request.POST.get('end_date')

                    files = request.FILES.getlist('file[]')
                    media_types = request.POST.getlist('media_type[]')
                    for file, media_type in zip(files, media_types):
                        if media_type in ['image', 'video']:
                            Media.objects.create(donation=donation_post, media_type=media_type, file=file)


                    goal_amount = request.POST.get('goal_amount')
                    address = request.POST.get('address')
                    pin_code = request.POST.get('pin_code')
                    country = request.POST.get('country')
                    state = request.POST.get('state')
                    email = request.POST.get('email')
                    phone_number = request.POST.get('phone_number')
                    
                    

                    donation_post.email = email
                    donation_post.phone_number = phone_number

                    donation_post.title = title
                    donation_post.description = description
                    donation_post.story = story
                    donation_post.category = category
                    donation_post.end_date = end_date

                    donation_post.goal_amount = goal_amount
                    donation_post.file = file
                    donation_post.address = address
                    donation_post.pin_code = pin_code
                    donation_post.country = country
                    donation_post.state = state
                    Media.objects.create(donation=donation_post, media_type=media_type, file=file)

                    messages.success(request,'kyc is verified')
                    if file:
                        donation_post.file = file
                    
                    try:
                        donation_post.save()
                        return redirect('profile') # here return to the page that is created for the donation post

                    except ValidationError as e:
                        messages.error(request, f'Error creating post profile: {e.message}')
                return render(request,'donations/donation_form.html',{'donation_post': donation_post,})
            else:
                messages.success(request, f'{status}')
                messages.success(request, f'{remarks}')
                return redirect('profile')
        except:
            response_data = response.json()
            print("this is when vendor is not there")
            print(response_data)
            message = response_data['status']
            messages.success(request, f'{message}')
        
            return redirect('profile')
        
@login_required
def donation_post(request):
        try:
                kyc_instance = get_object_or_404(kyc, user=request.user)
                
                # Access the vendor_id field
                vendor_id = kyc_instance.vendor_id
                
                # Log the vendor_id for debugging
                logger.debug(f'Vendor ID: {vendor_id}')

                api_key = 'TEST1019726310159d84051d9684409136279101'
                api_secret = 'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76'
                
                # Example API call using vendor_id (this is just for demonstration)
                headers = {
                    'x-client-id':'TEST1019726310159d84051d9684409136279101',
                    'x-client-secret':'cfsk_ma_test_9f7806b183df0cbedf76e4a00a8bfbff_ff123b76',
                    'x-api-version':'2022-09-01',
                    'Content-Type':'application/json'
                }
                
                response = requests.get(
                    f'https://sandbox.cashfree.com/pg/easy-split/vendors/vendor{vendor_id}',
                    headers=headers,
                    verify=certifi.where()
                )
                response.raise_for_status()  # Raise HTTPError for bad responses
                response_data = response.json()
                print(response_data)
                first_doc_status = response_data['related_docs'][0]['status']
                remarks = response_data['remarks']
                status = response_data['status']


        except:
                response_data = response.json()
                print("this is when vendor is not there")
                print(response_data)
                message = response_data['message']
                messages.success(request, f'{message}')
            
                return redirect('profile')
        
        if request.method == 'POST':
                title = request.POST.get('title')
                description = request.POST.get('description')
                story = request.POST.get('story')
                category = request.POST.get('category')
                end_date = request.POST.get('end_date')
                state = request.POST.get('state')
                files = request.FILES.getlist('file[]')
                media_types = request.POST.getlist('media_type[]')
                goal_amount = request.POST.get('goal_amount')
                address = request.POST.get('address')
                pin_code = request.POST.get('pin_code')
                country = request.POST.get('country')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone_number')
                
                donation_post = Donation.objects.create(
                    user=request.user,
                    title=title,
                    description=description,
                    story=story,
                    category=category,
                    end_date=end_date,
                    state=state,
                    goal_amount=goal_amount,
                    address=address,
                    pin_code=pin_code,
                    country=country,
                    email=email,
                    phone_number=phone_number
                )
                
                for file, media_type in zip(files, media_types):
                    if media_type in ['image', 'video']:
                        Media.objects.create(donation=donation_post, media_type=media_type, file=file)

                messages.success(request, 'Donation post created successfully!')
                return redirect('profile')

        else:
                return render(request, 'donations/donation_form.html', {
                    'donation_post': {
                        'INDIAN_STATES': Donation.INDIAN_STATES,
                        'CATEGORY_CHOICES': Donation.CATEGORY_CHOICES,
                    }
                })