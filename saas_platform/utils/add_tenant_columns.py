"""Utility to add tenant_id columns to all tables"""
import frappe


def add_tenant_id_columns():
    """Add tenant_id column to all DocType tables"""

    # Get all tables directly from database
    tables = frappe.db.sql("""
        SELECT TABLE_NAME 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME LIKE 'tab%'
        AND TABLE_TYPE = 'BASE TABLE'
    """, as_dict=True)

    tables_updated = []
    tables_skipped = []

    for table in tables:
        table_name = table.TABLE_NAME

        # Check if column already exists
        columns = frappe.db.sql(f"""
            SELECT COLUMN_NAME 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = '{table_name}' 
            AND COLUMN_NAME = 'tenant_id'
        """)

        if not columns:
            try:
                # Add tenant_id column
                frappe.db.sql(f"""
                    ALTER TABLE `{table_name}` 
                    ADD COLUMN tenant_id VARCHAR(255)
                """)

                # Create index
                frappe.db.sql(f"""
                    CREATE INDEX idx_tenant_id ON `{table_name}`(tenant_id)
                """)

                tables_updated.append(table_name)
                print(f"✅ Added tenant_id to {table_name}")

            except Exception as e:
                print(f"❌ Error adding tenant_id to {table_name}: {str(e)}")
        else:
            tables_skipped.append(table_name)

    frappe.db.commit()
    print(f"\n✅ Updated {len(tables_updated)} tables")
    print(f"⏭️  Skipped {len(tables_skipped)} tables (already have tenant_id)")
    return tables_updated
