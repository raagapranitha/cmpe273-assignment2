# import os
# import img2pdf
# import binascii
# from PIL import Image
# from io import BytesIO
# #from pdf2image import convert_from_path, convert_from_bytes
# with open("output.pdf", "wb") as f:
#     f.write(img2pdf.convert([i for i in os.listdir('.') if i.endswith(".jpg")]))
# with open("output.pdf", "rb") as binaryfile :
#     with open("readfile.raw", "wb") as newFile:
#         while True:
#             chunk = binaryfile.read(4096)
#             if not chunk:
#                 break
#             newFile.write(binascii.hexlify(chunk))
# with open("readfile.raw") as f:
#    data = f.read()
# b_data = binascii.unhexlify(data)
# stream = stream = BytesIO(b_data)
# image = Image.open(stream).convert("RGBA")
# stream.close()
# image.show()

#     value = f.read()

# cmap = {'0': (255,255,255),
#         '1': (0,0,0)}

# data = [cmap[letter] for letter in value]
# img = Image.new('RGB', (8, len(value)//8), "white")
# img.putdata(data)
# img.save('bnary_img.png','PNG')
# img.show()        
import copy

dict_from_post = {}
dict_to_database= {}
test_id = 1 
dict_to_database['answer'] = 'A'
dict_from_post['test_id'] = test_id
dict_from_post['subject'] = 'cmpe'
temp = dict(dict_to_database)
temp.update(dict_from_post)
dict_to_database = temp
dict_from_post['name'] = 'sara'


print(dict_to_database)
print(dict_from_post)
