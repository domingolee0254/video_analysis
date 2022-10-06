# correct_result.py
def leven(aText,bText):
    aLen = len(aText)+1
    bLen = len(bText)+1
    array = [ [] for a in range(aLen) ]
    for i in range(aLen):
        array[i] = [0 for a in range(bLen)]
    for i in range(bLen):
        array[0][i] = i
    for i in range(aLen):
        array[i][0] = i
    cost = 0
    for i in range(1,aLen):
        for j in range(1,bLen):
           if aText[i-1] != bText[j-1]:
               cost = 1
           else :
               cost = 0
           addNum = array[i-1][j] + 1 #추가
           minusNum = array[i][j-1] + 1 #감소
           modiNum = array[i-1][j-1]+cost #
           minNum = min([addNum,minusNum,modiNum])
           array[i][j] = minNum

    return array[aLen-1][bLen-1]
## corpus = [ "왕이 내게 이르시되그러면 네가무엇을 원하느나하시기로 나가필하는의하가부지 묵도하고", "왕이 내게 이르시되 그러면 네가 무엇을 원하느냐 하시기로 내가 곧 하늘의 하나님께 묵도하고", "왕이나가필하는의하가부지내게이르시되그러면묵도하고네가무엇을원하느나하시기로", "여호와 하나님이 여자에게 이르시되 네가 어찌하여 이렇게 하였느냐 여자가 이르되 뱀이 나를 꾀므로 내가 먹었나이다","그 다음은 학고스의 손자 우리아의 아들 므레못이 중수하였고 그 다음은 므세사벨의 손자 베레갸의 아들 므술람이 중수하였고 그 다음은 바아나의 아들 사독이 중수하였고"," 아담은 백삼십 세에 자기의 모양 곧 자기의 형상과 같은 아들을 낳아 이름을 셋이라 하였고"]
# result = sorted(corpus, key = lambda x  : leven("왕이나가필하는의하가부지내게이르시되그러면묵도하고네가무엇을원하느나하시기로",x))


# for i in result:
#     print(i, ":",leven("왕이나가필하는의하가부지내게이르시되그러면묵도하고네가무엇을원하느나하시기로",i))
