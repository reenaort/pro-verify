import pandas as pd
from django.shortcuts import render
from django.db.models import Max
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ProductCode, CodeBatch
from .serializers import ProductCodeSerializer, CodeBatchSerializer


class UploadCodesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        file_name = uploaded_file.name
        file_name_lower = file_name.lower()

        try:
            if file_name_lower.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif file_name_lower.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                return Response({"error": "Only CSV and Excel files allowed"}, status=400)

            df.columns = df.columns.str.strip().str.lower()

            if 'code' not in df.columns:
                return Response({"error": "File must contain a column named 'code'"}, status=400)

            batch = CodeBatch.objects.create(file_name=file_name)

            total = 0
            duplicates = 0
            invalid = 0
            codes_to_create = []

            for item in df['code']:
                total += 1
                if pd.isna(item):
                    invalid += 1
                    continue
                code = str(item).strip().upper()
                if len(code) < 4:
                    invalid += 1
                    continue
                if ProductCode.objects.filter(code=code).exists():
                    duplicates += 1
                    continue
                codes_to_create.append(ProductCode(code=code, batch=batch))

            ProductCode.objects.bulk_create(codes_to_create, batch_size=5000)
            uploaded = len(codes_to_create)

            batch.total_codes = total
            batch.uploaded_codes = uploaded
            batch.duplicate_codes = duplicates
            batch.invalid_codes = invalid
            batch.save()

            return Response({
                "message": "File uploaded successfully",
                "batch_id": batch.id,
                "total_codes": total,
                "uploaded_codes": uploaded,
                "duplicate_codes": duplicates,
                "invalid_codes": invalid
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Code is required"}, status=400)

        code = code.strip().upper()

        try:
            product_code = ProductCode.objects.get(code=code)
            if product_code.is_used:
                return Response({
                    "status": "already_verified",
                    "message": "This code has already been verified before",
                    "code": code,
                    "verified_at": product_code.verified_at
                })
            product_code.is_used = True
            product_code.verified_at = timezone.now()
            product_code.save()
            return Response({
                "status": "genuine",
                "message": "This product is genuine",
                "code": code
            })
        except ProductCode.DoesNotExist:
            return Response({
                "status": "invalid",
                "message": "Invalid product code"
            }, status=404)


class ProductCodeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        codes = ProductCode.objects.all().order_by('-created_at')[:100]
        serializer = ProductCodeSerializer(codes, many=True)
        return Response(serializer.data)


class CodeBatchListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        batches = CodeBatch.objects.all().order_by('-uploaded_at')
        serializer = CodeBatchSerializer(batches, many=True)
        return Response(serializer.data)


class DashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_codes = ProductCode.objects.count()
        total_authentications = ProductCode.objects.filter(is_used=True).count()
        total_batches = CodeBatch.objects.count()

        batches = CodeBatch.objects.order_by('-uploaded_at')[:10]
        batches_data = []

        for batch in batches:
            auth_count = ProductCode.objects.filter(batch=batch, is_used=True).count()
            last_auth = ProductCode.objects.filter(
                batch=batch, is_used=True
            ).aggregate(last=Max('verified_at'))['last']

            batches_data.append({
                "id": batch.id,
                "file_name": batch.file_name,
                "uploaded_at": batch.uploaded_at.strftime("%d %b %Y"),
                "uploaded_codes": batch.uploaded_codes or 0,
                "auth_count": auth_count,
                "last_authenticated": last_auth.strftime("%d %b %Y, %H:%M") if last_auth else "—",
            })

        return Response({
            "total_codes": total_codes,
            "total_authentications": total_authentications,
            "total_batches": total_batches,
            "batches": batches_data,
        })


class EmailLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)

        User = get_user_model()
        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            return Response({"error": "Invalid email or password"}, status=401)

        user = authenticate(username=user_obj.username, password=password)

        if user is None:
            return Response({"error": "Invalid email or password"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })


def admin_login_page(request):
    return render(request, "admin-login.html")

def admin_dashboard_page(request):
    return render(request, "admin.html")

def admin_upload_page(request):
    return render(request, "admin-upload.html")

def admin_codes_page(request):
    return render(request, "admin-codes.html")

def admin_details_page(request):
    return render(request, "admin-details.html")

def verify_page(request):
    return render(request, "verify.html")
