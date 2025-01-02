# Copyright 2025 braintec AG (https://braintec.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _account_entry_move(self, qty, description, svl_id, cost):
        res = super()._account_entry_move(qty, description, svl_id, cost)
        operating_unit = self.operating_unit_dest_id or self.operating_unit_id
        if operating_unit:
            for val_dict in res:
                val_dict["operating_unit_id"] = operating_unit.id
        return res
