-- Schema gerado automaticamente a partir dos arquivos CSV.
-- Banco de destino: PostgreSQL.
-- Script gerado usando apenas bibliotecas padrao do Python 3.

-- Arquivo fonte: addresses.csv
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER,
    customer_id INTEGER,
    address_type TEXT,
    postal_code TEXT,
    street TEXT,
    number INTEGER,
    complement TEXT,
    district TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    is_primary BOOLEAN
);

-- Arquivo fonte: attributes.csv
CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER,
    name TEXT,
    data_type TEXT
);

-- Arquivo fonte: brands.csv
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER,
    name TEXT,
    country TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: categories.csv
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER,
    name TEXT,
    slug TEXT,
    parent_category_id INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: customers.csv
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER,
    person_type TEXT,
    legal_name TEXT,
    trade_name TEXT,
    tax_id TEXT,
    state_registration TEXT,
    email TEXT,
    phone TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: employees.csv
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER,
    full_name TEXT,
    cpf TEXT,
    email TEXT,
    role TEXT,
    primary_location_id INTEGER,
    hire_date TIMESTAMP,
    termination_date TIMESTAMP,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: fiscal_invoices.csv
CREATE TABLE IF NOT EXISTS fiscal_invoices (
    id INTEGER,
    order_id INTEGER,
    nfe_number TEXT,
    nfe_access_key INTEGER,
    series INTEGER,
    issued_at TIMESTAMP,
    status TEXT,
    total_amount NUMERIC(8, 2),
    xml_storage_uri TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: goods_receipt_items.csv
CREATE TABLE IF NOT EXISTS goods_receipt_items (
    id INTEGER,
    goods_receipt_id INTEGER,
    purchase_order_item_id INTEGER,
    quantity_received NUMERIC(4, 2)
);

-- Arquivo fonte: goods_receipts.csv
CREATE TABLE IF NOT EXISTS goods_receipts (
    id INTEGER,
    purchase_order_id INTEGER,
    received_by_employee_id INTEGER,
    received_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP
);

-- Arquivo fonte: locations.csv
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER,
    name TEXT,
    location_type TEXT,
    postal_code TEXT,
    street TEXT,
    number INTEGER,
    complement TEXT,
    district TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: order_items.csv
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER,
    order_id INTEGER,
    product_variant_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(6, 2),
    icms_rate NUMERIC(2, 0),
    ipi_rate NUMERIC(2, 0),
    line_total NUMERIC(7, 2)
);

-- Arquivo fonte: orders.csv
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER,
    order_number TEXT,
    channel TEXT,
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id INTEGER,
    status TEXT,
    subtotal NUMERIC(8, 2),
    discount_amount NUMERIC(7, 2),
    total NUMERIC(8, 2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: payments.csv
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER,
    order_id INTEGER,
    method TEXT,
    installments INTEGER,
    amount NUMERIC(8, 2),
    status TEXT,
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: product_suppliers.csv
CREATE TABLE IF NOT EXISTS product_suppliers (
    product_variant_id INTEGER,
    supplier_id INTEGER,
    supplier_sku TEXT,
    last_quoted_cost NUMERIC(6, 2),
    lead_time_days INTEGER,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: product_variants.csv
CREATE TABLE IF NOT EXISTS product_variants (
    id INTEGER,
    product_id INTEGER,
    sku TEXT,
    barcode_ean INTEGER,
    sale_price NUMERIC(6, 2),
    cost_price NUMERIC(6, 2),
    weight_kg NUMERIC(5, 3),
    icms_rate NUMERIC(2, 0),
    ipi_rate NUMERIC(2, 0),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: products.csv
CREATE TABLE IF NOT EXISTS products (
    id INTEGER,
    name TEXT,
    description TEXT,
    brand_id INTEGER,
    category_id INTEGER,
    ncm_code TEXT,
    unit_of_measure TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: purchase_order_items.csv
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id INTEGER,
    purchase_order_id INTEGER,
    product_variant_id INTEGER,
    quantity_ordered INTEGER,
    unit_cost NUMERIC(6, 2),
    line_total NUMERIC(8, 2)
);

-- Arquivo fonte: purchase_orders.csv
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER,
    po_number TEXT,
    supplier_id INTEGER,
    buyer_id INTEGER,
    destination_location_id INTEGER,
    status TEXT,
    currency TEXT,
    subtotal NUMERIC(8, 2),
    total NUMERIC(8, 2),
    placed_at TIMESTAMP,
    expected_delivery_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: return_items.csv
CREATE TABLE IF NOT EXISTS return_items (
    id INTEGER,
    return_id INTEGER,
    order_item_id INTEGER,
    quantity NUMERIC(2, 0),
    action TEXT,
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(6, 2)
);

-- Arquivo fonte: returns.csv
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER,
    return_number TEXT,
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id INTEGER,
    status TEXT,
    reason TEXT,
    total_refund_amount NUMERIC(7, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: stock_levels.csv
CREATE TABLE IF NOT EXISTS stock_levels (
    product_variant_id INTEGER,
    location_id INTEGER,
    quantity_on_hand NUMERIC(4, 2),
    reorder_point TEXT,
    updated_at TIMESTAMP
);

-- Arquivo fonte: stock_movements.csv
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER,
    product_variant_id INTEGER,
    location_id INTEGER,
    movement_type TEXT,
    quantity NUMERIC(5, 2),
    reference_table TEXT,
    reference_id INTEGER,
    employee_id INTEGER,
    notes TEXT,
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

-- Arquivo fonte: suppliers.csv
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER,
    legal_name TEXT,
    trade_name TEXT,
    country TEXT,
    tax_id TEXT,
    tax_id_type TEXT,
    email TEXT,
    phone TEXT,
    contact_name TEXT,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Arquivo fonte: variant_attribute_values.csv
CREATE TABLE IF NOT EXISTS variant_attribute_values (
    product_variant_id INTEGER,
    attribute_id INTEGER,
    value TEXT
);
