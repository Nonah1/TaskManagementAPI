from rest_framework import serializers
from .models import Task, User, Notification
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):

    #show username
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at', 'owner']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Due date must be in the future')
        return value

#prevents editing of completed tasks uness changing it back to pending
    def validate(self, attrs): #works with a dict of fields
        instance = getattr(self, 'instance', None)# None is used when creating a new object
        if instance and instance.status == Task.STATUS_COMPLETED:
        #ensure only the status aspect is changed only after a completed task
            allowed_keys = {'status'}
            incoming_keys = set(self.initial_data.keys())#using sets for the incoming data 
            if not incoming_keys.issubset(allowed_keys):
                raise serializers.ValidationError('Completed tasks cannot be edited uness reverting to pending.')
            return attrs

#user serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    #hash passwords before saving
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

#notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = '__all__'


        




