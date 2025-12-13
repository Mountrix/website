##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    sale_order_type_id = fields.Many2one(
        'sale.order.type',
        string='Sale Order Type',
    )

    def _prepare_sale_order_values(self, partner_sudo):
        res = super()._prepare_sale_order_values(partner_sudo=partner_sudo)
        sale_type = (partner_sudo.sale_type or self.sudo().sale_order_type_id)

        if sale_type:
            res['type_id'] = sale_type.id
            if sale_type.warehouse_id:
                res['warehouse_id'] = sale_type.warehouse_id.id
                res['company_id'] = sale_type.warehouse_id.company_id.id
        
        # Ensure warehouse_id is always set, even if sale_type doesn't have one
        if not res.get('warehouse_id'):
            # Try to get warehouse from website's _get_warehouse_available method
            warehouse_id = self.sudo()._get_warehouse_available()
            if warehouse_id:
                res['warehouse_id'] = warehouse_id
            else:
                # Fallback: get first warehouse for the company
                company_id = res.get('company_id') or self.env.company.id
                warehouse = self.env['stock.warehouse'].sudo().search(
                    [('company_id', '=', company_id)], limit=1
                )
                if warehouse:
                    res['warehouse_id'] = warehouse.id
        
        return res
