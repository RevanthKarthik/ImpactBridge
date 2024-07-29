from django.db import models
from django.contrib.auth.models import User
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase,ItemBase

class Userdefine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('user', 'User'),
        ('ngo', 'NGO'),
        # Add other categories as needed
    ]

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='User',
        null=True,
    )
    first_time_login = models.BooleanField(
        default=True,
        null=True,
    )

class ProfilePersonal(models.Model):

    INDIAN_STATES = [
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CG', 'Chhattisgarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PY', 'Puducherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    full_name = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=200)
    pin_code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^[1-9][0-9]{2}\s{0,1}[0-9]{3}$", "Invalid PIN code format")],
    )
    country = models.CharField(max_length=2, choices=[('IN', 'India')], default='IN')
    state = models.CharField(max_length=2, choices=INDIAN_STATES, default='TS')
   




    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Phone number validation logic
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(self.phone_number, "IN")
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number format")
            except phonenumbers.NumberParseException:
                raise ValidationError("Invalid phone number format")
            
        self.vendor_id = self.user.pk

        super().save(*args, **kwargs)

        # Image resizing logic
        if self.profile_pic:
            try:
                img = Image.open(self.profile_pic.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.profile_pic.path)
            except OSError:
                pass

class kyc(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('business','Business Account'),
        ('individual','Individual'),
    ]
    BUSINESS_TYPE_CHOICES = [
    ('B2B', 'B2B'),
    ('Digital Goods', 'Digital Goods'),
    ('E-commerce', 'E-commerce'),
    ('Education', 'Education'),
    ('Financial Services', 'Financial Services'),
    ('Food and Beverages', 'Food and Beverages'),
    ('Gaming', 'Gaming'),
    ('Government', 'Government'),
    ('Grocery', 'Grocery'),
    ('Health care', 'Health care'),
    ('Insurance', 'Insurance'),
    ('Jewellery', 'Jewellery'),
    ('NBFCs/Organizations into Lending', 'NBFCs/Organizations into Lending'),
    ('Logistics', 'Logistics'),
    ('Miscellaneous', 'Miscellaneous'),
    ('Mutual funds/Broking', 'Mutual funds/Broking'),
    ('Non Profit/NGO', 'Non Profit/NGO'),
    ('Online Gaming', 'Online Gaming'),
    ('Open and Semi Open Wallet', 'Open and Semi Open Wallet'),
    ('Pan shop', 'Pan shop'),
    ('Pharmacy', 'Pharmacy'),
    ('Readymade', 'Readymade'),
    ('Real Estate, Housing, Rentals', 'Real Estate, Housing, Rentals'),
    ('Retail and Shopping', 'Retail and Shopping'),
    ('SaaS', 'SaaS'),
    ('Social Media and Entertainment', 'Social Media and Entertainment'),
    ('Society/Trust/Club/Association', 'Society/Trust/Club/Association'),
    ('Telecom', 'Telecom'),
    ('Travel and Hospitality', 'Travel and Hospitality'),
    ('Utilities', 'Utilities'),
    ('Chit Funds', 'Chit Funds'),
    ('Web host/Domain seller', 'Web host/Domain seller'),
    ('Professional Services', 'Professional Services (Doctors, Lawyers, Architects, CAs, and other Professionals)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor_id = models.IntegerField(editable=False)  # New field to store user.pk
    bank_full_name = models.CharField(max_length=100,null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, null=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, null=True)
    pan_number = models.CharField(max_length=10, validators=[RegexValidator(r'^[A-Z]{5}[0-9]{4}[A-Z]$', 'Invalid PAN number format')], unique=True, null=True)
    gst_number = models.CharField(max_length=15, validators=[RegexValidator(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', 'Invalid GST number format')], unique=True, null=True)
    bank_account_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{9,18}$', 'Invalid account number format')],null=True)
    ifsc_code = models.CharField(max_length=11, validators=[RegexValidator(r'^[A-Z]{4}0[A-Z0-9]{6}$', 'Invalid IFSC code format')],null=True)





    def __str__(self): 
        return f'{self.user.username} kyc details'
    
    def save(self, *args, **kwargs):
        self.vendor_id = self.user.pk
        
        super().save(*args, **kwargs)

    
class Causes(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NGOdetail(models.Model):
    INDIAN_STATES = [
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CG', 'Chhattisgarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PY', 'Puducherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    causes = models.ManyToManyField(Causes, related_name='ngos')

    Logo = models.ImageField(upload_to='profile_pics', null=True)
    NGO_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    NGO_email = models.EmailField(null=True)
    NGO_website = models.URLField(null=True)
    NGO_address = models.CharField(max_length=200, null=True)
    NGO_pin_code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^[1-9][0-9]{2}\s{0,1}[0-9]{3}$", "Invalid PIN code format")],
        null=True,
    )
    NGO_country = models.CharField(max_length=2, choices=[('IN', 'India')], default='IN', null=True)
    NGO_state = models.CharField(max_length=2, choices=INDIAN_STATES, default='TS', null=True)
    NGO_founded_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2999)], blank=True,null=True)
  
    NGO_files = models.FileField(upload_to='media/', null=True, blank=True)  # Allowing null and blank for optional media files
    NGO_verified = models.BooleanField(default=False)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    mission_statement = models.TextField(null=True)

    def __str__(self): 
        return f'{self.user.username} Ngo details'
    
    def save(self, *args, **kwargs):
        # Resize image if Logo is provided
        if self.Logo:
            self.resize_image(self.Logo, (300, 300))  # Resize to max 300x300

        super().save(*args, **kwargs)

    def resize_image(self, image_field, size):
        """
        Resizes the given image field to the specified size.
        """
        img = Image.open(image_field.path)
        img.thumbnail(size)
        img.save(image_field.path)