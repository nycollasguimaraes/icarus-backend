from rest_framework import serializers
from .models import User, Project, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'nusp', 'role', 'course', 'ideal_period', 'faculty',
        'department', 'curriculum_base64', 'curriculum_filename', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    # Mapear 'first_name' do Django para 'name' do frontend
    name = serializers.CharField(source='first_name')
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    professorId = serializers.IntegerField(source='professor.id', read_only=True)
    # Convert list to string and back for keywords
    keywords = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    def get_keywords(self, obj):
        return [k.strip() for k in obj.keywords.split(',')]

class ApplicationSerializer(serializers.ModelSerializer):
    studentId = serializers.IntegerField(source='student.id', read_only=True)
    professorId = serializers.IntegerField(source='professor.id', read_only=True)
    projectId = serializers.IntegerField(source='project.id', read_only=True)
    class Meta:
        model = Application
        fields = '__all__'
