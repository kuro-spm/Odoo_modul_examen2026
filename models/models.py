# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
 
 
class examen_pratssaraType(models.Model): 
    _name = 'examen_pratssara.type' 
    _description = 'Type Management' 
 
    name = fields.Char('Name', size=60, required=True) 
    #campo_id = fields.Many2one('modelo.relacionado', string='Etiqueta') 
    #campos_ids = fields.One2many('modelo.relacionado', 'campo_many2one_relacionado', string='Etiqueta') 
    #campos_ids = fields.Many2many('modelo.relacionado', string='Etiqueta') 
