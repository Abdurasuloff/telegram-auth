1. Birinchi o'rinda  foydalanuvchilar login qilda bo'ladigan eng sodda websaytni tuzib olamiz.

2. Telegram bot ochish

3. Ngrok serverini yoqamiz.

4. Shu server urlini botimizga botfatherdagi /setdomain buyrug'i orqali biriktiramiz.

5. pip install social-auth-app-django==5.0.0 deb ushbu paketni o'rnatamiz. Eslatma!! bu paketni shu versiyasi djangoni 4 versiyasida ishlamaydi.

6. installed apps listiga  "social_django" ni qo'shib qo'yoqamiz

7. authenticate sozlamarini sozlaymiz:
AUTHENTICATION_BACKENDS = (
    'social_core.backends.telegram.TelegramAuth',
    'django.contrib.auth.backends.ModelBackend',
)

8. 2-qadamda yartilgan bot tokenini ham sozlamalarimizga ham qo'shib qo'yamiz:
SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = "5869794463:AAFVmxkd5Xs2d2HDtKIuG1c2dNLaydPBmNg"

LOGIN_REDIRECT_URL = reverse_lazy('profile')

9. Paketimizni urllarini ham qo'shib qo'yamiz:

path('auth/', include('social_django.urls', namespace='social')),

10. Endi telegram orqali login qilish uchun tugma request jo'natish uchun JS yozishimiz kerak bularni telegramning rasmi sahifasidan olishimiz mumkin:
https://core.telegram.org/widgets/login
<script async src="https://telegram.org/js/telegram-widget.js?21" data-telegram-login="abdurasuloffcodes_bot" data-size="large" data-auth-url="https://c9a3-37-110-211-8.eu.ngrok.io/auth/complete/telegram" data-request-access="write"></script>

11. Olingan user ma'lumotlarini templateda chiqarish
'social_django.context_processors.backends',
'social_django.context_processors.login_redirect',

<h1>Hi, {{ user.first_name }}!</h1>
<p>Meta:</p>

<ul>
    {% for associated in backends.associated %}
        <li>ID: {{ associated.uid }}</li>
        <li>Provider: {{ associated.provider }}</li>
        <li>Extra: {{ associated.extra_data }}</li>
    {% endfor %}
</ul>

12. Telegram akkaunt profil rasmini Saytimizdagi user profiliga saqlash
 
CustomUser tuzish
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile = models.ImageField(upload_to='profile-image/')
    
    def __str__(self):
        return self.username

pip install Pillow

AUTH_USER_MODEL = "users.CustomUser"
media settingslarni to'g'irlash

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.joinpath("media")

urllar esdan chiqmasin

from django.conf import settings
from django.conf.urls.static import static

+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


signal yozamiz

app.py ushbu funksiyani qo'shib ketasiz

   def ready(self):
        import users.signals



from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from users.models import CustomUser


@receiver(post_save,  sender=UserSocialAuth)
def save_profile_photo(sender, instance, created, update_fields,  **kwargs):
    
    if instance.extra_data:
        user = instance.user
        picture = instance.extra_data['photo_url']
        user.profile = picture
        user.save() 
