"""Add tenant_id Custom Field to User DocType"""
import frappe


def add_tenant_id_to_user():
    """Add tenant_id Custom Field to User DocType"""

    if frappe.db.exists("Custom Field", "User-tenant_id"):
        print("Custom Field 'User-tenant_id' already exists")
        return

    custom_field = frappe.get_doc({
        "doctype": "Custom Field",
        "dt": "User",
        "fieldname": "tenant_id",
        "fieldtype": "Data",
        "label": "Tenant ID",
        "insert_after": "enabled",
        "read_only": 1,
        "hidden": 0,  # Visible for admin to see which tenant user belongs to
        "no_copy": 1,
        "print_hide": 1,
        "report_hide": 0,  # Allow in reports for admin
        "in_list_view": 1,
        "in_standard_filter": 1,
        "description": "The tenant this user belongs to. SYSTEM = Platform administrator."
    })
    custom_field.insert(ignore_permissions=True)
    frappe.db.commit()

    print(f"Created Custom Field 'tenant_id' for User DocType")


def set_administrator_tenant_id():
    """Set Administrator user's tenant_id to SYSTEM"""
    frappe.db.set_value("User", "Administrator", "tenant_id",
                        "SYSTEM", update_modified=False)
    frappe.db.commit()
    print("Set Administrator tenant_id = SYSTEM")


def setup_user_tenant():
    """Complete setup for user-tenant linking"""
    add_tenant_id_to_user()
    set_administrator_tenant_id()
    print("\n✅ User-Tenant linking setup complete")
