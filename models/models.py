# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
 

class InsurancePolicy(models.Model):
    _name = 'insurance.policy'
    _description = 'Insurance Policy management'

    policyholder_id = fields.Many2one('res.partner', string='Policy holder', domain=[('customer_rank', '>', 0)])
    product_id = fields.Many2one('product.template', string='Product')
    provider_id = fields.Many2one('res.partner', string='Provider', domain=[('supplir_rank', '>', 0)])
    #usuari que el crea
    created_by = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    #data de creació    
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)

    description = fields.Text(' Description')

    #data efectiva
    effective_date = fields.Date(string='Effective Date')
    cancellation_date = fields.Date(string='Cancellation Date')

    active = fields.Boolean(string='Active', default=True)

    type = fields.Selection([
        ('anual', 'Anual'),
        ('mensual', 'Mensual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral')  
    ], string='type')  

    @api.constrains('cancellation_date', 'effective_date')
    def _check_dates(self):
        for record in self:
            if record.cancellation_date and record.effective_date and record.cancellation_date < record.effective_date:
                raise ValidationError(_('Cancellation date cannot be before effective date.'))
            
    reason_id = fields.Many2one('insurance.reason', string='Reason for cancellation')

    def unlink(self):
        #cannot be deleted
        raise ValidationError(_('Insurance policies cannot be deleted.'))


    #cannot set to inactive unless cancellation date is set and reason for cancellation is set
    @api.constrains('active')
    def _check_active(self):
        for record in self:
            if not record.active:
                if not record.cancellation_date:
                    raise ValidationError(_('Cancellation date must be set to set policy as inactive.'))
                if not record.reason_id:
                    raise ValidationError(_('Reason for cancellation must be set to set policy as inactive.'))
                
    
    def _compute_display_name(self):
        for record in self:
            if record.policyholder_id and record.product_id:
                record.display_name = record.id + " - " + record.policyholder_id.name + " - " + record.product_id.name
            else:
                record.display_name = super(InsurancePolicy, record)._compute_display_name()
                


    

class InsuranceReason(models.Model):
    _name = 'insurance.reason'
    _description = 'Insurance Reason management'


    