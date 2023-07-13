##### 5~-5까지의 텍스트를 긁어온다.
def read_pdf(fname):
    import pdfplumber
    import re

    pattern = r"[^ㄱ-ㅣ가-힣a-zA-Z\s\d\.,?!'%()\\\"“”‘’]"

    pdf = pdfplumber.open(fname)
    x_len = pdf.pages[0].mediabox[2]  # pdf 가로 길이
    y_len = pdf.pages[0].mediabox[3]

    tmp_list = []  # character에 대한 정보를 담을 json 그릇
    for tmp in pdf.pages:
        tmp_list.append(tmp.chars)
    # tmp_list에 chr에 관한 json들이 덕지덕지존재한다.
    # [[page1], [page2], [page3], [page4], ]와 관련된 json들을 담고 있다.

    text = ""
    # 글자를 담을 최종그릇

    for i in tmp_list:
        # chr에 대한 정보를 페이지당 묶어서 가지고 있기 때문에
        for j in i:
            # 이제 각 chr에 대한 json에 대해서 논한다.
            # chr의 위치에 대한 조건을 걸고,
            if (
                j["x0"] > 0
                and j["x0"] < x_len
                and j["x1"] > 0
                and j["x1"] < x_len
                and j["y0"] > 0
                and j["y0"] < y_len
                and j["y1"] > 0
                and j["y1"] < y_len
                and j["top"] > 0
                and j["top"] < y_len
                and j["bottom"] > 0
                and j["bottom"] < y_len
            ):
                # pdfplumber가 인식하지 못하는 text는 고려하지 않는다.
                if "cid" in j["text"]:
                    pass
                else:
                    # 뽑아낸 텍스트에 대해서 전처리
                    clean_text = re.sub(pattern, "", j["text"])
                    clean_text = re.sub("“", '"', clean_text)
                    clean_text = re.sub("”", '"', clean_text)
                    clean_text = re.sub("’", "'", clean_text)
                    clean_text = re.sub("‘", "'", clean_text)
                    clean_text = re.sub("[\uf000-\uFFFF]|[\x01-\x09]", "", clean_text)
                    text += clean_text

    return text


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
    final = text_list[int(len(text_list) * 0.15) : int(len(text_list) * 0.85)]
    # Remove '\n' from the result
    final = [text.replace("\n", "") for text in final]
    final = [text.replace("\t", " ") for text in final]
    real_final = [v for v in final if v]
    return real_final