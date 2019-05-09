# -*- coding: utf-8 -*-
{
    'name': "seprate_stock_operation",

    'summary': """
        seprate_stock_operation""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techhive",
    'website': "http://www.techhivesolutions.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
	
        'report/report_stockpicking_operations_2.xml',

		
        'security/ir.model.access.csv',
        'views/internal_transfer.xml',
        'views/delivery_order.xml',
        'views/receipt.xml',
        'views/brand.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}