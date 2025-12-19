# SaaS Platform

A multi-tenant SaaS foundation for Frappe/ERPNext, designed to manage tenant lifecycle, data isolation, and central authentication.

## Key Responsibilities

- **Multi-Tenant Foundation**: Adds `tenant_id` to all relevant DocTypes (including `User`) to ensure strict row-level data isolation.
- **Central Authentication**: Acts as the Identity Provider (IdP) for the entire ecosystem.
- **Tenant Lifecycle**: Manages the creation of tenants, customer billing accounts, and subscriptions.
- **Core of the Microservice Ecosystem**: Provides the critical `tenant_id` metadata required by the **Frappe Microservice Framework** to perform cross-service authentication and data segregation.

## Documentation

- [Multi-Tenant Architecture](MULTI_TENANT_ARCHITECTURE.md)
- [Implementation Guide](MULTI_TENANT_IMPLEMENTATION.md)
- [Microservice Integration Guide](MICROSERVICE_INTEGRATION.md)

## License

MIT