from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer_group import create_customer_group
from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.lead import create_status
from sri_venkatesa_enterprises.sri_venkatesa_enterprises.utils.employee import employee_custom_fields


def after_install():
    create_customer_group()
    create_status()
    employee_custom_fields()

