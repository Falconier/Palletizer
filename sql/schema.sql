CREATE TABLE inventory (
    item_id INTEGER PRIMARY KEY IDENTITY(1,1),     -- Unique identifier for each item
    item_upc VARCHAR(12),            -- UPC code for the item, max 12 digits
    item_model_number VARCHAR(256),       -- Model number of the item
    item_part_number VARCHAR(256),        -- Part number of the item
    item_name VARCHAR(256),               -- Name of the item
    item_description NVARCHAR(MAX),           -- Description of the item
    item_price DECIMAL(10, 2),       -- Price of the item
    items_per_pallet INTEGER,        -- Number of items per pallet
    in_box BIT,                  -- Indicates if items are in a box
    items_per_box INTEGER            -- Number of items per box, nullable if in_box is false
);

CREATE TABLE InventorySellers (
    inventory_seller_id INTEGER PRIMARY KEY IDENTITY(1,1),  -- Unique identifier for each inventory seller            -- Foreign key referencing the item in the inventory table
    seller_name VARCHAR(256),       -- Name of the seller
    seller_url VARCHAR(256) NULL,        -- URL of the seller's website
);

CREATE TABLE SellerSKUs (
    seller_sku_id INTEGER PRIMARY KEY IDENTITY(1,1),  -- Unique identifier for each seller SKU
    inventory_seller_id INTEGER,        -- Foreign key referencing the inventory_sellers table
    item_id INTEGER,               -- Foreign key referencing the inventory table
    seller_sku VARCHAR(256),        -- SKU assigned by the seller
    FOREIGN KEY (inventory_seller_id) REFERENCES InventorySellers(inventory_seller_id),  -- Foreign key constraint
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)  -- Foreign key constraint
);
