# SaaS Platform

A Frappe-based multi-tenant SaaS platform with automated site provisioning and trial management.

## Overview

This application enables customers to self-register for isolated Frappe/ERPNext instances. The platform automates:

- **Tenant Registration**: Self-service signup via web form
- **Site Provisioning**: Automated creation of new Frappe sites with ERPNext
- **Trial Management**: 14-day trial periods with automatic expiration
- **Lifecycle Management**: Status tracking (Trial → Active → Suspended)
- **Email Notifications**: Automated reminders before trial expiry

## Key Features

### For End Users
- Self-service registration with custom subdomain
- Instant provisioning of Frappe/ERPNext instance
- 14-day free trial period
- Email notifications before trial expiration

### For Platform Administrators
- Centralized tenant management through Frappe DocType
- Automated trial suspension for expired accounts
- Subscription tracking field
- Administrative notes and status management

## Architecture

The application consists of:

- **Backend**: Frappe Python app with Tenant DocType and background tasks
- **Frontend**: Vue.js application with registration and authentication
- **Provisioning**: Automated Frappe site creation using bench commands

For detailed architecture and billing system documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Quick Start

### Backend Setup

1. Install this app in your Frappe bench:
   ```bash
   bench get-app saas_platform
   bench install-app saas_platform
   ```

2. Enable scheduled tasks in `hooks.py` (uncomment scheduler_events)

### Frontend Development

1. Navigate to frontend directory:
   ```bash
   cd frontend
   yarn install
   ```

2. Add to `site_config.json`:
   ```json
   {
     "ignore_csrf": 1
   }
   ```

3. Start development server:
   ```bash
   yarn dev
   ```

4. Access at `http://[your-site]:8080/frontend`

## Billing System

**Note**: The current implementation includes basic trial management and a subscription field, but does **not** include:
- Payment gateway integration
- Automated billing or invoicing  
- Subscription plans or pricing tiers
- Payment processing UI

The subscription field is manually managed. See [ARCHITECTURE.md](./ARCHITECTURE.md) for details on implementing full billing functionality.

## License

MIT