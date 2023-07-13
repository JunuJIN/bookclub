### 텍스트 전처리 고도화 필요
import os
import pandas as pd

from konlpy.tag import Kkma

from extract import read_pdf, read_epub
from base import checker1
from add1 import checker2
from add2 import checker3
from complex import checker4
from score import score

path_dir = "D:/data"
file_list = os.listdir(path_dir)

kkma = Kkma()
tagger = Kkma()

total_total_list = []

for file in file_list[:400]:
    try:
        if file[-3:] == "pdf":
            text_list = kkma.sentences(read_pdf(path_dir + "/" + file))
            sent_list = text_list[
                int(len(text_list) * 0.15) : int(len(text_list) * 0.85)
            ]
        if file[-3:] == "pub":
            sent_list = read_epub(path_dir + "/" + file)
        if len(sent_list) > 6:
            sample_sent = sent_list[:5]
        elif len(sent_list) > 0:
            sample_sent = sent_list
        else:
            sample_sent = ["no_sent"]
        print(path_dir + "/" + file)
        print("==============================")
        # 문장들 하나하나로 구성된 리스트에서 하나씩 뽑아서 tag붙이고, 기본조건/첨가1/첨가2 모듈 돌리기

        # 도서 하나의 문장에 대한 결과값을 여기에 모아서,
        # 결국에는 그것을 df시켜서,
        # 각종 통계값(총갯수, 종합점수에 대한 분위값들)을 계산하여,
        # total_total_list에 담아서 csv저장
        # total_list는 도서에 대한 데이터
        total_list = []

        for j in sent_list:
            token = tagger.pos(j)
            # 토큰 결과를 tag와 word를 각자의 리스트로 저장
            token_word = ["0", "0", "0", "0"]
            token_tag = ["0", "0", "0", "0"]
            for i in token:
                token_word.append(i[0])
                token_tag.append(i[1])
            token_word.append("0")
            token_word.append("0")
            token_word.append("0")
            token_word.append("0")
            token_tag.append("0")
            token_tag.append("0")
            token_tag.append("0")
            token_tag.append("0")

            ## 각 문장에 대해서 word, tag리스트 완성
            ## token_word, token_tag

            result_list = (
                checker1(token_tag, token_word, token)
                + checker2(token_tag, token_word)
                + checker3(token_tag, token_word)
            )
            result_list[5] = result_list[5] + checker4(j)
            result_list.append(score(result_list))
            # result_list는 각 문장에 대해서 진행하였고,
            total_list.append(result_list)
            # total_list는 특정

        col_name = [
            "sub",
            "obj",
            "comp",
            "cand",
            "pred",
            "adnom",
            "adv",
            "indep",
            "quot_c",
            "adnom_c",
            "noun_c",
            "adv_c",
            "score",
        ]
        tmp_df = pd.DataFrame(total_list, columns=col_name)
        tmp_list = []
        tmp_list.append(file)
        tmp_list.append(tmp_df["sub"].mean())
        tmp_list.append(tmp_df["obj"].mean())
        tmp_list.append(tmp_df["comp"].mean())
        tmp_list.append(tmp_df["cand"].mean())
        tmp_list.append(tmp_df["pred"].mean())
        tmp_list.append(tmp_df["adnom"].mean())
        tmp_list.append(tmp_df["adv"].mean())
        tmp_list.append(tmp_df["indep"].mean())
        tmp_list.append(tmp_df["quot_c"].mean())
        tmp_list.append(tmp_df["adnom_c"].mean())
        tmp_list.append(tmp_df["noun_c"].mean())
        tmp_list.append(tmp_df["adv_c"].mean())
        tmp_list.append(tmp_df["score"].quantile(0.5))
        tmp_list.append(tmp_df["score"].quantile(0.7))
        tmp_list.append(tmp_df["score"].quantile(0.8))
        tmp_list.append(tmp_df["score"].quantile(0.9))
        tmp_list.append(tmp_df["score"].quantile(1.0))
        tmp_list.append(tmp_df["score"].mean())
        tmp_list.append(tmp_df["score"].std())
        tmp_list.append(tmp_df["score"].count())
        tmp_list.append(sample_sent)
        total_total_list.append(tmp_list)
        print(tmp_list)
    except Exception as e:
        print(e)
        total_total_list.append(
            [
                file.split(".")[0],
                e,  # 주어 mean 대신에 error코드
                0,  # 목적어 mean
                0,  # 보어 mean
                0,  # 보조사 mean
                0,  # 서술어 mean
                0,  # 관형어 mean
                0,  # 부사어 mean
                0,  # 독립어 mean
                0,  # 인용절 mean
                0,  # 관형절 mean
                0,  # 명사절 mean
                0,  # 부사절 mean
                0,  # 5분위 점수
                0,  # 7분위 점수
                0,  # 8분위 점수
                0,  # 9분위 점수
                0,  # 10분위 점수
                0,  # 평균
                0,  # 표준편차
                0,  # 총문장수
                [],  # 문장이 존재하지 않는다.
            ]
        )

col_name = [
    "bookcode",
    "주어mean",
    "목적어mean",
    "보어mean",
    "보조사mean",
    "서술어mean",
    "관형어mean",
    "부사어mean",
    "독립어mean",
    "인용절mean",
    "관형절mean",
    "명사절mean",
    "부사절mean",
    "5분위점수",
    "7분위점수",
    "8분위점수",
    "9분위점수",
    "10분위점수",
    "평균",
    "표준편차",
    "추출문장수",
    "샘플문장",
]
df = pd.DataFrame(total_total_list, columns=col_name)
df.to_csv("D:/finalbookclub/result/jdy/result_400.csv", index=None)
