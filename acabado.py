# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.osv import osv

class acabado(models.Model):
    _name = "eclipse.cotizacion.acabado"

    acabado = fields.Char(u"Acabado", required=True)
    tipo = fields.Char(u"Tipo", required=True)
    datos = fields.Many2many("eclipse.cotizacion.acabado.dato", "eclipse_cotizacion_acabado_datos_rel", "id1", "id2", string="Datos")

    def name_get(self, cr, uid, ids, context=None):
        names = []
        for rec in self.browse(cr, uid, ids):
            name = rec.acabado + " " + rec.tipo
            names.append((rec.id, name))
        return names

    def name_search(self, cr, user, name='', args=None, operator='ilike',
                         context=None, limit=100):
        if not args:
            args = []

        ids = []
        ids2 =[]
        ids = self.search(cr, user, [('acabado', 'ilike', name)] + args, limit=limit, context=context)
        ids2 = self.search(cr, user, [('tipo', 'ilike', name)] + args, limit=limit, context=context)
        ids += ids2
        ids = list(set(ids))

        recs = self.name_get(cr, user, ids, context)
        return sorted(recs, key=lambda (id, name): ids.index(id))

class acabado_dato(models.Model):
    _name = "eclipse.cotizacion.acabado.dato"
    
    acabado_id = fields.Many2one("eclipse.cotizacion.acabado", string="Acabado")
    name = fields.Char("Nombre", required=True)
    tipo = fields.Selection([('numero', 'Número'),('texto', 'Texto'),('seleccion','Selección')],
        string="Tipo de dato")
    opciones_seleccion = fields.Many2many("eclipse.cotizacion.acabado.dato.opcion", "eclipse_cotizacion_acabado_dato_opcion_rel", "id1", "id2", string=u"Opciones de la selección")

class acabado_dato_opcion(models.Model):
    _name = "eclipse.cotizacion.acabado.dato.opcion"
    
    name = fields.Char("Nombre", required=True)

class instancia_acabado(models.Model):
    _name = "eclipse.cotizacion.acabado.inst"

    acabado_id = fields.Many2one("eclipse.cotizacion.acabado", string="Nombre", required=True)
    cotizacion_id = fields.Many2one("eclipse.cotizacion", string=u"Cotización")
    datos = fields.One2many("eclipse.cotizacion.acabado.dato.inst", "acabado_inst_id")
    show_datos = fields.Boolean("Pedir datos", default=False)

    def onchange_acabado_id(self, cr, uid, ids, acabado_id):
        if acabado_id:
            acabado = self.pool.get("eclipse.cotizacion.acabado").browse(cr, uid, acabado_id)
            show_datos = len(acabado.datos) > 0
            datos_lines = []
            for dato in acabado.datos:
                datos_lines.append((0,0,{'acabado_dato_id': dato.id}))
            return {
                'value': {'show_datos': show_datos, 'datos': datos_lines}
            }
        return {}
    
class instancia_acabado_dato(models.Model):
    _name = "eclipse.cotizacion.acabado.dato.inst"
    
    acabado_inst_id = fields.Many2one("eclipse.cotizacion.acabado.inst", string="Acabado")
    acabado_dato_id = fields.Many2one("eclipse.cotizacion.acabado.dato", string="Dato")
    tipo_dato = fields.Selection(related="acabado_dato_id.tipo", string="Tipo dato", readonly=True)
    dominio_seleccion = fields.Many2many(related="acabado_dato_id.opciones_seleccion", string="Dominio seleccion", readonly=True)
    numero = fields.Float(u"Número")
    cadena = fields.Char("Texto")
    seleccion = fields.Many2one("eclipse.cotizacion.acabado.dato.opcion", string=u"Selección")
    
    
    
