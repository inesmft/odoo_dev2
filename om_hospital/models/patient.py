from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


#class SaleOrderInherit(models.Model):
    # ici on a creer une classe pour que le model order herite le field name
 #   _inherit = 'sale.order'
  #  name = fields.Char(string="Patient Name")


class HospitalPatient(models.Model):
    _name = "hospital.patient"  # nom de la base de données créer en pgadmin est hospital_patient
    _description = "Patient Records"  # quand on fait la recherche en odoo--settings--models et on cherche le model "hospital.patient" on peux voir la description cité ici
    _rec_name = "name"  # pour modifier le nom qui s'affiche en haut pour representer le patient et egalement quand on utilise many2one il prend cette colonne de la table
    #_inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(string="Nom", required=True, track_visibility="always")  # creation du fields qui contiendra le nom, string="nom affiché" requiered true pour que ce champ soit obligatoire en remplissage et tracking pour qu'on aura un affichage a coté pour chaque modification effectué on peux egalement utilisé #tracking=True
    age = fields.Integer(string="Age", tracking=True)
    is_child = fields.Boolean(string="Est ce enfant?", compute="_compute_age", store=True, tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    gender = fields.Selection([("homme", "Homme"), ("femme", "Femme"), ("autre", "Autre")], string="Genre", tracking=True)
    capitalized_name = fields.Char(string="Nom en majuscule", compute="_compute_capitalized_name", store=True)
    ref = fields.Char(string="Reference", copy=False, readonly=True, index=True, default=lambda self: _("New"))
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    my_time_field = fields.Datetime(string='Time')
    appointment_count=fields.Integer(string='count', compute='get_appointment_count')

    # comment creer un smart button :
    # first : on definit la fonction qui a ete mis pour l'action du bouton.
    # ensuite pour compter on ajoute le field count et on lui attribue une fonction compute
    # et on definit la fonction compute qui permet de compter les rdv du patient

    def get_appointment_count(self):
        count = self.env['appointment.patient'].search_count([('name_patient_id', '=', self.id)])
        self.appointment_count= count


    def open_patient_appointments(self):
        return {
            'name' : _('Appointments'),
            'domain' : [('name_patient_id',"=" ,self.id)],
            'view_type': 'form',
            'res_model' : 'appointment.patient',
            'view_id' : False,
            'view_mode' : 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # create function elle est utilisé pour les sequence
    # pour creer une sequence il faut
    # créer le field correspondant
    # ajouter une div dans sheet du form dans patient.xml
    # ajouter un fichier sequence.xml dans data pour creer la sequence et ne pas oublier de l'ajouter dans le manifest
    # creer ensuite la fonction create et l'ajuster selon la sequence
    # ajouter dans le field l'expression default=lambda...
    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code("hospital.patient.sequence") or _("New")
        result = super(HospitalPatient, self).create(vals)
        return result

        # @api.model_create_multi
        #  def create(self, vals_list):
        #     for vals in vals_list:
        #        vals["ref"]=self.env["ir.sequence"].next_by_code("hospital.patient.sequence")
        #   return super(HospitalPatient, self).create(vals_list)


    # constrains function on l'utilise pour afficher des message a l'utilsateur en cas ou il fait entrer un element erronée
    # et pour cela on utilise la fonction ValidationError() alors il faut pas oublier de l'importer en haut a partir de odoo.exception
    @api.constrains("age")
    def _check_age(self):
        for rec in self:
            if rec.age <= 2:
                raise ValidationError(_("you need to enter an age upper than 2 !"))


# @api.constrains('is_child', 'age')
# def _check_age(self):
#   for rec in self:
#      if rec.is_child and rec.age == 0:
#         raise ValidationError(_("entrer l'age !"))

    # pour les compute function :
    # on utilise api.depends et on met comme argument de quoi depend l'element qui va changer (genre ça change selon quoi)
    # ensuite on definis la fonction selon notre besoin, par convetion on la nome _compute_fait_quoi
    # la boucle for rec est utilisé pour pouvoir afficher l'element dans the tree view sans avoir une erreur ( pour moi ça marche meme sans rec mais odoo mates said that :) )
    # et on ajoute un argument dans le field "compute=''" et on met le nom de la fonction a l'interieur
    @api.depends('name')
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.name:
                rec.capitalized_name = rec.name.upper()
            else:
                rec.capitalized_name = ""


    @api.depends("age")
    def _compute_age(self):
        for rec in self:
            if rec.age:
                if rec.age <= 10:
                    rec.is_child = True
                else:
                    rec.is_child = False





# @api.onchange('age')
# def _onchange_age(self):
#     if self.age:
#        if self.age <= 10:
#           self.is_child = True
#      else:
#         self.is_child = False
