# Saas Platform Architecture and Billing System

## Overview

This is a **Frappe-based SaaS Platform** application that allows customers to register for multi-tenant instances. The platform automates tenant provisioning, trial period management, and subscription handling.

## What This App Does

The Saas Platform app enables:

1. **Self-Service Tenant Registration**: Users can sign up and get their own isolated Frappe site
2. **Automated Site Provisioning**: Background job creates new Frappe sites with ERPNext installed
3. **Trial Period Management**: Automatic tracking and enforcement of trial periods
4. **Tenant Lifecycle Management**: Status tracking (Trial → Active/Suspended/Deleted)
5. **Email Notifications**: Automated warnings before trial expiration

## Architecture Components

### Backend (Frappe/Python)

#### Core DocType: Tenant

Located in `saas_platform/saas_platform/doctype/tenant/`

**Fields:**
- `tenant_name`: Company/organization name
- `subdomain`: Subdomain for the tenant's site (e.g., "acme" → acme.localhost)
- `admin_email`: Primary contact and administrator email
- `site_name`: Full site name (e.g., acme.localhost)
- `status`: Current state (Active, Suspended, Trial, Deleted)
- `trial_expiry`: Date when the trial period ends
- `subscription`: Subscription plan identifier
- `notes`: Administrative notes

**Status Workflow:**
```
Registration → Trial (14 days) → Active (after subscription)
                              → Suspended (trial expired without subscription)
```

#### API Endpoints

**`/api/method/saas_platform.api.register_user`**

Whitelisted public endpoint for new tenant registration.

**Parameters:**
- `email`: Admin email address
- `company`: Company/tenant name
- `password`: Admin password for the new site
- `subdomain`: Desired subdomain

**Process:**
1. Creates a new Tenant document with status "Trial"
2. Sets trial expiry to 14 days from registration
3. Enqueues background job for site provisioning
4. Returns success response immediately

#### Background Tasks

Located in `saas_platform/tasks.py`

**`provision_site(tenant, password)`**
- Creates a new Frappe site using `bench new-site` command
- Installs ERPNext and saas_platform apps
- Updates tenant record with site name and "Active" status
- Runs as an asynchronous background job

**`suspend_expired_trials()`**
- Scheduled task that checks all Trial tenants
- Compares trial_expiry with current date
- Suspends expired trials by enabling maintenance mode
- Should be configured in scheduler_events (currently commented)

**`suspend_tenant(tenant_name)`**
- Enables maintenance mode on the tenant's site using `bench` command
- Updates tenant status to "Suspended"
- Called automatically for expired trials

**`send_trial_warning_emails()`**
- Checks for trials expiring in 1 or 3 days
- Sends reminder emails to admin_email
- Prompts users to subscribe before suspension

### Frontend (Vue.js)

Located in `frontend/src/`

#### Technology Stack
- **Vue 3**: Frontend framework
- **Vue Router**: Client-side routing
- **Frappe UI**: Component library from Frappe
- **TailwindCSS**: Utility-first CSS framework
- **Vite**: Build tool and dev server

#### Key Components

**`RegisterForm.vue`**
- Public registration form
- Collects email, company name, subdomain, password
- Calls `/api/method/saas_platform.api.register_user`
- Shows success message after provisioning starts

**`Home.vue`**
- Dashboard for logged-in users
- Example of authenticated area
- Demonstrates Frappe API integration

**`Login.vue`**
- Standard Frappe authentication
- Redirects to Home after successful login

## Tenant Billing System

### Current Implementation

The billing system is **partially implemented** with basic trial and subscription tracking:

#### 1. Trial Period
- **Duration**: 14 days from registration
- **Automatic Setup**: Set during tenant creation
- **Storage**: `trial_expiry` field in Tenant doctype
- **Enforcement**: `suspend_expired_trials()` task checks and suspends expired trials

#### 2. Subscription Field
- **Type**: Data (string) field
- **Purpose**: Stores subscription plan identifier
- **Current State**: Basic field without payment integration

#### 3. Status Management
- **Trial**: Initial status for 14 days
- **Active**: Manually set or after subscription (not automated)
- **Suspended**: Set automatically when trial expires
- **Deleted**: For archived tenants

#### 4. Email Notifications
- Warnings sent 3 days and 1 day before trial expiry
- Encourages users to subscribe
- Includes trial expiry date

