"""Add tenant_id custom fields to core DocTypes"""
import frappe


def add_tenant_custom_fields():
    """Add tenant_id custom field to all core DocTypes that need it"""

    # DocTypes that need tenant_id field
    doctypes_to_customize = [
        'Company', 'Customer', 'Supplier', 'Item', 'Sales Order', 'Purchase Order',
        'Sales Invoice', 'Purchase Invoice', 'Quotation', 'Payment Entry',
        'Journal Entry', 'Delivery Note', 'Purchase Receipt', 'Stock Entry',
        'Lead', 'Opportunity', 'Project', 'Task', 'Issue', 'Contact', 'Address'
    ]

    created_count = 0
    skipped_count = 0

    for doctype in doctypes_to_customize:
        # Check if custom field already exists
        exists = frappe.db.exists('Custom Field', {
            'dt': doctype,
            'fieldname': 'tenant_id'
        })

        if not exists:
            try:
                custom_field = frappe.get_doc({
                    'doctype': 'Custom Field',
                    'dt': doctype,
                    'fieldname': 'tenant_id',
                    'label': 'Tenant ID',
                    'fieldtype': 'Data',
                    'insert_after': 'amended_from',
                    'hidden': 1,
                    'read_only': 1,
                    'no_copy': 1,
                    'print_hide': 1,
                    'report_hide': 1
                })
                custom_field.insert(ignore_permissions=True)
                created_count += 1
                print(f"✅ Added tenant_id custom field to {doctype}")
            except Exception as e:
                print(f"❌ Error adding tenant_id to {doctype}: {str(e)}")
        else:
            skipped_count += 1
            print(f"⏭️  Skipped {doctype} (tenant_id field already exists)")

    frappe.db.commit()
    print(f"\n✅ Created {created_count} custom fields")
    print(f"⏭️  Skipped {skipped_count} DocTypes (already have tenant_id)")

    return created_count
