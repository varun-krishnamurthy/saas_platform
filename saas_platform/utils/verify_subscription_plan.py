import frappe


def verify_plan():
    """Verify the subscription plan was created"""
    frappe.init(site="dev.localhost")
    frappe.connect()
    frappe.set_user("Administrator")

    print("\n=== Subscription Plans ===")
    plans = frappe.get_all("Subscription Plan",
                           fields=["name", "plan_name", "cost",
                                   "billing_interval", "item"],
                           limit_page_length=10
                           )

    if plans:
        for plan in plans:
            print(f"Plan: {plan.plan_name}")
            print(f"  Name: {plan.name}")
            print(f"  Cost: ${plan.cost}")
            print(f"  Billing: {plan.billing_interval}")
            print(f"  Item: {plan.item}")
            print()
    else:
        print("No Subscription Plans found")

    print("\n=== Tenants ===")
    tenants = frappe.get_all("Tenant",
                             fields=["name", "tenant_id",
                                     "tenant_name", "current_plan", "status"],
                             limit_page_length=10
                             )

    if tenants:
        for tenant in tenants:
            print(f"Tenant: {tenant.tenant_name}")
            print(f"  ID: {tenant.tenant_id}")
            print(f"  Plan: {tenant.current_plan}")
            print(f"  Status: {tenant.status}")
            print()
    else:
        print("No Tenants found")

    frappe.destroy()
