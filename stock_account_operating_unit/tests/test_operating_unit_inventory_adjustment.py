# Copyright 2025 braintec AG (https://braintec.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestOperatingUnitInventoryAdjustment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up a stock.quant that will be adjusted.
        # This quant should have an Operating Unit.
        cls.company_id = cls.env.ref("base.main_company")
        cls.operating_unit_id = cls.env["operating.unit"].create(
            {
                "name": "TestOU",
                "code": "TESTOU",
                "partner_id": cls.company_id.partner_id.id,
            }
        )
        cls.product_id = cls.env["product.template"].create(
            {
                "name": "TestProductTemplate",
                "type": "product",
                "standard_price": 1,
            }
        )
        cls.product_id.product_variant_id.valuation = "real_time"
        cls.location_id = cls.env["stock.location"].create(
            {
                "name": "TestLocation",
                "usage": "internal",
                "operating_unit_id": cls.operating_unit_id.id,
            }
        )
        cls.lot_id = cls.env["stock.lot"].create(
            {"name": "TestLot", "product_id": cls.product_id.product_variant_id.id}
        )
        cls.quant_id = cls.env["stock.quant"].create(
            {
                "product_id": cls.product_id.product_variant_id.id,
                "inventory_quantity": 10,
                "location_id": cls.location_id.id,
                "lot_id": cls.lot_id.id,
            }
        )

    def test_operating_unit_inventory_adjustment(self):
        # The same operating unit must be set in the account.move
        # related to this inventory adjustment.
        self.quant_id.inventory_quantity = 5
        self.quant_id.action_apply_inventory()
        move = self.env["account.move"].search(
            [("ref", "ilike", "% - TestProductTemplate")],
            limit=1,
            order="create_date desc",
        )
        self.assertTrue(move.exists())
        self.assertEqual(move.operating_unit_id, self.operating_unit_id)
