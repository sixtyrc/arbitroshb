import json
from pywebpush import webpush, WebPushException
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Designacion, PushSubscription
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Designacion)
def notificar_designacion(sender, instance, created, **kwargs):
    if created:
        # 1. Notificación por Email (Resend)
        subject = f'📍 Nueva Designación: {instance.partido.title}'
        message = f'Hola {instance.arbitro.user.first_name}, fuiste designado como {instance.get_rol_asignado_display()} para el partido en {instance.partido.location} el {instance.partido.date_time}.'
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.arbitro.user.email],
                fail_silently=False,
            )
            print(f"Email enviado a {instance.arbitro.user.email}")
        except Exception as e:
            print(f"Error enviando email: {e}")

        # 2. Notificación Push
        try:
            push_sub = PushSubscription.objects.get(user=instance.arbitro.user)
            sub_info = {
                "endpoint": push_sub.endpoint,
                "keys": {
                    "auth": push_sub.auth,
                    "p256dh": push_sub.p256dh
                }
            }
            data = json.dumps({
                "title": "📍 Nueva Designación",
                "body": f"Partido: {instance.partido.title}",
                "url": "/"
            })
            webpush(
                subscription_info=sub_info,
                data=data,
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={"sub": f"mailto:{settings.VAPID_ADMIN_EMAIL}"}
            )
            print(f"Push enviado a {instance.arbitro.user.username}")
        except PushSubscription.DoesNotExist:
            print(f"El usuario {instance.arbitro.user.username} no tiene suscripción push.")
        except WebPushException as ex:
            print(f"Error enviando Web Push a {instance.arbitro.user.username}: {repr(ex)}")
        except Exception as e:
            print(f"Error general Push: {e}")
