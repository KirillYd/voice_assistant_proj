import json
import threading
import time

import tools
from tools import *
from appform import App


tags_id = json.load(open("tags_id.json", 'r', encoding='utf-8'))
cities_id = json.load(open("cities_id.json", 'r', encoding='utf-8'))
it_tags = [".NET", "Автоматизация процессов", "Кибербезопасность", "Операционист", "C#", "Data science",
           "DevMLOps", "Docker", "Kubernetes", "ML", "Mlops", "Python", "SQL"]
analytics_tags = ["Анализ финансово-хозяйственной деятельности", "Аналитик", "Аналитик SQL", "Аналитика",
                  "Бизнес-аналитик", "Кредитный аналитик", "Финансовые риски", "Финансовый анализ",
                  "Финансовый аналитик"]
bank_tags = ['Автокредитование', "Активные продажи", "Банк", "Залоговое кредитование", "Ипотека",
             "Инвестиции", "Инвестиционный аналитик", "Работа в банке", "Услуги для бизнеса",
             "СКБ", "Портфельный анализ", "Залоговое кредитование", "Банковские гарантии"]
client_tags = ["Взыскание просроченной задолженности", "Консультация клиентов", "Ключевые клиенты",
               "Поддержка клиентов", "Продажи по телефону", "Привлечение клиентов", "Привлечение партнеров",
               "Call-центр", "Холодные звонки", "Премиум клиенты"]

main_phrases = {
    0: f"Здравствуйте, я помогу вам в выборе вакансии. Как я могу к Вам обращаться?",
    1: f"Вы из города {location()}?",
    2: f"Выберите Вашу сферу деятельности из списка:",
    3: f"Выберите подкатегорию.",
    4: f"Укажите ваш опыт работы.",
    5: f"Идет подбор вакансий...",
}

extra_phrases = {
    0: '',
    1: f"Пожалуйста, введите Ваш город.",
    2: '',
    3: '',
    4: '',
    5: '',
}

button_content = {
    0: '',
    1: ['Да', 'Нет'],
    2: ['IT   \n', 'Аналитикa\n', 'Кредиты и \nИнвестиции', 'Работа с \nклиентами'],
    3: [it_tags, analytics_tags, bank_tags, client_tags],
    4: ["Без\n опыта", "До 1\nгода", "От 1 до\n 5 лет", "Больше \n5 лет"],
    5: '',
}

job_group = ['IT   \n', 'Аналитикa\n', 'Кредиты и \nИнвестиции', 'Работа с \nклиентами']
answers_list = []


def wait_answer(application):
    while application.answer == None:
        time.sleep(1)
    answers_list.append(application.answer)


def get_data(answers, dict_values):
    for item in answers:
        if item in dict_values:
            return item, dict_values[item]
    return None, None


def dialog(counter, application):
    while True:

        application.add_label(1, main_phrases[counter])
        if counter == 5:
            time.sleep(2)
            break
        if button_content[counter]:
            print(counter)
            if len(answers_list) > 0 and answers_list[-1] in job_group:
                application.add_button(button_content[counter][job_group.index(answers_list[-1])], 2)
            else:
                application.add_button(button_content[counter], 1)

        extra_thread = threading.Thread(target=wait_answer, args=(application, ))
        extra_thread.start()
        extra_thread.join()

        if extra_phrases[counter] and application.answer == "Нет":
            application.add_label(1, extra_phrases[counter])
            application.answer = None
            extra_thread = threading.Thread(target=wait_answer, args=(application, ))
            extra_thread.start()
            extra_thread.join()

        counter += 1
        application.answer = None

    _, tag_id = get_data(answers_list, tags_id)
    city, city_id = (city_translate(tools.location()), cities_id[tools.location().strip()]) if get_data(answers_list,
                                                                                                      cities_id) == (
                                                                                             None, None) else get_data(
        answers_list, cities_id)
    application.return_link(tag_id, city_id, city)

    application.add_label(1, 'Хотите выбрать что-то другое?')
    application.add_button(['Да', 'Нет'], 1)

    extra_thread = threading.Thread(target=wait_answer, args=(application, ))
    extra_thread.start()
    extra_thread.join()

    if answers_list[-1] == 'Да':
        application.answer = None
        answers_list.clear()
        dialog(2, application)
    application.destroy()


# if __name__ == "__main__":
def main():
    application = App()
    count = 0
    thread1 = threading.Thread(target=dialog, args=(count, application))
    thread1.start()
    application.mainloop()


