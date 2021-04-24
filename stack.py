import pandas as pd
import time
import requests
from datetime import datetime

def getQuestions():
    try:
        question_cols = ['user_id', 'accepted_answer_id', 'answer_count', 'score', 'creation_date', 'question_id',
                         'link', 'title']
        answer_cols = ['question_id', 'answer_id', 'is_accepted', 'body', 'user_id', 'reputation', 'score']


        question_rows = []
        answer_rows = []

        # Set up query parameters
        page_num = "1"
        key = "gXD7eMSe46YvNyXJxKT4*w(("
        limit = 20

        # filter for getting the body of an answer
        filter = "!9Qz3Xr)ML"

        # https://api.stackexchange.com/docs/questions fields used to formulate query string and filter arg
        query = "questions?page=" + page_num + "&pagesize=100&order=desc&sort=activity&site=stackoverflow&filter=!9Qz3Xf4W6&key=" + \
            key

        # Get JSON page response from request
        res = requests.get("https://api.stackexchange.com/2.2/" + query).json()



        # Populate dataframe with question data
        while int(page_num) < limit:
            print(page_num)

            if 'items' not in res:
                questions_df = pd.DataFrame(question_rows)
                answers_df = pd.DataFrame(answer_rows)
                questions_df.to_csv('questions1.csv', index=False)
                answers_df.to_csv('answers1.csv', index=False)
                return

            questions = {}
            answers = {}
            for q in res['items']:
                if q['is_answered'] and 'accepted_answer_id' in q:
                    if 'user_id' in q['owner']:
                        questions['user_id'] = q['owner'].get('user_id')
                    questions['accepted_answer_id'] = q['accepted_answer_id']
                    questions['answer_count'] = q['answer_count']
                    questions['score'] = q['score']
                    questions['creation_date'] = datetime.utcfromtimestamp(q['creation_date']).strftime('%Y-%m-%d')
                    questions['question_id'] = q['question_id']
                    questions['link'] = q['link']
                    questions['title'] = q['title']
                    questions['body'] = q['body']

                    print(q['question_id'])
                    time.sleep(30)
                    # Use the current question_id to get all of its answers
                    query = "questions/" + str(q['question_id']) + "/answers?order=desc&sort=activity&site=stackoverflow&filter=" + filter + "&key=" + key

                    res = requests.get("https://api.stackexchange.com/2.2/" + query)

                    if res is not None:
                        res = res.json()
                    else:
                        questions_df = pd.DataFrame(question_rows)
                        answers_df = pd.DataFrame(answer_rows)
                        questions_df.to_csv('questions1.csv', index=False)
                        answers_df.to_csv('answers1.csv', index=False)
                        return

                    if 'items' not in res:
                        questions_df = pd.DataFrame(question_rows)
                        answers_df = pd.DataFrame(answer_rows)
                        questions_df.to_csv('questions1.csv', index=False)
                        answers_df.to_csv('answers1.csv', index=False)
                        return

                    for a in res['items']:
                        answers['question_id'] = a['question_id']
                        answers['answer_id'] = a['answer_id']
                        answers['is_accepted'] = a['is_accepted']
                        answers['body'] = a['body']
                        if 'user_id' in q['owner']:
                            answers['user_id'] = a['owner'].get('user_id')
                        answers['reputation'] = a['owner'].get('reputation')
                        answers['score'] = a['score']
                        answer_rows.append(answers)
                        print(a['question_id'])
                        answers = {}


            question_rows.append(questions)


            page_num = str(int(page_num) + 1)
            time.sleep(30)

            query = "questions?page=" + str(
                page_num) + "&pagesize=100&order=asc&sort=creation&site=stackoverflow&filter=!9Qz3Xf4W6&key=" + key

            res = requests.get("https://api.stackexchange.com/2.2/" + query)

            if res is not None:
                res = res.json()
            else:
                questions_df = pd.DataFrame(question_rows)
                answers_df = pd.DataFrame(answer_rows)
                questions_df.to_csv('questions1.csv', index=False)
                answers_df.to_csv('answers1.csv', index=False)
                return

        questions_df = pd.DataFrame(question_rows)
        answers_df = pd.DataFrame(answer_rows)
        questions_df.to_csv('questions1.csv', index=False)
        answers_df.to_csv('answers1.csv', index=False)
    except:
        questions_df = pd.DataFrame(question_rows)
        answers_df = pd.DataFrame(answer_rows)
        questions_df.to_csv('questions1.csv', index=False)
        answers_df.to_csv('answers1.csv', index=False)

if __name__ == "__main__":
    getQuestions()
