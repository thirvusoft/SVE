from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer_group import create_customer_group
from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.lead import create_status


def after_install():
    create_customer_group()
    create_status()

