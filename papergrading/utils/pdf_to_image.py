import fitz

# pdf_path = "C:/code base/Main pro/gradeeaseeee/test/codetest/s.pdf"
# out_path = "C:/code base/Main pro/gradeeaseeee/test/codetest"

def pdf_to_img(pdf_path: str,out_path: str) -> list:
    image_paths = []
    pdf = fitz.open(pdf_path)
    # print("Total number of pages in PDF:", len(pdf))
    for num in range(pdf.page_count):
        # print("Processing page:", num+1)
        page = pdf.load_page(num)
        image = page.get_pixmap()
        image_path = f"{out_path}/page_{num+1}.jpg"
        image.save(image_path)
        image_paths.append(image_path)
        # print("Image content:", image)
    pdf.close()
    return image_paths

# images = pdf_to_img(pdf_path=pdf_path, out_path=out_path)

# for img in images:
#     print(img)
