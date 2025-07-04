USE [Palletizer]
GO
/****** Object:  StoredProcedure [dbo].[insert_inventory]    Script Date: 5/30/2025 3:11:07 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
ALTER PROCEDURE [dbo].[insert_inventory]
    @item_upc VARCHAR(13) = NULL,
    @item_model_number VARCHAR(256) = NULL,
    @item_part_number VARCHAR(256) = NULL,
    @item_name VARCHAR(256) = NULL,
    @item_description NVARCHAR(MAX) = NULL,
    @item_price DECIMAL(10, 2) = NULL,
    @items_per_pallet INT = NULL,
    @in_box BIT = NULL,
    @items_per_box INT = NULL,
    @inventory_seller_id INT = NULL,
	@seller_sku VARCHAR(12) = NULL
AS
BEGIN
    SET NOCOUNT ON;
	DECLARE @new_item_table TABLE (
		new_item_id INT
	);
    
    BEGIN TRY
        -- Insert into Inventory table and output the new item_id
        INSERT INTO [dbo].[Inventory] (
            item_upc,
            item_model_number,
            item_part_number,
            item_name,
            item_description,
            item_price,
            items_per_pallet,
            in_box,
            items_per_box
        )
        OUTPUT INSERTED.item_id INTO @new_item_table
        VALUES (
            @item_upc,
            @item_model_number,
            @item_part_number,
            @item_name,
            @item_description,
            @item_price,
            @items_per_pallet,
            @in_box,
            @items_per_box
        );

		DECLARE @new_item_id INT;
		SELECT @new_item_id = new_item_id FROM @new_item_table;

		IF @inventory_seller_id IS NOT NULL OR @inventory_seller_id > 0
		BEGIN
        INSERT INTO [dbo].[SellerSKUs]
        (
            inventory_seller_id,
            item_id,
            seller_sku
        )
        VALUES (
            @inventory_seller_id,
            @new_item_id,
            @seller_sku
        );
		END


    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
        RETURN -1;
    END CATCH
END;
