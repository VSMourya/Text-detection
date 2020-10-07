# pip install pdf2image

from pdf2image import convert_from_path
pages = convert_from_path('/home/mourya/Desktop/OFFICE/Authbridge/new_tagged_data/part_1/State_Wise_Documents/Karnataka/1675776_5978123.pdf', 500)

#Saving pages in jpeg format
print("ran")
for i,page in enumerate(pages):
    page.save(f'{i}.jpg', 'JPEG')
    break




