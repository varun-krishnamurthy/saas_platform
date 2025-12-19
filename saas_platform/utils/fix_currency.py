"""Fix Free Plan currency"""
import frappe


def fix_free_plan_currency():
    """Update Free Plan to use system default currency"""
    default_currency = frappe.db.get_single_value(
        'Global Defaults', 'default_currency') or 'USD'
    print(f"System default currency: {default_currency}")

    if frappe.db.exists("Subscription Plan", "Free Plan"):
        frappe.db.set_value("Subscription Plan", "Free Plan",
                            "currency", default_currency)
        frappe.db.commit()
        print(f"Updated Free Plan to use {default_currency}")
    else:
        print("Free Plan does not exist")
