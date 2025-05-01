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

--sellers table
seller_id
seller_name
seller_url

--seller locations table -- for each seller (not needed right now)
seller_location_id
seller_location_name
seller_location_address
seller_location_city
seller_location_state
seller_location_zip



-- INSERT INTO inventory (
--     item_upc, 
--     item_model_number, 
--     item_part_number, 
--     item_name, 
--     item_description, 
--     item_price, 
--     items_per_pallet, 
--     in_box, 
--     items_per_box
-- ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);