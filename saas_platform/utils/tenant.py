"""Tenant management utilities"""
import frappe
from frappe import _
import random
import string


def on_session_creation(login_manager):
    """
    Post-login hook to set tenant_id in session.
    Called after user successfully logs in.
    """
    user = login_manager.user

    # Administrator always gets SYSTEM tenant_id
    if user == "Administrator":
        frappe.session['tenant_id'] = "SYSTEM"
        frappe.log(f"Session created for Administrator with tenant_id=SYSTEM")
        return

    # Get tenant_id from User document
    try:
        user_doc = frappe.get_doc("User", user)
        tenant_id = getattr(user_doc, 'tenant_id', None)

        if tenant_id:
            frappe.session['tenant_id'] = tenant_id
            frappe.log(
                f"Session created for {user} with tenant_id={tenant_id}")
        else:
            frappe.log(f"Warning: User {user} has no tenant_id assigned")
    except Exception as e:
        frappe.log_error(f"Failed to get tenant_id for user {user}: {str(e)}")


def set_tenant_id(doc, method=None):
    """Automatically set tenant_id when documents are created"""
    # Skip if user is Administrator (bypass tenant isolation)
    if frappe.session.user == "Administrator":
        return

    # Skip system doctypes that shouldn't have tenant isolation
    system_doctypes = [
        'Usera', 'Role', 'DocType', 'DocField', 'DocPerm', 'Module Def',
        'Domain', 'Domain Settings', 'Tenant', 'Plan', 'aSubscription Plan',
        'Subscription', 'Subscription Plan Detail', 'aCustomer',
        'Workspace', 'Workflow', 'Print Format', 'Email Template',
        'System Settings', 'Website Settings', 'Portal Settings',
        'Error Log', 'Activity Log', 'Version', 'Communication',
        'Comment', 'File', 'Session', 'aToken Cache'
    ]

    if doc.doctype in system_doctypes:
        return

    # Skip if tenant_id is already set
    if getattr(doc, 'tenant_id', None):
        return

    # Get current user's tenant_id from context or user
    tenant_id = frappe.session.get('tenant_id')
    print("Tenant ID in session:", tenant_id)
    if not tenant_id:
        # Try to get tenant_id from the User's default tenant
        try:
            user = frappe.get_doc("User", frappe.session.user)
            if hasattr(user, 'tenant_id') and user.tenant_id:
                tenant_id = user.tenant_id
        except:
            pass

    # Set tenant_id if found
    if tenant_id:
        doc.tenant_id = tenant_id


def generate_tenant_id():
    """Generate a unique tenant ID"""
    while True:
        # Generate a random 8-character alphanumeric ID
        tenant_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=8))

        # Check if it already exists
        if not frappe.db.exists("Tenant", {"tenant_id": tenant_id}):
            return tenant_id


def get_tenant_id():
    """Get the current user's tenant_id"""
    tenant_id = frappe.session.get('tenant_id')

    if not tenant_id:
        user = frappe.get_doc("User", frappe.session.user)
        if hasattr(user, 'tenant_id') and user.tenant_id:
            tenant_id = user.tenant_id
            frappe.session['tenant_id'] = tenant_id

    return tenant_id


def apply_tenant_filter(doc, method=None):
    """Apply tenant filter to queries"""
    tenant_id = get_tenant_id()

    if tenant_id:
        # Allow access to SYSTEM tenant data and own tenant data
        return f"(`tabtenantid` = '{tenant_id}' OR `tab{doc.doctype}`.`tenant_id` = 'SYSTEM' OR `tab{doc.doctype}`.`tenant_id` IS NULL)"

    return None


def get_permission_query_conditions(user, doctype):
    """
    Return SQL conditions for filtering documents by tenant_id.
    Administrator can see all documents.
    Other users can only see their tenant's data + SYSTEM data.
    """
    # Administrator can see everything
    if user == "Administrator":
        return None

    # System doctypes don't get filtered
    system_doctypes = [
        'User', 'Role', 'DocType', 'DocField', 'DocPerm', 'Module Def',
        'Domain', 'Domain Settings', 'Tenant', 'Plan', 'Subscription Plan',
        'Subscription', 'Subscription Plan Detail', 'Customer',
        'Workspace', 'Workflow', 'Print Format', 'Email Template',
        'System Settings', 'Website Settings', 'Portal Settings',
        'Error Log', 'Activity Log', 'Version', 'Communication',
        'Comment', 'File', 'Custom Field'
    ]

    if doctype in system_doctypes:
        return None

    # Get user's tenant_id
    tenant_id = get_tenant_id()

    if not tenant_id:
        # User has no tenant - they can only see SYSTEM data
        return f"(`tab{doctype}`.`tenant_id` = 'SYSTEM' OR `tab{doctype}`.`tenant_id` IS NULL)"

    # User can see their own tenant's data + SYSTEM data
    return f"(`tab{doctype}`.`tenant_id` = '{tenant_id}' OR `tab{doctype}`.`tenant_id` = 'SYSTEM' OR `tab{doctype}`.`tenant_id` IS NULL)"
