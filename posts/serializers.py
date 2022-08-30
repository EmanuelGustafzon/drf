from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.Profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.Profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger then 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger then 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger then 4096px'
            )

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'title',
            'content', 'image', 'image_filter', 'is_owner'
        ]