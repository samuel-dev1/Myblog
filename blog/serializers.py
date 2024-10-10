from rest_framework import serializers
from .models import UpdatePost, Advertisement, Comment, DailyTask, Profile

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdatePost
        fields = '__all__'  # or specify fields you want to expose

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'  # or specify fields you want to expose
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'  
        
class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
