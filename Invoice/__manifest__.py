# -*- coding: utf-8 -*-
{
    'name': "Custom Invoice Module",

    'summary': """
        Module to generate invoices""",

    'description': """
        Module to generate receipts
    """,

    'author': "Techhive",
    'website': "http://www.techhivesolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Custom Invoice Module',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
	
    # always loaded
    'data': [

        'views/Invoice.xml',
        'views/customer.xml',
        'views/company.xml',
        'views/CashMemo_View.xml',
        'views/WithoutDc_View.xml',
        'views/Salestax_View.xml',
        'views/allinvoice.xml',
        'views/ProductForm.xml',
        'views/CreditSaleVoucher_view.xml',
        'reports/All_reports.xml',
        'reports/pdf_report.xml',
        # 'reports/salestax_report.xml',
        # 'reports/withoutdc_report.xml',
        'views/DC_view.xml',
        #'views/commercialinvoicewithdc_view.xml',
        'views/CreditSaleVoucher_view.xml',
        # 'reports/creditsalevoucher_report.xml',
        # 'reports/DC_report.xml',
        #'reports/withdc_report.xml'
        # 'views/cashMemo.xml',
        # 'views/cash_memo_report.xml'

    ]

}
