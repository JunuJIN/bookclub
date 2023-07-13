# 초기 버전
def read_pdf(file_path):
    import re
    from pdfminer.high_level import extract_text

    raw_text = extract_text(file_path)
    refined = re.findall("(?<=[^가-힣])[가-힣0-9\,\\s]+[\.\?\!]", raw_text)
    processed = [element.strip() for element in refined if re.search("[가-힣]", element)]
    text_list = [t for t in processed if len(t.strip()) > 5]
    final = text_list[int(len(text_list) * 0.3) : int(len(text_list) * 0.7)]
    # Remove '\n' from the result
    final = [text.replace("\n", "") for text in final]
    final = [text.replace("\t", " ") for text in final]
    real_final = [v for v in final if v]
    return real_final


def read_epub(file_path):
    import re
    from bs4 import BeautifulSoup
    from ebooklib import epub
    import ebooklib

    book = epub.read_epub(file_path)
    raw_text = ""
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapter = item.get_content()
            soup = BeautifulSoup(chapter, "html.parser")
            raw_text += soup.get_text() + "\n"
    refined = re.findall("(?<=[^가-힣])[가-힣0-9\,\\s]+[\.\?\!]", raw_text)
    processed = [element.strip() for element in refined if re.search("[가-힣]", element)]
    text_list = [t for t in processed if len(t.strip()) > 5]
    final = text_list[int(len(text_list) * 0.3) : int(len(text_list) * 0.7)]
    # Remove '\n' from the result
    final = [text.replace("\n", "") for text in final]
    final = [text.replace("\t", " ") for text in final]
    real_final = [v for v in final if v]
    return real_final
