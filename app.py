from flask import Flask, render_template, request  
import openai  
app = Flask(__name__)  

@app.route('/', methods=['GET', 'POST'])  # Определяем маршрут для главной страницы, поддерживает GET и POST
def index():
    answer = ''      # Переменная для хранения ответа от AI
    api_key = ''     # Переменная для хранения API ключа
    question = ''    # Переменная для хранения вопроса пользователя
    if request.method == 'POST':  # Если форма отправлена методом POST
        api_key = request.form.get('api_key', '')      # Получаем API ключ из формы
        question = request.form.get('question', '')    # Получаем вопрос из формы
        if api_key and question:  # Если оба поля заполнены
            try:
                client = openai.OpenAI(api_key=api_key)  # Создаём клиента OpenAI с введённым API ключом
                response = client.chat.completions.create(  # Отправляем запрос к модели GPT
                    model="gpt-3.5-turbo",                # Указываем модель
                    messages=[{"role": "user", "content": question}]  # Передаём вопрос пользователя
                )
                answer = response.choices[0].message.content  # Извлекаем ответ из результата
            except Exception as e:
                answer = f"Ошибка: {str(e)}"  # В случае ошибки выводим её текст
        else:
            answer = 'Пожалуйста, введите API ключ и вопрос.'  # Если не все поля заполнены
    return render_template('index.html', answer=answer, api_key=api_key, question=question)

if __name__ == '__main__':  
    app.run(debug=True)  