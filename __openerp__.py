# -*- encoding: utf-8 -*-
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'Eclipse - Módulo de Cotización',
    'version' : '',
    'author' : 'Julián Solórzano',
    'website' : '',
    'category' : '',
    'depends' : [],
    'description': """
Módulo para cotizar
    """,
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        
        'data/eclipse.cotizacion.opcion.csv',
        
        'report.xml',
        'report_cotizacion.xml',
        'report_cartacotizacion.xml',
        'report_cotizacionflete.xml',
        'report_cartacotizacionflete.xml',
        
        'eclipse_coti.xml',
        'papel_view.xml',
        'acabado_view.xml',
        'opcion_view.xml',
        'cotizacion_view.xml',
        'partner_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
