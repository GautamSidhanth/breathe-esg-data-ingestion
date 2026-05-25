import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Tenant, DataSource
import uuid

def seed():
    tenant, created = Tenant.objects.get_or_create(name='Breathe ESG Demo Client')
    
    DataSource.objects.get_or_create(
        tenant=tenant,
        name='SAP ERP (Procurement)',
        source_type='SAP'
    )
    
    DataSource.objects.get_or_create(
        tenant=tenant,
        name='PG&E Utility Portal',
        source_type='UTILITY'
    )
    
    DataSource.objects.get_or_create(
        tenant=tenant,
        name='Navan Travel Export',
        source_type='TRAVEL'
    )
    print("Database seeded with default tenant and data sources.")

if __name__ == '__main__':
    seed()
