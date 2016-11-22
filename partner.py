# -*- coding: utf-8 -*-
from openerp import fields,api,models

class res_partner(models.Model):
    _inherit = "res.partner"

    condiciones = fields.Char("Condiciones comerciales")
