from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Project, Application
from .serializers import UserSerializer, ProjectSerializer, ApplicationSerializer


# -------------------------
# User ViewSet
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -------------------------
# Project ViewSet
# -------------------------
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Convert array of keywords ["AI", "DSP"] → "AI,DSP"
        if 'keywords' in data and isinstance(data['keywords'], list):
            data['keywords'] = ",".join(data['keywords'])

        # For migration simplicity, trust professorId sent by frontend
        professor_id = data.get('professorId')
        data['professor'] = professor_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------
# Application ViewSet
# -------------------------
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        data['student'] = data.get('studentId')
        data['project'] = data.get('projectId')
        data['professor'] = data.get('professorId')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------
# Simple Login (not JWT)
# -------------------------
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)

        if user.check_password(password):
            return Response(UserSerializer(user).data)
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
