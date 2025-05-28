-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE [dbo].[insert_inventory]
    @item_upc VARCHAR(12) = NULL,
    @item_model_number VARCHAR(256) = NULL,
    @item_part_number VARCHAR(256) = NULL,
    @item_name VARCHAR(256) = NULL,
    @item_description NVARCHAR(MAX) = NULL,
    @item_price DECIMAL(10, 2) = NULL,
    @items_per_pallet INT = NULL,
    @in_box BIT = NULL,
    @items_per_box INT = NULL,
	@seller_sku VARCHAR(12) = NULL,
    @new_item_id INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
	DECLARE @new_item_id INT;

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
        OUTPUT INSERTED.item_id INTO @new_item_id
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

        -- Return the new item_id
        SELECT @new_item_id = INSERTED.item_id
        FROM INSERTED;
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
GO