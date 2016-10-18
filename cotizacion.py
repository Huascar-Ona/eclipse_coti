# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from openerp.exceptions import ValidationError
from openerp.osv import osv
from datetime import datetime
from openerp import SUPERUSER_ID

OPCIONES_1 = {
    'Offset': ['Editorial', 'Producto'],
    'Digital': ['Editorial', 'Producto'],
    'Plotter': ['Producto']    
}

OPCIONES_2 = {
    'Editorial': ['Catálogo', 'Block', 'Libro', 'Manual', 'Revista', 'Cuaderno', 'Libreta', 'Otro'],
    'Producto': ['Caja', 'Cuadríptico', 'Díptico', 'Etiqueta', 'Flyer', 'Folder', 
        'Volante', 'Encarte', 'Tríptico', 'Políptico', 'Póster', 'Dangler', 'Stopper', 'Cenefa', 
        'Planilla de etiquetas', 'Colgante', 'Tarjeta', 'Separador', 'Collarín', 'Sobre', 'Otro']
}

OPCIONES_PLOTTER = ['Póster', 'Otro']

class opcion(models.Model):
    _name = "eclipse.cotizacion.opcion"
    
    name = fields.Char("Nombre", required=True)

class vendedor(models.Model):
    _name = "eclipse.vendedor"

    name = fields.Char("Nombre", required=True)

