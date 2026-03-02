from rest_framework import serializers
from review.models import Review
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
# 12.5
    user_data = serializers.SerializerMethodField()
# 12.5
    class Meta:
        model = Review
        fields = '__all__'

        read_only_fields = ['user', 'user_data']
# 12.5
    def get_user_data(self, obj):
        user_data = User.objects.get(id=obj.user.id)
        return {
            'last_name': user_data.last_name,
            'first_name': user_data.first_name
        }
# 12.5