from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError

class Appointment(models.Model):
    _name = "appointment.patient"  # nom de la base de données créer en pgadmin est hospital_patient
    _description = "Appointment for patients"  # quand on fait la recherche en odoo--settings--models et on cherche le model "hospital.patient" on peux voir la description cité ici
    _rec_name = "reference"  # pour modifier le nom qui s'affiche en haut pour representer le patient
   # _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_rdv desc" #on utilise ceci pour ordonner les rendez vous par exemple quand on met id ils sont ordonnée par leur id quand on met nom du field (ex date_rdv) ils sont ordonnée par les dates de leur rendez-vous

    def _get_default_note(self):
        return "message"

    #name_patient = fields.Char(string="Nom", required=True, track_visibility="always")  # creation du fields qui contiendra le nom, string="nom affiché" requiered true pour que ce champ soit obligatoire en remplissage et tracking pour qu'on aura un affichage a coté pour chaque modification effectué on peux egalement utilisé #tracking=True
    name_patient_id = fields.Many2one('hospital.patient', string='Nom', ) # many2one consiste a donner l'acces au utilisateur de prendre un rendez vous en lui affichant les patients qui existe dans la base de donées et ceci ce fait en ajoutant le nom de la class a qui il doit avoir accés
                                                                        # si on met cet fonction dans many2one default=_get_default_note et on la fonction return par exemple 9, ce 9 est l'id qui se trouve dans "view datameta" dans n'importe quel patient qu'on veux le mettre par defaut dans ce champs ( 9=enfant)
    age_patient = fields.Integer(string="Age", tracking=True, related='name_patient_id.age') # related permet de lier de field, le premier prend ses valeur d'une autre table et le 2eme il doit s'adapter au choix du user, s'il choisit ines il doit automatiquement mettre 22 par exemple
                                                                                             # la syntaxe est : related="(field ou l'utilisateur choisit).(field ou il recupere l'information voulu, le nom du field dans la table)"
    reference = fields.Char(string="Reference", copy=False, readonly=True, index=True, default=lambda self: _("New"))
    note=fields.Text(string="note", default=_get_default_note)
    date_rdv = fields.Date(string="Date")
    state= fields.Selection([
        ('brouillon','Brouillon'),
        ('confirmer', 'Confirmer'),
        ("valider", "Valider"),
        ('annuler', 'Annuler'),
    ], string="status", readonly=True, default='brouillon')

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code("appointment.sequence") or _("New")
        result = super(Appointment, self).create(vals)
        return result
