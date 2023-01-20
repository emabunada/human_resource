//// Copyright (c) 2023, mohammed and contributors
//// For license information, please see license.txt
//
//frappe.ui.form.on('Employee', {
//  validate: function (frm) {
//    calculate_age(frm);
//    age_lower_sixty(frm);
//    full_name(frm);
//    mobile_validation(frm);
//    child_table_length(frm);
//
//
//  },
//
//});
//
//
//function calculate_age(frm) {
//  var dob = new Date(frm.doc.employee_date_of_birth);
//  var now = new Date();
//  var age_now = now.getFullYear() - dob.getFullYear();
//  cur_frm.set_value("employee_age", age_now);
//}
//
//
//function age_lower_sixty(frm) {
//
//  var age = parseInt(frm.doc.employee_age);
//  var status = frm.doc.employee_status;
//  if (age >= 60 && status == 'Active') {
//    frappe.throw('Active employee age must be lower than 60');
//  }
//
//}
//
//
//function full_name(frm) {
//
//  var first = frm.doc.employee_first_name != undefined ?frm.doc.employee_first_name:'';
//  var middle = frm.doc.employee_middle_name!= undefined ?frm.doc.employee_middle_name:'';
//  var last = frm.doc.employee_last_name!= undefined ?frm.doc.employee_last_name:'';
//  cur_frm.set_value("employee_full_name", first+' '+middle+' '+last);
//
//
//}
//
//function mobile_validation(frm) {
//
//  var mobile = frm.doc.employee_mobile != undefined ?frm.doc.employee_mobile:'';
//
//if (mobile.length < 10 ) {
//    frappe.throw('mobile number must be more than 9 digits');
//
//
//    }else   if(!mobile.startsWith('059')){
//    frappe.throw('Mobile number must start with 059');
//  }
//
//
//}
//
//function child_table_length(frm) {
//
//var total_education = 0;
//// msgprint(total_education.toString());
// $.each(frm.doc.employee_education,  function(i,  d) {
// if ( d.employee_school){
// total_education += 1; }
// });
//if(total_education <= 2 ){
//  frappe.throw('the employee must have more than two education degrees');
//}
//
//}
//
//
//
