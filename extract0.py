## pdf, epub에서 텍스트를 긁어오는 함수
def read_pdf(file_path):
    import re
    import fitz

    doc = fitz.open(path)
    text = ""

    for i in range(len(doc)):
        text += doc.get_page_text(i)
    clean_text = re.sub("\d{0,3}\n\d{0,3}", "", text)
    clean_text = re.sub("“", '"', clean_text)
    clean_text = re.sub("”", '"', clean_text)
    clean_text = re.sub("’", "'", clean_text)
    clean_text = re.sub("‘", "'", clean_text)

    refined = re.findall("(?<=[^가-힣])[가-힣0-9\,\\s]+[\.\?\!]", clean_text)
    processed = [element.strip() for element in refined if re.search("[가-힣]", element)]
    text_list = [t for t in processed if len(t.strip()) > 5]
    final = text_list[int(len(text_list) * 0.3): int(len(text_list) * 0.7)]

    return final


def read_epub(file_path):
    import re
    from bs4 import BeautifulSoup
    from ebooklib import epub
    import ebooklib

    book = epub.read_epub(file_path)
    raw_text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapter = item.get_content().decode("utf-8")
            soup = BeautifulSoup(chapter, "html.parser")
            raw_text += soup.get_text() + "\n"
    refined = re.findall("(?<=[^가-힣])[가-힣0-9\,\\s]+[\.\?\!]", raw_text)
    processed = [element.strip() for element in refined if re.search("[가-힣]", element)]
    text_list = [t for t in processed if len(t.strip()) > 5]
    final = text_list[int(len(text_list) * 0.15): int(len(text_list) * 0.85)]
    # Remove '\n' from the result
    final = [text.replace("\n", "") for text in final]
    final = [text.replace("\t", " ") for text in final]
    real_final = [v for v in final if v]
    return real_final
