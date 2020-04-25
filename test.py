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
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
from pytesseract import Output,image_to_string

# PDF_file = "output.pdf"
# pages = convert_from_path(PDF_file, 500) 
# image_counter = 1
  
# for page in pages: 
#     filename = "page_"+str(image_counter)+".jpg"
#     page.save(filename, 'JPEG') 
#     image_counter = image_counter + 1
  
# filelimit = image_counter-1
# outfile = "out_text2.txt"

f = open("NameFile.txt", "w") 
colorImage  = Image.open("scantron_marked.jpg")
rotated     = colorImage.rotate(45)
transposed  = colorImage.transpose(Image.ROTATE_90)
transposed = transposed.save("rotatedImage.jpg")

img = Image.open("rotatedImage.jpg")
temp = img.crop((614, 41, 1088, 92))
student = temp.save("student.jpg",quality=95)
temp2 = img.crop((607, 95, 905, 150))
subject = temp2.save("subject.jpg",quality=95)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'    
d = pytesseract.image_to_data("student.jpg",output_type=Output.DICT) 
text=d['text']
for t in d['text']:
	if t =="":
		text.remove(t)
print(text)

d = pytesseract.image_to_data("subject.jpg",output_type=Output.DICT) 
text=d['text']
print(text)


# f.write(d) 
f.close() 
