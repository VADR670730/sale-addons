# Copyright 2020 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class SaleOrderLineProductConfiguratorTest(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(SaleOrderLineProductConfiguratorTest, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.sale_line_obj = cls.env['sale.order.line']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'partner_invoice_id': cls.partner.id,
            'partner_shipping_id': cls.partner.id,

        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
        })

    def test_copy_sale_order_line(self):
        new_line = self.sale_line_obj.new({'name': 'test',
                                           'order_id': self.sale_order.id,
                                           'product_id': self.product.id,
                                           'product_uom_qty': 2,
                                           })
        self.sale_order.order_line = new_line
        self.sale_order.order_line.copy_sale_order_line()
        self.assertEqual(len(self.sale_order.order_line), 2)
