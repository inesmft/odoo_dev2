{
    'name': 'hospital_managment',
    'version': '1.1',
    'summary': 'managment des hopitaux',
    'sequence': 30,
    'description': """
managment hopital
    """,
    'category': 'Extra Tools',
    'website': 'https://www.odoo.com',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
    ],
    'installable': True,
    'application': True,
}
