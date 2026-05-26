# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ , tools
from odoo.exceptions import ValidationError 
from dateutil.relativedelta import relativedelta
 

class InsurancePolicy(models.Model):
    _name = 'insurance.policy'
    _description = 'Insurance Policy management'
    _order = 'id desc'

    policyholder_id = fields.Many2one('res.partner', string='Policy holder', domain=[('customer_rank', '>', 0)])
    product_id = fields.Many2one('product.template', string='Insurance')
    broker_id = fields.Many2one('res.partner', string='Insurance Broker', domain=[('supplier_rank', '>', 0)])
    created_by = fields.Many2one('res.partner', string='Created by', default=lambda self: self.env.user)
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    object = fields.Text('Insured Object')
    cancellation_date = fields.Date(string='Cancellation Date')
    effective_date = fields.Date(string='Effective Date')
    effective_hour = fields.Float(string='Effective Hour')
    expiration_date = fields.Date(string='Expiration Date')
    reason_id = fields.Many2one('insurance.reason', string='Reason for cancellation')
    active = fields.Boolean(string='Active', default=True)

    type = fields.Selection([
        ('anual', 'Anual'),
        ('mensual', 'Mensual'),
        ('semestral', 'Semestral'),
        ('trimestral', 'Trimestral')  
    ], string='Type of expiration', default='anual') 

    def _compute_expiration_date(self):
        for record in self:
            if record.effective_date and record.type:
                if record.type == 'anual':
                    record.expiration_date = record.effective_date + relativedelta(years=1)
                elif record.type == 'mensual':
                    record.expiration_date = record.effective_date + relativedelta(months=1)
                elif record.type == 'semestral':
                    record.expiration_date = record.effective_date + relativedelta(months=6)
                elif record.type == 'trimestral':
                    record.expiration_date = record.effective_date + relativedelta(months=3)
            else:
                record.expiration_date = False 

    # cancellation date cannot be before effective date
    @api.constrains('cancellation_date', 'effective_date')
    def _check_cancellation_date(self):
        for record in self:
            if record.cancellation_date and record.effective_date and record.cancellation_date < record.effective_date:
                raise ValidationError(_('Cancellation date cannot be before effective date.'))
    
    # efective date cannot be in the past
    @api.constrains('effective_date')
    def _check_effective_date(self):
        for record in self:
            if record.effective_date and record.effective_date < fields.Date.today():
                raise ValidationError(_('Effective date cannot be in the past.'))       

    def unlink(self):
        #cannot be deleted
        raise ValidationError(_('Insurance policies cannot be deleted.'))


    #cannot set to inactive unless cancellation date is set and reason for cancellation is set
    @api.constrains('active')
    def _check_active(self):
        for record in self:
            if not record.active:
                if not record.expiration_date:
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
    
    description = fields.Text(string='Reason for cancellation', required=True)
    #unique index on description
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)


    #def _auto_init(self):
    #    res = super(InsuranceReason, self)._auto_init()
    #    tools.create_unique_index(self._cr, 'insurance_reason_description_uniq', self.ids, ['lower(description)'])
      
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Res Partner'

    insurance_policy_ids = fields.One2many('insurance.policy', 'policyholder_id', string='Insurance Policies')
    insurance_broker_ids = fields.One2many('insurance.policy', 'broker_id', string='Insurance Broker Policies')
    


    