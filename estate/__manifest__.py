{
    'name': 'estate',
    'version': '0.1',
    'summary': '',
    'category': 'Real Estate/Brokerage',
    'depends': ['base'],
    'author': 'Mauricio Aponte',
    'installable': True,
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ] 
}