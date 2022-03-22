from fastapi import HTTPException

from services.exchange_rate_services import FixerProvider, BanxicoProvider, DofProvider


class ServiceRatesProvider:
    vendor = ''
    valid_service_vendors = ['fixer', 'banxico', 'dof']
    service_vendors_providers = {
        'fixer': FixerProvider(),
        'banxico': BanxicoProvider(),
        'dof': DofProvider(),
    }

    def __init__(self, vendor='fixer'):
        if vendor not in self.valid_service_vendors:
            raise HTTPException(status_code=500, detail="Invalid Service Vendor!")
        self.vendor = vendor

    def dispatch(self):
        return self.service_vendors_providers[self.vendor]
