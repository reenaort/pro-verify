from django.contrib import admin
from .models import ProductCode, CodeBatch


@admin.register(CodeBatch)
class CodeBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'total_codes', 'uploaded_codes', 'duplicate_codes', 'invalid_codes', 'uploaded_at')


@admin.register(ProductCode)
class ProductCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'batch', 'is_used', 'verified_at', 'created_at')
    search_fields = ('code',)
    list_filter = ('is_used', 'created_at')