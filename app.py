import openai
import json
import streamlit as st
from google.api_core.exceptions import BadRequest
from typing import List, Dict
import pandas as pd


class App():
    def __init__(self, bq, api_key, prompt):
        self.bq = bq
        self.api_key = api_key
        self.prompt = prompt

    def request_query_repeatedly(self, messages: List[Dict[str, str]], repeat_count: int, dry_run: bool = True) -> pd.DataFrame:
        if repeat_count >= 6:
            "5回実行しました。最大試行回数を超えたため終了します"
            return

        st.code(messages, language='shellSession')
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            # model="gpt-3.5-turbo",
            messages=messages
        )
        # st.code(response, language='shellSession')

        log = json.dumps(response['usage']).replace(' ', '').replace('\n', '')
        st.code('token usage: ' + log, language='shellSession')

        content = response['choices'][0]['message']['content']
        # st.code(content, language='shellSession')
        content_dict = json.loads(content)
        query = content_dict['query']
        st.code('message: ' + content_dict['message'], language='shellSession')
        st.code(content_dict['query'], language='sql')

        try:
            if dry_run:
                return self.bq.dry_run(query)
            else:
                return self.bq.client.query(query).to_dataframe()
        except BadRequest as e:
            st.code('== エラーが発生したので再試行します ==', language='shellSession')

            error_msgs = []
            for err in e.errors:
                error_msgs.append(err['message'])

            fix_user_prompt = {
                'role': 'user',
                'content': self.prompt.get_user_prompt_fix(query, '. '.join(error_msgs))
            }

            messages.insert(len(messages) - 1, fix_user_prompt)
            return self.request_query_repeatedly(messages, repeat_count + 1, dry_run)
