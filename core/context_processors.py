def site_settings(request):
    ctx = {'SITE_NAME': 'ImmoFacile'}
    if request.user.is_authenticated:
        from messaging.models import Message
        from django.contrib.auth import get_user_model
        User = get_user_model()
        ctx['unread_count'] = Message.objects.filter(
            receiver=request.user, status='sent'
        ).count()
        if request.user.is_staff:
            ctx['pending_agencies_count'] = User.objects.filter(
                role='agency', is_verified=False, is_active=True
            ).count()
    return ctx
