import streamlit as st
import os
from bq import BQ
from app import App
from prompt_factory import PromptFactory


# DEFAULT_API_KEY
# DEFAULT_TABLE_KEY
# DEFAULT_INSTRUCTION
# PASSWORD

def main():
    st.sidebar.text_input(
        'OPENAI API KEY',
        key='api_key'
    )

    st.sidebar.text_input(
        'Service Account Json Path',
        key='sa_path',
        placeholder='/Users/yourname/Desktop/hoge.json'
    )

    st.sidebar.selectbox(
        'データタイプ',
        ('ga4', 'その他'),
        key='schema_type'
    )

    st.sidebar.text_input(
        'BigQuery table_key',
        key='table_key',
        placeholder='project_id.dataset_name.table_name'
    )

    st.sidebar.text_area(
        '指示',
        key='instruction',
        placeholder='直近1週間の流入元毎のイベント数を表示するSQLを出力してください.'
    )

    st.sidebar.checkbox(
        '実際にクエリを実行して結果を表示する',
        key="run_query"
    )

    st.sidebar.button('実行')

    api_key = st.session_state.api_key
    if api_key == "":
        api_key = os.environ.get('DEFAULT_API_KEY', '')
    if api_key == '':
        'api_keyを入力してください'
        return

    sa_path = st.session_state.sa_path
    if sa_path == '':
        sa_path = os.environ.get('DEFAULT_SA_PATH', '')
    if sa_path != '':
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = sa_path

    schema_type = st.session_state.schema_type

    table_key = st.session_state.table_key
    if table_key == '':
        table_key = os.environ.get('DEFAULT_TABLE_KEY', '')

    if table_key == '':
        'table_keyを入力してください'
        return

    instruction = st.session_state.instruction
    if instruction == '':
        instruction = os.environ.get('DEFAULT_INSTRUCTION', '')

    if instruction == '':
        'instructionを入力してください'
        return

    dry_run = not st.session_state.run_query

    project = table_key.split('.')[0]
    dataset = table_key.split('.')[1]
    table = table_key.split('.')[2]

    log = f"""
    run with input...
    schema_type: {schema_type}
    table_key: {table_key},
    instruction: {instruction}
    """
    st.code(log, language='shellSession')

    bq = BQ(project, dataset, table)
    schema_json = bq.schema_json(schema_type)

    prompt = PromptFactory.get(schema_type, table_key, schema_json, instruction)
    messages = prompt.get_messages()
    df = App(bq, api_key, prompt).request_query_repeatedly(messages, 1, dry_run)
    df


if __name__ == '__main__':
    main()
