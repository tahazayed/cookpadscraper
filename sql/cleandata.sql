use Meals
GO

update Ingredients set cleanedTxt=txt

update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'كاس',N'كأس')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'ملعقه',N'ملعقة')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'كبيره',N'كبيرة')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'صغثره',N'صغيرة')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'طحين',N'دقيق')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'حليب',N'للبن')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'كوب',N'كاس')
--update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'أ',N'ا')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')
update Ingredients set cleanedTxt=REPLACE(cleanedTxt,N'  ',N' ')

update Ingredients set parsed=0



update Ingredients set parsed=1,amount=left(cleanedTxt,CHARINDEX(N' ملعقة كبيرة',cleanedTxt)),unit=N'ملعقة كبيرة' WHERE CHARINDEX(N' ملعقة كبيرة',cleanedTxt)>0 and parsed=0
update Ingredients set parsed=1,amount=1,unit=N'ملعقة كبيرة' WHERE CHARINDEX(N'ملعقة كبيرة',cleanedTxt)>0 and parsed=0

update Ingredients set parsed=1,amount=left(cleanedTxt,CHARINDEX(N' ملعقة صغيرة',cleanedTxt)),unit=N'ملعقة صغيرة' WHERE CHARINDEX(N' ملعقة صغيرة',cleanedTxt)>0 and parsed=0
update Ingredients set parsed=1,amount=1,unit=N'ملعقة صغيرة' WHERE CHARINDEX(N'ملعقة صغيرة',cleanedTxt)>0 and parsed=0

update Ingredients set parsed=1,amount=left(cleanedTxt,CHARINDEX(N' ملعقة',cleanedTxt)),unit=N'ملعقة' WHERE CHARINDEX(N' ملعقة',cleanedTxt)>0 and parsed=0
update Ingredients set parsed=1,amount=1,unit=N'ملعقة' WHERE CHARINDEX(N'ملعقة',cleanedTxt)>0 and parsed=0


update Ingredients set parsed=1,amount=left(cleanedTxt,CHARINDEX(N' كأس',cleanedTxt)),unit=N'كأس' WHERE CHARINDEX(N' كأس',cleanedTxt)>0 and parsed=0
update Ingredients set parsed=1,amount=1,unit=N'كأس' WHERE CHARINDEX(N'كأس',cleanedTxt)>0 and parsed=0

SELECT * FROM Ingredients where cleanedTxt like N'%كأس%'

SELECT * FROM Ingredients where PARSEd=0



