from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from common.models import TimestampedModel

User = get_user_model()


class Profile(TimestampedModel):
    class Gender(models.TextChoices):
        MALE = (
            "Male",
            _("Male"),
        )
        FEMALE = (
            "Female",
            _("Female"),
        )
        OTHER = (
            "Other",
            _("Other"),
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(
        max_length=30, default="+254798355814", verbose_name=_("phone number")
    )
    about_me = models.TextField(
        verbose_name=_("about me"), default="say something about yourself"
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )
    country = CountryField(verbose_name=_("country"), default="KE")
    city = models.CharField(max_length=180, default="Nairobi", verbose_name=_("city"))
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="/profile_default.png"
    )
    x_handle = models.CharField(
        max_length=20, verbose_name=_("x handle"), blank=True, null=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )

    def __str__(self):
        return f"{self.user.first_name}'s Profile"

    def follow(self, profile):
        self.followers.add(profile)

    def unfollow(self, profile):
        self.followers.remove(profile)

    def check_following(self, profile):
        return self.followers.filter(pkid=profile.pkid).exists()