### How Billing Works (Current Flow)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Registration                                         │
│    - Fill out registration form (email, company, subdomain) │
│    - Submit registration                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Tenant Creation                                           │
│    - Status: "Trial"                                         │
│    - trial_expiry: today + 14 days                           │
│    - subscription: empty                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Site Provisioning (Background)                            │
│    - Create Frappe site: {subdomain}.localhost              │
│    - Install ERPNext + saas_platform                         │
│    - Update status to "Active" (for trial period)            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Trial Period (14 days)                                    │
│    - User has full access to their site                     │
│    - Email warnings at day 11 and day 13                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Trial Expiry Check (Scheduled Task)                       │
│    - Check if trial_expiry < today                           │
│    - If expired and no subscription → Suspend                │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
┌──────────────────┐          ┌──────────────────┐
│ 6a. Suspended    │          │ 6b. Active       │
│     - No access  │          │     - Subscribed │
│     - Maintenance│          │     - Full access│
└──────────────────┘          └──────────────────┘
```

### Billing Limitations (Not Implemented)

The current implementation **does NOT include**:

1. **Payment Integration**: No Stripe, PayPal, or other payment gateway
2. **Subscription Plans**: No pricing tiers or feature limits
3. **Automated Billing**: No recurring charge automation
4. **Invoice Generation**: No invoices or receipts
5. **Usage Metering**: No tracking of users, storage, or API calls
6. **Upgrade/Downgrade**: No plan change functionality
7. **Payment UI**: No frontend for entering payment information
8. **Webhook Handling**: No payment confirmation webhooks
9. **Dunning Management**: No retry logic for failed payments
10. **Prorated Billing**: No mid-cycle plan changes

### What Would Be Needed for Full Billing

To implement complete billing functionality:

#### Payment Integration
```python
# Example additions needed:
- Stripe/PayPal SDK integration
- Payment method storage (tokenized)
- Subscription plan management
- Webhook endpoints for payment events
```

#### Additional DocTypes
```
- Subscription Plan (pricing, features, limits)
- Invoice (amount, date, status, payment_method)
- Payment (transaction records)
- Usage Log (for metered billing)
```

#### Enhanced Tenant Fields
```json
{
  "subscription_plan": "Link to Subscription Plan",
  "billing_email": "Data",
  "payment_method_token": "Data (encrypted)",
  "next_billing_date": "Date",
  "mrr": "Currency (Monthly Recurring Revenue)"
}
```

#### Scheduled Tasks
```python
- generate_monthly_invoices()
- process_subscription_renewals()
- retry_failed_payments()
- calculate_usage_charges()
```

## Configuration and Setup

### Scheduled Tasks

The app includes scheduled task hooks in `hooks.py` but they are **commented out**. To enable automated trial management, uncomment:

```python
scheduler_events = {
    "daily": [
        "saas_platform.tasks.suspend_expired_trials",
        "saas_platform.tasks.send_trial_warning_emails"
    ]
}
```

### Frontend Development

1. Navigate to `frontend/` directory
2. Install dependencies: `yarn install`
3. Start dev server: `yarn dev` (runs on port 8080)
4. Add to `site_config.json`: `"ignore_csrf": 1`

### Production Deployment

- Frontend builds to static files served under `/frontend` route
- Backend runs as standard Frappe app
- Sites are provisioned on the same bench by default

## Security Considerations

1. **Password Handling**: Admin passwords passed to `bench new-site`
2. **Guest Access**: `register_user` API is publicly accessible
3. **Subdomain Validation**: No validation for subdomain availability or format
4. **Resource Limits**: No limits on tenant provisioning rate
5. **CSRF**: Disabled in development mode

## Summary

This Frappe SaaS Platform is a **trial management system** with **basic subscription tracking**. It automates:

- ✅ Tenant self-registration
- ✅ Automated site provisioning with ERPNext
- ✅ 14-day trial period tracking
- ✅ Automatic suspension of expired trials
- ✅ Email notifications before trial expiry
- ⚠️ Basic subscription field (manual entry only)

The billing system is **not fully implemented**. The `subscription` field exists but there is:
- ❌ No payment processing
- ❌ No subscription plans or pricing
- ❌ No automated billing or invoicing
- ❌ No payment UI for end users

**Current State**: The app manages tenant lifecycles and trials effectively but requires manual intervention for actual billing and subscription management.
