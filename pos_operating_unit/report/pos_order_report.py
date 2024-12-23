from odoo import fields, models


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        relation="pos_order_operating_unit_rel",
        column1="pos_order_id",
        column2="operating_unit_id",
        string="Operating Units",
    )
