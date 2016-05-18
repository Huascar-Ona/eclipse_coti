# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv

class papel(models.Model):
    _name = "eclipse.cotizacion.papel"

    clasificacion = fields.Char("Clasificación", required=True)
    tipo = fields.Char("Tipo", required=True)
    gramaje = fields.Integer("Gramaje", required=True)

    def name_get(self, cr, uid, ids, context=None):
        names = []
        for rec in self.browse(cr, uid, ids):
            name = rec.clasificacion + " " + rec.tipo + " " + rec.gramaje
            names.append((rec.id, name))
        return names

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100):
        if not args:
            args = []

        ids = []
        ids2 =[]
        ids = self.search(cr, user, [('clasificacion', 'ilike', name)] + args, limit=limit, context=context)
        ids2 = self.search(cr, user, [('tipo', 'ilike', name)] + args, limit=limit, context=context)
        ids += ids2

        recs = self.name_get(cr, user, ids, context)
        return sorted(recs, key=lambda (id, name): ids.index(id))
