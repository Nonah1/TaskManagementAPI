from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, User, Notification
from rest_framework.decorators import action
from .serializers import TaskSerializer, UserSerializer, NotificationSerializer


# Create your views here.


#task viewset
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # each user only sees their task
    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')
        due_date_param = self.request.query_params.get('due_date')

        #filtering
        if status_param:
            queryset = queryset.filter(status=status_param)
        if priority_param:
            queryset = queryset.filter(priority=priority_param)
        if due_date_param:
            queryset = queryset.filter(due_date__date=due_date_param)

        return queryset

    #assign the logged-in user as task owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    #mark as complete
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.STATUS_COMPLETED:
            return Response({'detail': 'Task already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = Task.STATUS_COMPLETED
        task.completed_at = timezone.now()
        task.save()
        return Response(self.get_serializer(task).data)

    #mark as incomplete
    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.STATUS_PENDING:
            return Response({'detail': 'Task is already pending.'}, status=status.HTTP_400_BAD_REQUEST)
        task.status = Task.STATUS_PENDING
        task.completed_at = None
        task.save()
        return Response(self.get_serializer(task).data)


#userviewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  #anyone can register



#notification viewset
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show notifications for the logged-in user
        return Notification.objects.filter(user=self.request.user)

    #mark notification as read
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'})

