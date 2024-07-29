from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

class Donation(models.Model):

        CATEGORY_CHOICES = (
        ('medical_emergency', 'Medical_Emergency'),#
        ('healthandwellness', 'Health and Wellness'),#
        ('education', 'Education and Learning'),#
        ('poverty', 'Poverty Alleviation'),#
        ('community', 'Community Development'),#
        ('humanitarian', 'Humanitarian Aid'),#
        ('arts', 'Arts & Culture'),#
        ('women', 'Women Welfare'),#
        ('child', 'Child Welfare'),#
        ('elders', 'Elderly Care'),#
        ('environment', 'Environmental Conservation'),#
        ('hunger', 'Food Security'),#
        ('speciallyabled', 'Specially Abled'),
                            )
        
        PAYMENT_CHOICES = {
        ('upi', 'PhonePe/GooglePay'),
        ('credit/debit_cards', 'Credit or Debit Cards'),
        ('netbanking', 'NetBanking'),
        }

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
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
        description = models.CharField(max_length=300)
        story = models.TextField()
        category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
        date_posted = models.DateTimeField(default=timezone.now)
        end_date = models.DateTimeField(null=True)
        goal_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
        file = models.FileField(upload_to='media/', null=True, blank=True)  # Allowing null and blank for optional media files
        is_approved = models.BooleanField(default=False)
    
        class Meta:
            permissions = [
                ("can_change_is_approved", "Can change the approval status of donations"),
            ]
        #progress
        address = models.CharField(max_length=200,null=True)
        pin_code = models.CharField(
        max_length=6,
        validators=[RegexValidator(r"^[1-9][0-9]{2}\s{0,1}[0-9]{3}$", "Invalid PIN code format")],
        null=True
    )
        country = models.CharField(max_length=2, choices=[('IN', 'India')], default='IN')
        state = models.CharField(max_length=2, choices=INDIAN_STATES, null=True)
        #contactdetails
        phone_number = models.CharField(max_length=10, null=True)
        email = models.EmailField(max_length=255,null=True)
        #author


        def __str__(self):
         return str(self.pk)
class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    donation = models.ForeignKey(Donation, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)

    def __str__(self):
        return f"{self.donation.title} - {self.media_type}"

    def save(self, *args, **kwargs):
        # Save the file first
        super().save(*args, **kwargs)
        
        # Process image files
        if self.media_type == 'image':
            self.process_image()

    def process_image(self):
        img = Image.open(self.file.path)

        # Resize the image
        max_size = (800, 800)
        img.thumbnail(max_size, Image.LANCZOS)

        # Save the image back to the file field
        img_format = img.format
        if not img_format:
            img_format = 'JPEG'  # default to JPEG if format is not recognized
        img_io = BytesIO()
        img.save(img_io, format=img_format, quality=85)
        img_io.seek(0)
        
        # Construct a new name for the image to avoid overwriting the original
        name, ext = os.path.splitext(self.file.name)
        self.file.save(f"{name}_compressed{ext}", ContentFile(img_io.read()), save=False)
        super().save(update_fields=['file'])
    
class Blog(models.Model):
    donation = models.ForeignKey(Donation, related_name='blogs', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now,null=True)
    file = models.FileField(upload_to='media/', null=True, blank=True)  # Allowing null and blank for optional media files


    def __str__(self):
        return self.title



        