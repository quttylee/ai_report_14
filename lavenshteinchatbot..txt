import pandas as pd
import gradio as gr

# 레벤슈타인 거리 계산 함수 정의
def levenshtein_distance(s1, s2):
    # 더 긴 문자열이 s1이 되도록 조정
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    # 빈 문자열일 경우 다른 문자열의 길이를 거리로 반환
    if len(s2) == 0:
        return len(s1)
    
    # 초기 거리 행렬 설정
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # 삽입 비용
            deletions = current_row[j] + 1        # 삭제 비용
            substitutions = previous_row[j] + (c1 != c2)  # 변경 비용
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]  # 최종 거리 반환

class LevenshteinChatBot:
    def __init__(self, filepath):
        # CSV 파일 로드 및 질문, 답변 리스트 초기화
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        # CSV 파일 읽기
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문 데이터 추출
        answers = data['A'].tolist()    # 답변 데이터 추출
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 입력된 문장과 기존 질문들과의 레벤슈타인 거리 계산
        distances = [levenshtein_distance(input_sentence, question) for question in self.questions]
        # 가장 거리가 짧은 질문의 인덱스 찾기
        best_match_index = distances.index(min(distances))
        # 해당 인덱스의 답변 반환
        return self.answers[best_match_index]

class ChatHistory:
    def __init__(self):
        self.conversation = []  # 채팅 내역을 저장할 리스트

    def add_message(self, sender, message):
        # 채팅 내역에 메시지 추가 (발신자, 메시지)
        self.conversation.append((sender, message))

    def get_conversation(self):
        # 채팅 내역을 문자열로 변환하여 반환
        return '\n'.join(f'{sender}: {message}' for sender, message in self.conversation)

chat_history = ChatHistory()  # 채팅 내역 인스턴스 생성

def chat(input_sentence):
    # 사용자 입력에 대한 최적의 답변 찾기
    response = chatbot.find_best_answer(input_sentence)
    chat_history.add_message('You', input_sentence)  # 사용자 메시지 추가
    chat_history.add_message('Chatbot', response)    # 챗봇 응답 추가
    return chat_history.get_conversation()  # 현재 채팅 내역 반환

filepath = 'ChatbotData.csv'  # 데이터 파일 경로
chatbot = LevenshteinChatBot(filepath)  # 챗봇 인스턴스 생성

# Gradio 인터페이스 설정 및 실행
iface = gr.Interface(fn=chat, inputs=gr.Textbox(lines=2), outputs=gr.Textbox())
iface.launch()
