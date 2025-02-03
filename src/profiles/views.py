from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from common.exceptions import CantFollowYourself
from common.views import GenericModelViewSet

from .models import Profile
from .serializers import (FollowingSerializer, ProfileSerializer,
                          ProfileUpdateSerializer)

User = get_user_model()


class ProfileView(GenericModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "id"
    action_serializers = {
        "list": ProfileSerializer,
        "retrieve": ProfileSerializer,
        "update": ProfileUpdateSerializer,
        "partial_update": ProfileUpdateSerializer,
    }
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.select_related("user")

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
    )
    def me_view(self, request, pk=None):
        user = request.user.profile
        serializer = ProfileSerializer(user)
        res = {
            "message": "profile retrieved successfully",
            "data": serializer.data,
        }
        return Response(data=res, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        url_path="followers",
    )
    def followers_view(self, request, pk=None):
        try:
            profile = Profile.objects.get(user=request.user)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            res = {
                "message": "Followers retrieved successfully",
                "data": {
                    "followers_count": follower_profiles.count(),
                    "followers": serializer.data,
                },
            }
            return Response(res, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Resource Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        methods=["get"],
        detail=False,
        url_path="^(?P<profile_id>[^/.]+)/follow",
    )
    def follow_view(self, request, profile_id, pk=None):
        try:
            me = request.user.profile
            profile = Profile.objects.get(id=profile_id)

            if profile == me:
                raise CantFollowYourself()

            if me.check_following(profile):
                res = {
                    "status": "error",
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_login}",
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            me.follow(profile)
            subject = "A New User Follows You :)"
            message = f"Hi there, {profile.user.first_name}!!, the user {request.user.first_name} {request.user.last_name} now follows you"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            res = {
                "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
            }
            return Response(res, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile Resource Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        methods=["get"],
        detail=False,
        url_path="^(?P<profile_id>[^/.]+)/unfollow",
    )
    def unfollow_view(self, request, profile_id, pk=None):
        try:
            me = request.user.profile
            profile = Profile.objects.get(id=profile_id)

            if not me.check_following(profile):
                res = {
                    "message": f"You can't unfollow {profile.user.first_name} {profile.user.last_name}, since you were not following them in the first place",
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            me.unfollow(profile)
            res = {
                "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
            }
            return Response(res, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile Resource Not Found"},
                status=status.HTTP_404_NOT_FOUND,
            )
