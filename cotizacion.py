# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.osv import osv
from datetime import datetime

OPCIONES_1 = {
    'Offset': ['Editorial', 'Producto'],
    'Digital': ['Editorial', 'Producto'],
    'Plotter': ['Producto']    
}

OPCIONES_2 = {
    'Editorial': ['Catálogo', 'Block', 'Libro', 'Manual', 'Revista', 'Otro'],
    'Producto': ['Caja', 'Cuadríptico', 'Díptico', 'Etiqueta', 'Flyer', 'Folder', 'Otro']
}

class opcion(models.Model):
    _name = "eclipse.cotizacion.opcion"
    
    name = fields.Char("Nombre", required=True)

class vendedor(models.Model):
    _name = "eclipse.vendedor"

    name = fields.Char("Nombre", required=True)

class cotizacion(models.Model):
    _name = "eclipse.cotizacion"

    #Datos encabezado
    name = fields.Char(u"No. de cotización", required=True, default="/", readonly=True, states={'draft':[('readonly',False)]})
    fecha = fields.Datetime("Fecha", readonly=True, states={'draft':[('readonly',False)]}, default=lambda x:datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tiempo_de_entrega = fields.Datetime("Tiempo de entrega", readonly=True, states={'draft':[('readonly',False)]})
    agente = fields.Many2one("eclipse.vendedor", string="Agente", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    atencion_a = fields.Char(u"Atención a", readonly=True, states={'draft':[('readonly',False)]})
    empresa = fields.Many2one("res.partner", string="Empresa", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    tel = fields.Char(u"Tel", readonly=True, states={'draft':[('readonly',False)]})
    
    #Opciones
    diseno = fields.Selection([("s", "Sí"), ("n", "No")], required=True, string=u"Diseño", readonly=True, states={'draft':[('readonly',False)]})
    opcion1 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string="Proceso", domain=[('name', 'in', list(OPCIONES_1.keys()))], readonly=True, states={'draft':[('readonly',False)]})
    opcion2 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string=u"Tipo", readonly=True, states={'draft':[('readonly',False)]})
    opcion3 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string=u"Subtipo", readonly=True, states={'draft':[('readonly',False)]})
    show_otro = fields.Boolean("Mostrar Otro", default=False)
    opcion_otro = fields.Char("Especificar", readonly=True, states={'draft':[('readonly',False)]})
    es_editorial = fields.Boolean("Es Editorial", default=False)
    
    #Para Produto y para Editorial - Forros:
    #Medida extendida en cm
    largo_ext = fields.Integer("Largo", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    ancho_ext = fields.Integer("Ancho", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    #Medida final en cm
    largo_final = fields.Integer("Largo", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    ancho_final = fields.Integer("Ancho", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    #Tintas a X b
    tintas_a = fields.Selection([(x,x) for x in '01234'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    tintas_b = fields.Selection([(x,x) for x in '01234'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    #Pantone
    pantone = fields.Selection([(x,x) for x in '12345'], string="Pantone", readonly=True, states={'draft':[('readonly',False)]})
    #No. páginas (solo Forros)
    n_paginas = fields.Integer(u"No. Páginas", readonly=True, states={'draft':[('readonly',False)]})
    
    #Para Editorial - Interiores:
    #Medida extendida en cm
    largo_ext_int = fields.Integer("Largo", readonly=True, states={'draft':[('readonly',False)]})
    ancho_ext_int = fields.Integer("Ancho", readonly=True, states={'draft':[('readonly',False)]})
    #Medida final en cm
    largo_final_int = fields.Integer("Largo", readonly=True, states={'draft':[('readonly',False)]})
    ancho_final_int = fields.Integer("Ancho", readonly=True, states={'draft':[('readonly',False)]})
    #Tintas a X b
    tintas_a_int = fields.Selection([(x,x) for x in '01234'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]})
    tintas_b_int = fields.Selection([(x,x) for x in '01234'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]})
    #Pantone
    pantone_int = fields.Selection([(x,x) for x in '12345'], string="Pantone", readonly=True, states={'draft':[('readonly',False)]})
    #No. páginas
    n_paginas_int = fields.Integer(u"No. Páginas", readonly=True, states={'draft':[('readonly',False)]})
    tipo_paginas_int = fields.Selection([("iguales", "Iguales"),("diferentes", "Diferentes")], string=u"Tipo páginas", readonly=True, states={'draft':[('readonly',False)]})

    #Tipo de papel
    papel = fields.Many2one("eclipse.cotizacion.papel", string="Papel", readonly=True, states={'draft':[('readonly',False)]})
    papel_otro = fields.Char("Otro: (Especificar)", readonly=True, states={'draft':[('readonly',False)]})
    #Para Editorial- Interiores
    papel_int = fields.Many2one("eclipse.cotizacion.papel", string="Papel", readonly=True, states={'draft':[('readonly',False)]})
    papel_otro_int = fields.Char("Otro: (Especificar)", readonly=True, states={'draft':[('readonly',False)]})
    
    #Acabados
    #Ambos:
    acabados = fields.One2many("eclipse.cotizacion.acabado.inst", "cotizacion_id", string="Acabados", readonly=True, states={'draft':[('readonly',False)]})
    #Solo Editorial:
    tipo_encuadernado = fields.Many2one("eclipse.cotizacion.acabado", string="Tipo encuadernado", readonly=True, states={'draft':[('readonly',False)]}, domain=[('acabado','=','Encuadernación')])
    
    #Precios y observaciones
    precios = fields.One2many("eclipse.cotizacion.precio", "cotizacion_id", string="Precios", states={'validated':[('readonly',True)]})
    observaciones = fields.Text("Observaciones")
    
    #Variables de control
    validaciones = fields.One2many("eclipse.cotizacion.validacion", "cotizacion_id", string="Validaciones")
    state = fields.Selection([('draft', 'Requisición'),('submitted', 'Esperando precio'),
        ('validating', 'Esperando validación'), ('validated', 'Validada')], string="Estado", default="draft")

    def create(self, cr, uid, vals, context=None):
        if vals["name"] == "/":
            vals["name"] = self.pool.get('ir.sequence').get(cr, uid, 'secuencia.cotizacion')
        return super(cotizacion, self).create(cr, uid, vals, context=context)

  
    def onchange_opcion1(self, cr, uid, ids, opcion1, context=None):
        if opcion1:
            #Abir tipos de acuerdo al proceso seleccionado
            opcion1 = self.pool.get("eclipse.cotizacion.opcion").browse(cr, uid, opcion1).name
            opciones = OPCIONES_1[opcion1]
            opcion2_ids = self.pool.get("eclipse.cotizacion.opcion").search(cr, uid, [('name', 'in', opciones)])
            print "******", opcion2_ids
            return {
                'domain': {'opcion2': [('id', 'in', opcion2_ids)]}
            }
        return {}

    def onchange_opcion2(self, cr, uid, ids, opcion2, context=None):
        if opcion2:
            #Abir subtipos de acuerdo al tipo seleccionado
            opcion2 = self.pool.get("eclipse.cotizacion.opcion").browse(cr, uid, opcion2).name
            opciones = OPCIONES_2[opcion2]
            opcion3_ids = self.pool.get("eclipse.cotizacion.opcion").search(cr, uid, [('name', 'in', opciones)])
            es_editorial = opcion2 == 'Editorial'
            return {
                'domain': {'opcion3': [('id', 'in', opcion3_ids)]},
                'value': {'es_editorial': es_editorial}
            }
        return {}
        
    def onchange_opcion3(self, cr, uid, ids, opcion3, context=None):
        if opcion3:
            #Si es "otro" hacer que se muestre el campo de especificar
            opcion = self.pool.get("eclipse.cotizacion.opcion").browse(cr, uid, opcion3).name
            show_otro = opcion == 'Otro'
            return {
                'value': {'show_otro': show_otro}
            }
        return {}
        
    
    def action_solicitar_cotizacion(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'submitted'})
        return True

    def action_solicitar_validacion(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validating'})
        return True
        
    def action_validar(self, cr, uid, ids, context=None):
        val_obj = self.pool.get("eclipse.cotizacion.validacion")
        for id in ids:
            validaciones_user = val_obj.search(cr, uid, [
                ('user_id','=',uid),
                ('cotizacion_id','=',id)])
            if len(validaciones_user) != 0:
                raise osv.except_osv(u"Acción inválida", u"Este usuario ya validó esta cotización")
            val_obj.create(cr, uid, {
                'cotizacion_id': id,
                'user_id': uid
            })
            rec = self.browse(cr, uid, id)
            if len(rec.validaciones) >= 2:
                self.write(cr, uid, [rec.id], {'state': 'validated'})
        return True

    @api.one
    @api.constrains("largo_ext", "ancho_ext", "largo_final", "ancho_final",
        "largo_ext_int", "ancho_ext_int", "largo_final_int", "ancho_final_int")
    def _check_medidas(self):
        medida_ext = self.largo_ext * self.ancho_ext
        medida_final = self.largo_final * self.ancho_final
        medida_ext_int = self.largo_ext_int * self.ancho_ext_int
        medida_final_int = self.largo_final_int * self.ancho_final_int
        if medida_final > medida_ext or medida_final_int > medida_ext_int :
            raise exceptions.ValidationError("La medida final no puede ser mayor a la medida extendida")
    
    @api.one
    @api.constrains("n_paginas", "n_paginas_int")
    def _check_zeros(self):
        if self.es_editorial:
            if self.n_paginas <= 0 or self.n_paginas_int <= 0:
                raise exceptions.ValidationError("El número de páginas no puede ser cero")

    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if rec.state != 'draft':
                raise osv.except_osv(u"Acción no permitida", u"No se pueden borrar cotizaciones a menos que estén en estado borrador")
        return super(cotizacion, self).unlink(cr, uid, ids, context=context)

class cotizacion_validacion(osv.Model):
    _name = "eclipse.cotizacion.validacion"
    
    cotizacion_id = fields.Many2one("eclipse.cotizacion", string=u"Cotización")
    user_id = fields.Many2one("res.users", string="Validador")
    
class cotizacion_precio(models.Model):
    _name = "eclipse.cotizacion.precio"

    cotizacion_id = fields.Many2one("eclipse.cotizacion", string=u"Cotización")
    cantidad = fields.Float("Cantidad", digits=(14,0))
    precio_unitario = fields.Float("Precio Unitario")
    observacion = fields.Text(u"Observación")

