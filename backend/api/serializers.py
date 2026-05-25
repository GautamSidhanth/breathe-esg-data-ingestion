from rest_framework import serializers
from .models import Tenant, DataSource, DataUpload, ActivityData

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'

class DataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataUpload
        fields = '__all__'

class ActivityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityData
        fields = '__all__'
