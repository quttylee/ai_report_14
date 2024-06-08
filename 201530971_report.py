import pandas as pd
#레벤슈타인 거리 구하기
def calc_distance(a,b):
        
    if a == b: return 0
    a_len = len(a) 
    b_len = len(b) 
    if a == "": return b_len
    if b == "": return a_len 
    matrix = [[] for i in range(a_len+1)] 
    for i in range(a_len+1): 
        matrix[i] = [0 for j in range(b_len+1)] 
    for i in range(a_len+1):
        matrix[i][0] = i
    for j in range(b_len+1):
        matrix[0][j] = j
    for i in range(1, a_len+1):
        ac = a[i-1]
    for j in range(1, b_len+1):
        bc = b[j-1]
        cost = 0 if (ac == bc) else 1  #  파이썬 조건 표현식 예:) result = value1 if condition else value2
        matrix[i][j] = min([
            matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
            matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1
            matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
        ])
    return matrix[a_len][b_len]

class SimpleChatBot():
    
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
        
#csv파일로부터 질문과 답변 데이터를 불러오는 메서드
    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers   
    
#입력문장에 가장 잘 맞는 댭변을 찾는 메서드,
#입력문장과 기존 데이터 질문문장과의 레벤슈타인거리를 이용한 문장유사도 분석하여
#가장 높은 유사도를 가진 질문의 답변을 반환함
    def find_best_answer(self, input_sentence):
    
        samples = [calc_distance(input_sentence,question) for question in self.questions]
        best_match_index = samples.index(min(samples))
        return self.answers[best_match_index] #chat의 질문과 레벤슈타인 거리와 가장 유사한 학습데이터의 질문의 인덱스를 구하기   
            
    
#CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    
    if input_sentence.lower() == '종료':
        break
    
    response = chatbot.find_best_answer(input_sentence)
    print ('Chatbot:', response )#학습 데이터의 인덱스의 답을 chat의 답변을 채택한 뒤 출력
    