class cotizacion(models.Model):
    _name = "eclipse.cotizacion"
    _order = "name desc"

    #Datos encabezado
    name = fields.Char(u"No. de cotización", required=True, default="/", readonly=True, states={'draft':[('readonly',False)]})
    fecha = fields.Datetime("Fecha de solicitud", readonly=True, states={'draft':[('readonly',False)]})
    tiempo_de_entrega = fields.Datetime("Fecha de entrega", readonly=True, states={'draft':[('readonly',False)]})
    agente = fields.Many2one("eclipse.vendedor", string="Agente", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    atencion_a = fields.Char(u"Atención a", readonly=True, states={'draft':[('readonly',False)]})
    empresa = fields.Many2one("res.partner", string="Empresa", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    tel = fields.Char(u"Tel", readonly=True, states={'draft':[('readonly',False)]})
    
    #Opciones
    descripcion = fields.Char(u"Descripción del proyecto", readonly=True, states={'draft':[('readonly',False)]})
    diseno = fields.Selection([("s", "Sí"), ("n", "No")], required=True, string=u"Diseño", readonly=True, states={'draft':[('readonly',False)]})
    check_diseno = fields.Boolean(u"Check Diseño", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    flete = fields.Selection([("s", "Sí"), ("n", "No")], required=True, string=u"Flete Foráneo", readonly=True, states={'draft':[('readonly',False)]})
    check_flete = fields.Boolean(u"Check Flete", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    tienes_costo = fields.Selection([("s", "Sí"), ("n", "No")], readonly=True, states={'draft':[('readonly',False)]}, required=True, string=u"¿Tienes el costo?")
    costo_flete = fields.Float("Costo flete", readonly=True, states={'draft':[('readonly',False)]})
    codigos_postales = fields.One2many("eclipse.cotizacion.cp", "cotizacion_id", readonly=True, states={'draft':[('readonly',False)]}, string=u"Códigos Potales")
    opcion1 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string="Proceso", domain=[('name', 'in', list(OPCIONES_1.keys()))], readonly=True, states={'draft':[('readonly',False)]})
    check_opcion1 = fields.Boolean(u"Check Opción 1", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    opcion2 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string=u"Tipo", readonly=True, states={'draft':[('readonly',False)]})
    check_opcion2 = fields.Boolean(u"Check Opción 2", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    opcion3 = fields.Many2one("eclipse.cotizacion.opcion", required=True, string=u"Subtipo", readonly=True, states={'draft':[('readonly',False)]})
    check_opcion3 = fields.Boolean(u"Check Opción 3", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    show_otro = fields.Boolean("Mostrar Otro", default=False)
    opcion_otro = fields.Char("Especificar", readonly=True, states={'validating':[('readonly',False)]})
    es_editorial = fields.Boolean("Es Editorial", default=False)
    es_digital = fields.Boolean("Es Digital", default=False)
    es_plotter = fields.Boolean("Es Plotter", default=False)
    
    #Para Produto y para Editorial - Forros:
    #Medida extendida en cm
    check_medida_ext = fields.Boolean(u"Check Medida ext", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    largo_ext = fields.Float("Largo", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    ancho_ext = fields.Float("Ancho", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    #Medida final en cm
    check_medida_final = fields.Boolean(u"Check Medida Final", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    largo_final = fields.Float("Largo", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    ancho_final = fields.Float("Ancho", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    #Tintas a X b
    check_tintas = fields.Boolean(u"Check Tintas", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    tintas_a = fields.Selection([(x,x) for x in '0123456789'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    tintas_b = fields.Selection([(x,x) for x in '0123456789'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]})
    #Barnices
    check_barniz_mate = fields.Boolean(u"Check Barniz Mate", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    barniz_mate_a = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina mate", readonly=True, states={'draft':[('readonly',False)]})
    barniz_mate_b = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina mate", readonly=True, states={'draft':[('readonly',False)]})
    check_barniz_brillante = fields.Boolean(u"Check Barniz Brillante", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    barniz_brillante_a = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina brillante", readonly=True, states={'draft':[('readonly',False)]})
    barniz_brillante_b = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina brillante", readonly=True, states={'draft':[('readonly',False)]})
    #Pantone
    check_pantone = fields.Boolean(u"Check Pantone", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    pantone = fields.Char("Pantone", readonly=True, states={'draft':[('readonly',False)]})
    #No. páginas (solo Forros)
    check_n_paginas = fields.Boolean(u"Check N Paginas", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    n_paginas = fields.Integer(u"No. Páginas", required=True, readonly=True, states={'draft':[('readonly',False)]})
    
    #Para Editorial - Interiores:
    #Medida extendida en cm
    check_medida_ext_int = fields.Boolean(u"Check Medida ext int", readonly=True, states={'submitted':[('readonly',False)]})
    largo_ext_int = fields.Float("Largo", readonly=True, states={'draft':[('readonly',False)]})
    ancho_ext_int = fields.Float("Ancho", readonly=True, states={'draft':[('readonly',False)]})
    #Medida final en cm
    check_medida_final_int = fields.Boolean(u"Check Medida final int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    largo_final_int = fields.Float("Largo", readonly=True, states={'draft':[('readonly',False)]})
    ancho_final_int = fields.Float("Ancho", readonly=True, states={'draft':[('readonly',False)]})
    #Tintas a X b
    check_tintas_int = fields.Boolean(u"Check Tintas int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    tintas_a_int = fields.Selection([(x,x) for x in '0123456789'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]})
    tintas_b_int = fields.Selection([(x,x) for x in '0123456789'], string="Tintas", readonly=True, states={'draft':[('readonly',False)]})
    #Barnices
    check_barniz_mate_int = fields.Boolean(u"Check Barniz mate int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    barniz_mate_a_int = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina mate", readonly=True, states={'draft':[('readonly',False)]})
    barniz_mate_b_int = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina mate", readonly=True, states={'draft':[('readonly',False)]})
    check_barniz_brillante_int = fields.Boolean(u"Check Barniz brillante int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    barniz_brillante_a_int = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina brillante", readonly=True, states={'draft':[('readonly',False)]})
    barniz_brillante_b_int = fields.Selection([(x,x) for x in '01'], string=u"Barniz máquina brillante", readonly=True, states={'draft':[('readonly',False)]})
    #Pantone
    check_pantone_int = fields.Boolean(u"Check Pantone int", readonly=True, states={'submitted':[('readonly',False)]})
    pantone_int = fields.Char("Pantone", readonly=True, states={'draft':[('readonly',False)]})
    #No. páginas
    check_n_paginas_int = fields.Boolean(u"Check N Paginas int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    n_paginas_int = fields.Integer(u"No. Páginas", readonly=True, states={'draft':[('readonly',False)]})
    check_tipo_paginas_int = fields.Boolean(u"Check Tipo paginas int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    tipo_paginas_int = fields.Selection([("iguales", "Iguales"),("diferentes", "Diferentes")], string=u"Tipo páginas", readonly=True, states={'draft':[('readonly',False)]})

    #Tipo de papel
    check_papel = fields.Boolean(u"Check Papel", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    papel = fields.Many2one("eclipse.cotizacion.papel", string="Papel", readonly=True, states={'draft':[('readonly',False)]})
    papel_otro = fields.Char("Otro: (Especificar)", readonly=True, states={'draft':[('readonly',False)]})
    #Para Editorial- Interiores
    check_papel_int = fields.Boolean(u"Check Papel int", readonly=True, states={'submitted':[('readonly',False)]}, copy=False)
    papel_int = fields.Many2one("eclipse.cotizacion.papel", string="Papel", readonly=True, states={'draft':[('readonly',False)]})
    papel_otro_int = fields.Char("Otro: (Especificar)", readonly=True, states={'draft':[('readonly',False)]})
    
    #Acabados
    #Ambos:
    acabados = fields.One2many("eclipse.cotizacion.acabado.inst", "cotizacion_id", string="Acabados", readonly=True, states={'draft':[('readonly',False)]}, copy=True)
    #Solo Editorial:
    check_tipo_encuadernado = fields.Boolean(u"Check Tipo Encuadernado", readonly=True, states={'submitted':[('readonly',False)]})
    tipo_encuadernado = fields.Many2one("eclipse.cotizacion.acabado", string="Tipo encuadernado", readonly=True, states={'draft':[('readonly',False)]}, domain=[('acabado','=','Encuadernación')])
    
    #Precios y observaciones
    precios = fields.One2many("eclipse.cotizacion.precio", "cotizacion_id", string="Precios", states={'validated':[('readonly',True)]}, copy=True)
    observaciones = fields.Text("Observaciones", readonly=True, states={'draft':[('readonly',False)]})
    
    #Variables de control
    bloqueada = fields.Many2one("res.users", string=u"Cotizador")
    validaciones = fields.One2many("eclipse.cotizacion.validacion", "cotizacion_id", string="Validaciones",  states={'cancel':[('readonly',True)]})
    state = fields.Selection([('draft', 'Requisición'),('submitted', 'Esperando precio'),
        ('validating', 'Esperando validación'), ('validated', 'Validada'), ('cancel', 'Cancelada')], string="Estado", default="draft")

    _sql_constraints = [('unique_name', 'unique(name)', 'Folio repetido')]

    def copy(self, cr, uid, id, default={}, context=None):
        if default is None: default={}
        default["name"] = "/"
        return super(cotizacion, self).copy(cr, uid, id, default=default, context=context)

    def create(self, cr, uid, vals, context=None):
        if vals.get("name", "/") == "/":
            vals["name"] = self.pool.get('ir.sequence').get(cr, uid, 'secuencia.cotizacion')
        return super(cotizacion, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        this = self.browse(cr, uid, ids[0])
        model_obj = self.pool.get("ir.model.data")
        requisicion_group = model_obj.get_object(cr, uid, 'eclipse_coti', 'grupo_requisicion').id
        cotizacion_group = model_obj.get_object(cr, uid, 'eclipse_coti', 'grupo_cotizacion').id
        user_groups = self.pool.get("res.users").browse(cr, uid, uid).groups_id
        user_groups = [x.id for x in user_groups]
        vendedor = requisicion_group in user_groups
        cotizador = cotizacion_group in user_groups
        if vendedor and not cotizador:
            if this.state != 'draft':
                raise osv.except_osv("Error", u"Los vendedores no pueden editar ningún aspecto de la cotización una vez solicitada")
        if this.bloqueada and vals.get("bloqueada", None) != False and this.bloqueada.id != uid:
            raise osv.except_osv("Bloqueada", u"La cotización está bloqueada")
        return super(cotizacion, self).write(cr, uid, ids, vals, context=context)

    def action_bloquear(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'bloqueada': uid})
        return True

    def action_desbloquear(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'bloqueada': False})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def onchange_opcion1(self, cr, uid, ids, opcion1, context=None):
        if opcion1:
            #Abir tipos de acuerdo al proceso seleccionado
            opcion1 = self.pool.get("eclipse.cotizacion.opcion").browse(cr, uid, opcion1).name
            opciones = OPCIONES_1[opcion1]
            opcion2_ids = self.pool.get("eclipse.cotizacion.opcion").search(cr, uid, [('name', 'in', opciones)])
            es_digital = opcion1 == 'Digital'
            es_plotter = opcion1 == 'Plotter'
            res = {
                'domain': {'opcion2': [('id', 'in', opcion2_ids)]},
                'value': {'es_digital': es_digital, 'es_plotter': es_plotter}
            }
            if es_plotter:
                res["value"]["tintas_a"] = '4'
            return res
        return {}

    def onchange_opcion2(self, cr, uid, ids, opcion1, opcion2, context=None):
        if opcion2:
            opcion_obj = self.pool.get("eclipse.cotizacion.opcion")
            opcion1 = opcion_obj.browse(cr, uid, opcion1).name
            opcion2 = opcion_obj.browse(cr, uid, opcion2).name
            #Abir subtipos de acuerdo al tipo seleccionado. Si es plotter usar las opciones de plotter
            if opcion1 == 'Plotter':
                opciones = OPCIONES_PLOTTER
            else:
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
        for rec in self.browse(cr, uid, ids):
            if rec.flete == 's' and rec.tienes_costo == 'n' and len(rec.codigos_postales) == 0:
                raise osv.except_osv(u"No se puede solicitar cotización", u"No has ingresado por lo menos un código postal")
            if len(rec.acabados) < 1:
                raise osv.except_osv(u"No se puede solicitar cotización", u"Debe haber por lo menos un acabado.")                
            if len(rec.precios) == 0:
                raise osv.except_osv(u"No se puede solicitar cotización", u"No se ha ingresado ninguna cantidad a solicitar.")
            self.write(cr, uid, ids, {'state': 'submitted', 'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return True

    def action_solicitar_validacion(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validating', 'bloqueada': False})
        return True
        
    def action_validar(self, cr, uid, ids, context=None):
        val_obj = self.pool.get("eclipse.cotizacion.validacion")
        user_obj = self.pool.get("res.users")
        user = user_obj.browse(cr, uid, uid)
        grupo_validar_25 = self.pool.get("ir.model.data").get_object(cr, uid, 'eclipse_coti', 'grupo_validar_25').id
        user_groups = [x.id for x in user.groups_id]
        adrian = user_obj.search(cr, uid, [('name', '=', 'Adrian Mees')])
        adrian = adrian[0] if adrian else 0
        for id in ids:
            rec = self.browse(cr, uid, id)
            for cantidad in rec.precios:
                if cantidad.cantidad * cantidad.precio_unitario >= 25000:
                    if uid not in (adrian, SUPERUSER_ID) and grupo_validar_25 not in user_groups:
                        raise osv.except_osv(u"Acción inválida", u"Una de las líneas pasa de $25 mil, se requiere validación de Adrian Mees, de administrador o de miembro del grupo 'Validar más de $25mil'")
                    break
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
            if len(rec.validaciones) >= 2 or uid in (adrian, SUPERUSER_ID):
                self.write(cr, uid, [rec.id], {'state': 'validated'})
        return True

    @api.one
    @api.constrains("largo_ext", "ancho_ext", "largo_final", "ancho_final",
        "largo_ext_int", "ancho_ext_int", "largo_final_int", "ancho_final_int")
    def _check_medidas(self):
        if self.largo_ext <= 0 or self.ancho_ext <= 0 or self.largo_final <= 0 or self.ancho_final <= 0:
            raise exceptions.ValidationError("Todas las medidas deben ser mayores a cero")
        if self.es_editorial:
            if self.largo_ext_int <= 0 or self.ancho_ext_int <= 0 or self.largo_final_int <= 0 or self.ancho_final_int <= 0:
                raise exceptions.ValidationError("Todas las medidas deben ser mayores a cero")
        medida_ext = self.largo_ext * self.ancho_ext
        medida_final = self.largo_final * self.ancho_final
        medida_ext_int = self.largo_ext_int * self.ancho_ext_int
        medida_final_int = self.largo_final_int * self.ancho_final_int
        if medida_final > medida_ext or medida_final_int > medida_ext_int :
            raise exceptions.ValidationError("La medida final no puede ser mayor a la medida extendida")

    @api.one
    @api.constrains("barniz_mate_a", "barniz_mate_b", "barniz_brillante_a", "barniz_brillante_b")
    def _check_barnices(self):
        if self.barniz_mate_a or self.barniz_mate_b:
            if self.barniz_mate_a == '0' and self.barniz_mate_b == '0':
                raise exceptions.ValidationError("Los barnices solo pueden ser 1x0, 1x1 ó 0x1")
        if self.barniz_brillante_a or self.barniz_brillante_b:
            if self.barniz_brillante_a == '0' and self.barniz_brillante_b == '0':
                raise exceptions.ValidationError("Los barnices solo pueden ser 1x0, 1x1 ó 0x1")
    
    @api.one
    @api.constrains("costo_flete")
    def _check_flete(self):
        if self.flete == 's' and self.tienes_costo == 's' and self.costo_flete <= 0:
            raise exceptions.ValidationError("El costo del flete debe ser mayor a cero")

    @api.one
    @api.constrains("tiempo_de_entrega", "fecha")
    def _check_tiempo_entrega(self):
        if self.tiempo_de_entrega < self.fecha:
            raise exceptions.ValidationError("La fecha de entrega debe ser posterior a la fecha de solicitud.")
    
    @api.one
    @api.constrains("n_paginas", "n_paginas_int")
    def _check_zeros(self):
        if self.es_editorial:
            if self.n_paginas <= 0 or self.n_paginas_int <= 0:
                raise exceptions.ValidationError("El número de páginas debe ser mayor a cero")

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
    cantidad = fields.Float("Cantidad", digits=(14,0), readonly=True, states={'draft':[('readonly',False)]})
    unidad = fields.Char("Unidad", readonly=True, states={'draft':[('readonly',False)]})
    precio_unitario = fields.Float("Precio Unitario", digits=(14,4), readonly=True, states={'validating':[('readonly',False)],'submitted':[('readonly',False)]})
    observacion = fields.Text(u"Observación", readonly=True, states={'draft':[('readonly',False)],'submitted':[('readonly',False)],'validating':[('readonly',False)]})
    state = fields.Selection([('draft', 'Requisición'),('submitted', 'Esperando precio'),
        ('validating', 'Esperando validación'), ('validated', 'Validada')], related="cotizacion_id.state", string="Estado", default="draft")
    
    @api.one
    @api.constrains("cantidad")
    def check_qty(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a cero")


class cotizacion_flete(models.Model):
    _name = "eclipse.cotizacion.flete"

    name = fields.Char(u"No. de cotización", required=True, default="/", readonly=True, states={'draft':[('readonly',False)]})
    fecha = fields.Datetime("Fecha de solicitud", readonly=True, states={'draft':[('readonly',False)]})
    tiempo_de_entrega = fields.Datetime("Fecha de entrega", readonly=True, states={'draft':[('readonly',False)]})
    agente = fields.Many2one("eclipse.vendedor", string="Agente", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    atencion_a = fields.Char(u"Atención a", readonly=True, states={'draft':[('readonly',False)]})
    empresa = fields.Many2one("res.partner", string="Empresa", readonly=True, states={'draft':[('readonly',False)]}, required=True)
    tel = fields.Char(u"Tel", readonly=True, states={'draft':[('readonly',False)]})
    costo_flete = fields.Float("Costo Flete", readonly=True, states={'submitted':[('readonly',False)]})
    descripcion = fields.Text(u"Descripción",  readonly=True, states={'draft':[('readonly',False)]})
    state = fields.Selection([('draft','Borrador'),('submitted','Solicitada'),('validated', 'Validada'),('cancel','Cancelada')], string="Estado", default="draft")

    _sql_constraints = [('unique_name', 'unique(name)', 'Folio repetido')]

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def action_validate(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validated'})
        return True

    def copy(self, cr, uid, id, default={}, context=None):
        if default is None: default={}
        default["name"] = "/"
        return super(cotizacion_flete, self).copy(cr, uid, id, default=default, context=context)

    def create(self, cr, uid, vals, context=None):
        if vals.get("name", "/") == "/":
            vals["name"] = self.pool.get('ir.sequence').get(cr, uid, 'secuencia.cotizacion.flete')
        return super(cotizacion_flete, self).create(cr, uid, vals, context=context)

    @api.one
    @api.constrains("costo_flete")
    def _check_flete(self):
        if self.costo_flete <= 0 and self.state == 'submitted':
            raise exceptions.ValidationError("El costo del flete debe ser mayor a cero")

    def action_solicitar_cotizacion(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if not rec.descripcion:
                raise osv.except_osv(u"No se puede solicitar cotización", u"No se ha ingresado descrípción")
            self.write(cr, uid, ids, {'state': 'submitted', 'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return True

    @api.one
    @api.constrains("tiempo_de_entrega", "fecha")
    def _check_tiempo_entrega(self):
        if self.tiempo_de_entrega < self.fecha:
            raise exceptions.ValidationError("La fecha de entrega debe ser posterior a la fecha de solicitud.")

class codigo_postal(models.Model):
    _name = "eclipse.cotizacion.cp"
    
    name = fields.Char(u"Código postal", size=5)
    cotizacion_id = fields.Many2one("eclipse.cotizacion", string=u"Cotización")

    @api.one
    @api.constrains("name")
    def _check_name(self):
        for ch in self.name:
            if not ch.isdigit():
                raise exceptions.ValidationError("Solo ingresar números en el código postal")
