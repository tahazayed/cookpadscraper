USE [Meals]
GO

/****** Object:  StoredProcedure [dbo].[USP_Recipes_NotFound_insert]    Script Date: 7/2/2017 12:49:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USP_Recipes_NotFound_insert]') AND type in (N'P', N'PC'))
BEGIN
EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE [dbo].[USP_Recipes_NotFound_insert] AS' 
END
GO


ALTER proc [dbo].[USP_Recipes_NotFound_insert]
@src varchar(900)
as


INSERT INTO [dbo].[Recipes_NotFound]
           ([src])
     VALUES
           (@src)


GO

/****** Object:  StoredProcedure [dbo].[USP_Recipes_upsert]    Script Date: 7/2/2017 12:49:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USP_Recipes_upsert]') AND type in (N'P', N'PC'))
BEGIN
EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE [dbo].[USP_Recipes_upsert] AS' 
END
GO




ALTER proc [dbo].[USP_Recipes_upsert]
@json NVARCHAR(MAX)
as


declare @likes int, @n nvarchar(500),@src varchar(900),@img varchar(900),@tags nvarchar(max),@pub datetime,
@_auth  nvarchar(max),@ingrd nvarchar(max),@instrct nvarchar(max),@auth_anme  nvarchar(200),@auth_src varchar(900),@rcpe_id bigint

declare @Author_SID bigint

SELECT
  @n = JSON_VALUE(@json, '$.n'),
  @src=JSON_VALUE(@json, '$.src'),
  @rcpe_id=convert(bigint,JSON_VALUE(@json, '$.rcpe_id')),
  @img=JSON_VALUE(@json, '$.img'),
  @tags=JSON_QUERY(@json, '$.tags'),
  @likes=convert(int,JSON_VALUE(@json, '$.likes')) ,
  @pub=convert(date,JSON_VALUE(@json, '$.pub')),
  @_auth=JSON_QUERY(@json, '$.auth'),
  @ingrd=JSON_QUERY(@json, '$.ingrd'),
  @instrct=JSON_QUERY(@json, '$.instrct')

select @auth_anme=JSON_VALUE(@_auth, '$.n'),@auth_src=JSON_VALUE(@_auth, '$.src')

select top 1 @Author_SID=SID from Authors with(nolock) where src=@auth_src
if(@Author_SID is null)
  begin
    insert Authors(name,src)values(@auth_anme,@auth_src)
	select @Author_SID= SCOPE_IDENTITY()
  end

 MERGE Recipes AS target  
    USING (SELECT @rcpe_id) AS source (rcpe_id)  
    ON (target.rcpe_id = source.rcpe_id)  
    WHEN MATCHED THEN   
        UPDATE SET n = @n,src=@src,img=@img,tags=@tags,likes=@likes,pub=@pub,Author_SID=@Author_SID  
    WHEN NOT MATCHED THEN  
    INSERT  (rcpe_id,n,src,img,tags,likes,pub,Author_SID)  
    VALUES (@rcpe_id,@n,@src,@img,@tags,@likes,@pub,@Author_SID); 


delete Ingredients with(rowlock) where rcpe_id=@rcpe_id

insert Ingredients(OrderNO,txt,rcpe_id)
SELECT OrderNO,txt,@rcpe_id as rcpe_id
FROM OPENJSON(@ingrd)  
  WITH (OrderNO int 'strict $.in', txt nvarchar(500) '$.n')
  
 
delete Instructions with(rowlock) where rcpe_id=@rcpe_id

insert Instructions(OrderNO,txt,img,rcpe_id)
SELECT OrderNO,txt,img,@rcpe_id as rcpe_id
FROM OPENJSON(@instrct)  
  WITH (OrderNO int 'strict $.in', txt nvarchar(500) '$.txt',img varchar(900) '$.img' ) 

update Instructions with(rowlock) set img =null where img=''

GO

/****** Object:  StoredProcedure [dbo].[USP_RecipesSpider_readall]    Script Date: 7/2/2017 12:49:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USP_RecipesSpider_readall]') AND type in (N'P', N'PC'))
BEGIN
EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE [dbo].[USP_RecipesSpider_readall] AS' 
END
GO



ALTER proc [dbo].[USP_RecipesSpider_readall]
as
SELECT url FROM dbo.RecipesSpider with(nolock)
left join Recipes with(nolock) on Recipes.src=RecipesSpider.URL
left join Recipes_NotFound with(nolock) on RecipesSpider.URL=Recipes_NotFound.src
where Recipes.src is null and Recipes_NotFound.src is null
 order by RecipesSpider.SID



GO

/****** Object:  StoredProcedure [dbo].[USP_RecipesSpider_upsert]    Script Date: 7/2/2017 12:49:38 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USP_RecipesSpider_upsert]') AND type in (N'P', N'PC'))
BEGIN
EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE [dbo].[USP_RecipesSpider_upsert] AS' 
END
GO

ALTER proc [dbo].[USP_RecipesSpider_upsert]
@URL nvarchar(900)
as

 MERGE RecipesSpider AS target  
    USING (SELECT @URL) AS source (URL)  
    ON (target.URL = source.URL)  
    WHEN MATCHED THEN   
        UPDATE SET Last_updated=getdate()  
    WHEN NOT MATCHED THEN  
    INSERT  (URL)  
    VALUES (@URL); 


GO


