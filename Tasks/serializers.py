from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(seriaizers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Due date must be in the future')
        return value

    def validate(self, attrs #works with a dict of fields):
        instance = getattr(self, 'instance', None)# None is used when creating a new object
        if instance and instance.status == Task.STATUS_COMPLETED
        #ensure only the status aspect is changed only after a completed task
            allowed_keys = {'status'}
            incoming_keys = set(self.initial_data.keys())#using sets to ensure above logic 
            if not incoming_keys.issubset(allowed_keys):
                raise serializers.ValidationError('Completed tasks cannot be edited')
            return attrs


            




