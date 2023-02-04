// Copyright (c) 2023, mohammed and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance', {
	// refresh: function(frm) {

	// }

// check_in: function (frm) {
//    frm.trigger("calculate_work__hours");
//  },
//  check_out: function (frm) {
//    frm.trigger("calculate_work__hours");
//  },


//	  calculate_work__hours: function (frm) {
//    if (
//      frm.doc.check_in != undefined &&
//      frm.doc.check_out != undefined
//    ) {
//      frappe.call({
//        method:
//          "human_resource.human_resource.doctype.attendance.attendance.calculate_work_late_hours",
//        args: {
//          employee: frm.doc.employee,
//          check_in: frm.doc.check_in,
//          check_out: frm.doc.check_out,
//        },
//
//        callback: (r) => {
//          frm.doc.work_hours = r.message.work_hours;
//          frm.doc.late_hours = r.message.late_hours;
//          frm.refresh();
//        },
//      });
//    }
//  },
});
