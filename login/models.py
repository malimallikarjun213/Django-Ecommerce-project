
from django.conf import settings
from django.db import models


class NotificationPreference(models.Model):
    # Each user gets one notification preference record.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
    )

    # Notification categories
    order_updates = models.BooleanField(default=True)
    offers_deals = models.BooleanField(default=True)
    wishlist_alerts = models.BooleanField(default=True)
    personalized_recommendations = models.BooleanField(default=True)
    security_alerts = models.BooleanField(default=True)

    # Delivery methods
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user}"
