import requests
import logging
import certifi
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import CreateView
#login required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ProfilePersonal, kyc
from .forms import UserUpdateForm,UserCreationForm,ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.messages import get_messages
from .models import Userdefine,NGOdetail,Causes
from django.views.generic import DetailView


# Configure logging
logger = logging.getLogger(__name__)
def ngo_list(request):
    ngos = NGOdetail.objects.filter(user__userdefine__category='ngo')
    context = {
        'ngos': ngos
    }
    return render(request, 'users/ngo_list.html', context)

@login_required
def Userdefine_view(request):
    user=request.user
    userdefine_instance, created = Userdefine.objects.get_or_create(user=user)
    if userdefine_instance.first_time_login == True :
        if request.method == 'POST':
            category = request.POST.get('category')
            if category:
                userdefine_instance.category = category
                userdefine_instance.first_time_login = False
                userdefine_instance.save()
                return redirect('profile')
        return render(request, 'users/first_time_login.html')
    else:
        return redirect('profile')

@login_required
def profile(request):
    
    user_profile, created = ProfilePersonal.objects.get_or_create(user=request.user)
    user_kyc, created = kyc.objects.get_or_create(user=request.user)
    user_ngodetail, created = NGOdetail.objects.get_or_create(user=request.user)
    causes = Causes.objects.all()
    selected_causes = user_ngodetail.causes.all()

    userdefine_instances = Userdefine.objects.filter(user=request.user)
    print("Number of instances:", userdefine_instances.count())
    for userdefine_instance in userdefine_instances:
        print("Instance:", userdefine_instance)
 
    #add create vendor api and update api here!! with if comditions and also a check status button to check the kyc verifiaction process
    storage = get_messages(request)
    messages_list = list(storage)  # Convert the storage to a list
    global message
    if messages_list:  # Check if there's any message
        message = messages_list[0]  # Get the first (and only) message
        print(message)
        message_content = message.message  # Access the message content

    if request.method == 'POST':
                #user details
                full_name = request.POST.get('full_name')
                phone_number = request.POST.get('phone_number')
                address = request.POST.get('address')
                pin_code = request.POST.get('pin_code')
                country = request.POST.get('country')
                state = request.POST.get('state')
                profile_pic = request.FILES.get('profile_pic')

                #NGO details
                ngo_logo = request.FILES.get('logo')
                ngo_name = request.POST.get('ngo_name')
                ngo_phone_number = request.POST.get('ngo_phone_number')
                ngo_email = request.POST.get('ngo_email')
                ngo_website = request.POST.get('ngo_website')
                ngo_address = request.POST.get('ngo_address')
                ngo_pin_code = request.POST.get('ngo_pin_code')
                ngo_country = request.POST.get('ngo_country')
                ngo_state = request.POST.get('ngo_state')
                ngo_founded_year = request.POST.get('ngo_founded_year')
                
                causes_ids = request.POST.getlist('causes')
                print("POST data:", request.POST)  # Debugging statement to print POST data
                print("Selected cause IDs:", causes_ids)  # Debugging statement to print selected cause IDs

                facebook_url = request.POST.get('facebook_url')
                twitter_url = request.POST.get('twitter_url')
                instagram_url = request.POST.get('instagram_url')
                youtube_url = request.POST.get('youtube_url')
                ngo_files = request.FILES.get('NGO_files')
                mission_statement = request.POST.get('mission_statement') 

                     
                bank_full_name = request.POST.get('bank_full_name')
                account_type = request.POST.get('account_type')
                business_type = request.POST.get('business_type')
                pan_number = request.POST.get('pan_number')
                gst_number = request.POST.get('gst_number')

                bank_account_number = request.POST.get('bank_account_number')
                ifsc_code = request.POST.get('ifsc_code')

                if userdefine_instance.category == 'user' :
                    user_profile.full_name = full_name
                    user_profile.phone_number = phone_number
                    user_profile.address = address
                    user_profile.pin_code = pin_code
                    user_profile.country = country
                    user_profile.state = state
                    if profile_pic:
                        user_profile.profile_pic = profile_pic
                elif userdefine_instance.category == 'ngo':
                    user_profile.full_name = full_name
                    user_ngodetail.NGO_name = ngo_name
                    user_ngodetail.phone_number = ngo_phone_number
                    user_ngodetail.NGO_email = ngo_email
                    user_ngodetail.NGO_website = ngo_website
                    user_ngodetail.NGO_address = ngo_address
                    user_ngodetail.NGO_pin_code = ngo_pin_code
                    user_ngodetail.NGO_country = ngo_country
                    user_ngodetail.NGO_state = ngo_state
                    user_ngodetail.NGO_founded_year = ngo_founded_year
                    user_ngodetail.NGO_files = ngo_files
                    user_ngodetail.facebook_url = facebook_url
                    user_ngodetail.twitter_url = twitter_url
                    user_ngodetail.instagram_url = instagram_url
                    user_ngodetail.youtube_url = youtube_url
                    user_ngodetail.mission_statement = mission_statement

                    if causes:
                        user_ngodetail.causes.add(*causes_ids)
                    if ngo_logo:
                        user_ngodetail.Logo = ngo_logo

                user_kyc.bank_full_name = bank_full_name
                user_kyc.account_type = account_type
                user_kyc.business_type = business_type
                user_kyc.pan_number = pan_number
                user_kyc.gst_number = gst_number
                user_kyc.bank_account_number = bank_account_number
                user_kyc.ifsc_code = ifsc_code
                user_kyc.bank_full_name = bank_full_name

                
                
                try:
                    user_profile.save()
                    user_kyc.save()
                    user_ngodetail.save()
                 
              
                except ValidationError as e:
                    messages.error(request, f'Error updating profile: {e.message}')

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
                            if userdefine_instance.category == 'user' :
                                 phone_number = user_profile.phone_number
                            elif userdefine_instance.category == 'ngo':
                                 phone_number = user_ngodetail.phone_number
                      
                                 
                            payload = {
                                    "vendor_id": f"vendor{vendor_id}",
                                    "status": "ACTIVE",
                                    
                                    "name": f"{user_kyc.bank_full_name}",
                                    "email": f"{request.user.email}",
                                    
                                    "phone": f"{phone_number}",

                                    "verify_account": True,
                                    "dashboard_access": True,
                                    "schedule_option": 2,
                                    "bank": {
                                    "account_number": f"{user_kyc.bank_account_number}",
                                        "account_holder": f"{user_profile.full_name}",
                                        "ifsc": f"{user_kyc.ifsc_code}"
                                    },
                                    "kyc_details": {
                                        "account_type": f"{user_kyc.account_type}",
                                        "business_type": f"{user_kyc.business_type}",
                                        "uidai": "",
                                        "gst": f"{user_kyc.gst_number}",
                                        "cin": "",
                                        "pan": f"{user_kyc.pan_number}",
                                        "passport_number": ""
                                    }
                                }
                            response = requests.post(
                                'https://sandbox.cashfree.com/pg/easy-split/vendors',
                                json=payload,
                                headers=headers,
                                verify=certifi.where()
                            )
                            response.raise_for_status()  # Raise HTTPError for bad responses
                            response_data = response.json()
                            print(payload)
                            print(response_data)
                            messages.success(request,f"{response_data['status']}")
                            return redirect('profile')
                    # we can write updating kyc api in our except block only!!!
                except:
                            response_data = response.json()
                            print("this is when vendor is not there")
                            print(response_data)
                            

                                   
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
                                payload = {
                                        "vendor_id": f"vendor{vendor_id}",
                                        "status": "",
                                        "name": f"{user_profile.full_name}",
                                        "email": f"{request.user.email}",
                                        "phone": f"{user_profile.phone_number}",
                                        "verify_account": True,
                                        "dashboard_access": True,
                                        "schedule_option": 2,
                                        "bank": {
                                        "account_number": f"{user_kyc.bank_account_number}",
                                            "account_holder": f"{user_profile.full_name}",
                                            "ifsc": f"{user_kyc.ifsc_code}"
                                        },
                                        "kyc_details": {
                                            "account_type": f"{user_kyc.account_type}",
                                            "business_type": f"{user_kyc.business_type}",
                                            "uidai": "",
                                            "gst": f"{user_kyc.gst_number}",
                                            "cin": "",
                                            "pan": f"{user_kyc.pan_number}",
                                            "passport_number": ""
                                        }
                                    }
                                response = requests.patch(
                                    f'https://sandbox.cashfree.com/pg/easy-split/vendors/vendor{vendor_id}',
                                    json=payload,
                                    headers=headers,
                                    verify=certifi.where()
                                )
                                response.raise_for_status()  # Raise HTTPError for bad responses
                                response_data = response.json()
                                print(payload)
                                messages.success(request,"KYC updated successfully")
                                print(response_data)
                                return redirect('profile')
                    # we can write updating kyc api in our except block only!!!
                            except:
                                        response_data = response.json()
                                        print("this is when vendor is not there")
                                        print(payload)
                                        print(response_data)
                                        messages.success(request,"KYC update Unsuccessfully")
                                        return redirect('profile')
                            return redirect('profile')
                

    return render(request,'users/profile.html',{'profile': user_profile , 'kyc':user_kyc, 'userdefine':userdefine_instance,'ngodetail':user_ngodetail,'causes':causes,'selected_causes':selected_causes,})
                

def kycverify(request , pk):
    return render(request,'users/kyc_verify_status.html')




