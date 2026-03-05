// Copyright (c) 2026, dharanidharans and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	refresh(frm) {},
});
frappe.realtime.on("job_ready", function (data) {
	frappe.show_alert(`Job ${data.job} is ready`);
});
