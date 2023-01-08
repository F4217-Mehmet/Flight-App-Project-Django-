from django.contrib.auth.models import User         # register olduğumuzda User tablosunda create ediliyor.
from django.db.models.signals import post_save      # user create edildiğinde signali gönder (post_save)
from django.dispatch import receiver                # signali receiver ile yakalıyoruz
from rest_framework.authtoken.models import Token   # tokeni create edeceğimiz token tablomuz

@receiver(post_save, sender=User)   # post_save, olay gerçekleştikten sonra demektir. (Burada user send edildikten sonra diyoruz.) bunun pre_save versiyonu da var. ama genelde post kullanılır.
def create_Token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)