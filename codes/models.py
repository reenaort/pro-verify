from django.db import models


class CodeBatch(models.Model):
    file_name = models.CharField(max_length=255)
    total_codes = models.IntegerField(default=0)
    uploaded_codes = models.IntegerField(default=0)
    duplicate_codes = models.IntegerField(default=0)
    invalid_codes = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class ProductCode(models.Model):
    code = models.CharField(max_length=100, unique=True, db_index=True)
    batch = models.ForeignKey(CodeBatch, on_delete=models.CASCADE, related_name='codes')
    is_used = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code