from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _to_markup_data(self, website):
        """Keep schema.org availability InStock when the shop still sells it."""
        markup_data = super()._to_markup_data(website)
        offers = markup_data.get("offers") or {}
        if self.is_product_variant and self.is_storable and self.allow_out_of_stock_order and offers:
            offers["availability"] = "https://schema.org/InStock"
        return markup_data
