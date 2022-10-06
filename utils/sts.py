from pororo import Pororo
sts = Pororo(task="similarity", lang='ko')

print(sts("왕이 내게 이르시되 그러면 네가 무엇을 원하느냐 하시기로 내가 곧 하늘의 하나님께 묵도하고", "그 다음은 학고스의 손자 우리아의 아들 므레못이 중수하였고 그 다음은 므세사벨의 손자 베레갸의 아들 므술람이 중수하였고 그 다음은 바아나의 아들 사독이 중수하였고"))

# def chat(sent="0"):
#   while 1:
#     q = input("user > ").strip()
#     if q == "quit":
#       break
#     a = ""
#     # Pororo Sentense Embedding으로 텍스트 유사도를 구합니다.
#     q = sTe(q)
#     # 질문을 Tensor로 바꿉니다.
#     q = torch.tensor(q)
#     # 코사인 유사도 
#     cos_sim = util.pytorch_cos_sim(q, EmbData)

#     #유사도가 가장 비슷한 질문 인덱스를 구합니다.
#     best_sim_idx = int(np.argmax(cos_sim))

#     # 질문의 유사도와 가장 비슷한  답변 제공
#     answer = Chatbot_Data['A'][best_sim_idx]
#     print(answer)

# chat