import frappe

from quickfix.service_center.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):
	def validate(self):
		super().validate()
		self._check_urgent_unassigned()

	def _check_urgent_unassigned(self):
		if self.priority == "Urgent" and not self.assigned_technician:
			settings = frappe.get_single("QuickFix Settings")
			frappe.enqueue(
				"quickfix.utils.send_urgent_alert", job_card=self.name, manager=settings.manager_email
			)


"""

what is Method Resolution Order (MRO), and why calling super() is non-negotiable
Method Resolution Order (MRO) is the order which python use to look for the method and the class in the inheritance hierarchy. When you call super(), it ensures that the method from the parent class is called, following the MRO. This is crucial for maintaining the integrity of the class hierarchy and ensuring that all necessary methods are executed properly. Not using super() can lead to unexpected behavior and bugs, especially in complex inheritance scenarios.

example of MRO:
class A:
	def method(self):
		print("Method in A")
class B(A):
	def method(self):
		print("Method in B")
		super().method()
class C(B):
	def method(self):
		print("Method in C")
		super().method()
class D(C):
	def method(self):
		print("Method in D")
		super().method()
d = D()
d.method()
Output:
Method in D
Method in C
Method in B
Method in A
"""

"""
when would you choose override_doctype_class over doc_events?

override_doctype_class
    use when the whole class needs to be overridden
	use to change the behaviour of the multiple methods in the doctype

doc_events
	use when you want to add some additional logic to the existing methods without changing the core logic
	use to trigger some custom logic on specific events like on_update, on_submit etc without changing the
	it does not require overriding the whole class and is more lightweight than override_doctype_class
"""
