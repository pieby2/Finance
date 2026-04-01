from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomUser, Record
from .serializers import UserSerializer, RecordSerializer
from .permissions import IsAdminUser, CanManageRecords
from .filters import RecordFilter


# these views just render the HTML pages
def login_page(request):
    return render(request, 'api/login.html')

def dashboard_page(request):
    return render(request, 'api/dashboard.html')

def records_page(request):
    return render(request, 'api/records.html')

def users_page(request):
    return render(request, 'api/users.html')


# --- API Views below ---

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # only admins can manage users


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all().order_by('-date')
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated, CanManageRecords]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecordFilter

    def perform_create(self, serializer):
        # save who created this record
        serializer.save(created_by=self.request.user)


class DashboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = Record.objects.all()

        total_income = records.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = records.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
        net_balance = total_income - total_expenses

        # group records by category and sum amounts
        category_totals = list(
            records.values('category')
                   .annotate(total=Sum('amount'))
                   .order_by('-total')
        )

        # monthly breakdown - group by month and transaction type
        monthly_trends = list(
            records.annotate(month=TruncMonth('date'))
                   .values('month', 'transaction_type')
                   .annotate(total=Sum('amount'))
                   .order_by('month')
        )

        data = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'category_totals': category_totals,
            'monthly_trends': monthly_trends,
        }

        # viewers shouldn't see individual transaction details
        if request.user.role == 'VIEWER':
            data['recent_activity'] = 'Not available for your role.'
        else:
            recent = records.order_by('-date', '-created_at')[:5]
            data['recent_activity'] = RecordSerializer(recent, many=True).data

        return Response(data)
