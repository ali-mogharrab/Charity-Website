from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        benefactor = BenefactorSerializer(data=request.data)
        if benefactor.is_valid():
            benefactor.save(user=request.user)
            return Response({'message': 'User was registered successfully!'})
        
        return Response({'message': benefactor.errors})


class CharityRegistration(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        charity = CharitySerializer(data=request.data)
        if charity.is_valid():
            charity.save(user=request.user)
            return Response({'message': 'User was registered successfully!'})

        return Response({'message': charity.errors})


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = (IsBenefactor, )

    def get(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
        except Task.DoesNotExist:
            return task
        
        if task.state != 'P':
            return Response(data={'detail': 'This task is not pending.'}, status=404)
        else:
            task.state = 'W'
            task.assigned_benefactor = request.user.benefactor
            task.save()
            return Response(data={'detail': 'Request sent.'}, status=200)


class TaskResponse(APIView):
    permission_classes = (IsCharityOwner, )

    def post(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
        except Task.DoesNotExist:
            return task

        response = request.data['response']
        if response != 'A' and response != 'R':
            return Response(data={'detail': 'Required field ("A" for accepted / "R" for rejected)'}, status=400)

        if task.state != 'W':
            return Response(data={'detail': 'This task is not waiting.'}, status=404)

        if response == 'A':
            task.state = 'A'
            task.save()
            return Response(data={'detail': 'Response sent.'}, status=200)

        if response == 'R':
            task.state = 'P'
            task.assigned_benefactor = None
            task.save()
            return Response(data={'detail': 'Response sent.'}, status=200)


class DoneTask(APIView):
    parser_classes = (IsCharityOwner, )
    
    def post(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
        except Task.DoesNotExist:
            return task

        if task.state != 'A':
            return Response(data={'detail': 'Task is not assigned yet.'}, status=404)

        task.state = 'D'
        task.save()
        return Response(data={'detail': 'Task has been done successfully.'}, status=200)
