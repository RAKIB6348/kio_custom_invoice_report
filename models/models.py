# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one(
        'education.student',
        string='Student',
        compute='_compute_student_id',
    )
    student_class_roll = fields.Integer(
        string='Student Roll No',
        compute='_compute_student_id',
    )
    student_class_division_id = fields.Many2one(
        'education.class.division',
        string='Student Class',
        compute='_compute_student_id',
    )
    student_group_id = fields.Many2one(
        'education.group',
        string='Student Section',
        compute='_compute_student_id',
    )

    def _compute_student_id(self):
        students_by_partner = {
            student.partner_id.id: student
            for student in self.env['education.student'].sudo().search([
                ('partner_id', 'in', self.mapped('partner_id').ids)
            ])
        }
        for move in self:
            student = students_by_partner.get(move.partner_id.id)
            move.student_id = student
            move.student_class_roll = student.class_roll if student else False
            move.student_class_division_id = student.class_division_id if student else False
            move.student_group_id = student.group_id if student else False

    def action_print_custom_receipt_invoice(self):
        self.ensure_one()
        return self.env.ref(
            'kio_custom_invoice_report.action_report_custom_receipt_invoice'
        ).report_action(self)
