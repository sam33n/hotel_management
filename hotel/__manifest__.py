# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hotel',
    'version': '1.0',
    'category': 'Hotel',
    'description': """
The module adds the possibility to manage hotels and their customers.
=================================================================================================
""",
    'data': [
        'views/rooms_view.xml',
	'views/rooms_menu.xml',
    'views/reservation_id_view.xml',
    ],
    'depends': ['stock'],
    'installable': True,
    'auto_install': False,
}
