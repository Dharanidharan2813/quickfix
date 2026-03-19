frappe.ready(() => {
	if (frappe.boot.quickfix_shop_name) {
		const navbar = document.querySelector(".navbar-brand");

		if (navbar) {
			navbar.innerText = frappe.boot.quickfix_shop_name;
		}
	}
});
