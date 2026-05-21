from rest_framework import serializers
from .models import ProductCode, CodeBatch


class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCode
        fields = '__all__'


class CodeBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBatch
        fields = '__all__' 