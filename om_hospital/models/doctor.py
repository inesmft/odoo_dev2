from odoo import api, fields, models, _
#from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name="hospital.doctor"
    _description="doctor record"
    #_inherit="mail.thread"
    _rec_name='ref'

    name=fields.Char(string="Nom", required=True, tracking=True)
    gender=fields.Selection([("homme","Homme"),("femme","Femme"),("autre","Autre")], string="genre", tracking=True)
    ref=fields.Char(string="Reference")
    active= fields.Boolean(default=True)

    def name_get(self):
        res=[]
        for rec in self :
            name=f'{rec.ref}-{rec.name}'
            res.append((rec.id, name))
        return res