from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Tenant, DataSource, DataUpload, ActivityData
from .serializers import TenantSerializer, DataSourceSerializer, DataUploadSerializer, ActivityDataSerializer
import csv
import codecs
import json
from datetime import datetime

def parse_date(date_str, source_type):
    if not date_str:
        return None
        
    formats = []
    if source_type == 'SAP':
        formats = ['%d.%m.%Y', '%Y-%m-%d']
    elif source_type == 'UTILITY':
        formats = ['%m/%d/%Y', '%Y-%m-%d']
    elif source_type == 'TRAVEL':
        formats = ['%Y-%m-%d']

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Invalid date format: {date_str}")

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

class ActivityDataViewSet(viewsets.ModelViewSet):
    queryset = ActivityData.objects.all()
    serializer_class = ActivityDataSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'APPROVED'
        instance.save()
        return Response(self.get_serializer(instance).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        instance = self.get_object()
        instance.status = 'REJECTED'
        instance.save()
        return Response(self.get_serializer(instance).data)

class DataUploadViewSet(viewsets.ModelViewSet):
    queryset = DataUpload.objects.all()
    serializer_class = DataUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        source_id = request.data.get('data_source_id')

        if not file or not source_id:
            return Response({'error': 'Missing file or data_source_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source = DataSource.objects.get(id=source_id)
        except DataSource.DoesNotExist:
            return Response({'error': 'Invalid data_source_id'}, status=status.HTTP_400_BAD_REQUEST)

        upload = DataUpload.objects.create(
            data_source=source,
            filename=file.name,
            status='PENDING'
        )

        try:
            reader = csv.DictReader(codecs.iterdecode(file, 'utf-8-sig'))
            import hashlib
            row_number = 1
            for row in reader:
                row_number += 1
                errors = []
                # Simple normalization based on source type
                if source.source_type == 'SAP':
                    activity_type = 'Procurement/Fuel'
                    scope = 'SCOPE_1'
                    try:
                        qty = float(row.get('MENGE', row.get('Quantity', 0)))
                        unit = row.get('MEINS', row.get('Unit', 'UNKNOWN'))
                        d_str = row.get('AEDAT', row.get('Date', ''))
                        date_start = parse_date(d_str, source.source_type)
                    except Exception as e:
                        qty, unit, date_start = 0, 'UNKNOWN', None
                        errors.append(str(e))
                
                elif source.source_type == 'UTILITY':
                    activity_type = 'Electricity'
                    scope = 'SCOPE_2'
                    try:
                        qty = float(row.get('Usage', 0))
                        unit = row.get('Usage_Unit', 'kWh')
                        s_str = row.get('Start_Date', '')
                        date_start = parse_date(s_str, source.source_type)
                        e_str = row.get('End_Date', '')
                        date_end = parse_date(e_str, source.source_type)
                    except Exception as e:
                        qty, unit, date_start, date_end = 0, 'UNKNOWN', None, None
                        errors.append(str(e))

                elif source.source_type == 'TRAVEL':
                    activity_type = 'Business Travel'
                    scope = 'SCOPE_3'
                    try:
                        qty = float(row.get('Distance_km', 0))
                        unit = 'km'
                        d_str = row.get('Date', '')
                        date_start = parse_date(d_str, source.source_type)
                    except Exception as e:
                        qty, unit, date_start = 0, 'UNKNOWN', None
                        errors.append(str(e))
                else:
                    qty, unit, activity_type, scope = 0, 'UNKNOWN', 'Unknown', 'SCOPE_3'

                raw_json_str = json.dumps(row, sort_keys=True)
                dedup_key = hashlib.sha256(f"{source.id}-{raw_json_str}".encode('utf-8')).hexdigest()

                ActivityData.objects.create(
                    tenant=source.tenant,
                    data_upload=upload,
                    scope=scope,
                    activity_type=activity_type,
                    date_start=date_start,
                    date_end=date_start if source.source_type != 'UTILITY' else date_end,
                    normalized_quantity=qty,
                    normalized_unit=unit,
                    source_row_number=row_number,
                    deduplication_key=dedup_key,
                    raw_data=row,
                    status='PENDING_REVIEW',
                    validation_errors=errors if errors else None
                )

            upload.status = 'PROCESSED'
            upload.save()
            return Response({'status': 'success', 'upload_id': upload.id})
        except Exception as e:
            upload.status = 'FAILED'
            upload.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
