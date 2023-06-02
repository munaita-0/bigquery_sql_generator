from typing import List, Dict
from prompt import Prompt


class GA4Prompt(Prompt):

    def __init__(self, table_key: str, schema_json: str, instruction: str):
        super().__init__(table_key, schema_json, instruction)
        self.table_key = table_key
        self.schema_json = schema_json
        self.instruction = instruction

    user_prompt_first = """
    分析対象のテーブルはGoogle Analitics 4 のBigQueryにExportしたテーブルになります。
    分析対象のtable_id は `analytics_dataset.events_*`  です。

    命令は以下です。

    ###
    直近一週間の日別ページビューを出してください
    ###

    フォーマットは以下です。

    ###
    必ずJSON形式で出力してください。
    キーは query と message です。
    queryキーの値にSQLを出力してください。
    messageキーの値にメッセージを出力してください。
    SQLはbigqueryで実行できる形で出力してください。
    ###
    """

    asistant_prompt_first = """
    {
        "message": "直近1週間の日別のページビューを出しています",
        "query": "SELECT DATE(timestamp_micros(event_timestamp), 'Asia/Tokyo') AS hitdate, COUNT(1) AS pageviews FROM `analytics_dataset.events_*` WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)) AND event_name = 'page_view' GROUP BY 1 ORDER BY 1"
    }
    """

    user_prompt_second = """
    分析対象のテーブルはGoogle Analitics 4 のBigQueryにExportしたテーブルになります。
    分析対象のtable_id は `analytics_dataset.events_*`  です。

    命令は以下です。

    ###
    セッション数を出してください
    ###

    フォーマットは以下です。

    ###
    必ずJSON形式で出力してください。
    キーは query と message です。
    queryキーの値にSQLを出力してください。
    messageキーの値にメッセージを出力してください。
    SQLはbigqueryで実行できる形で出力してください。
    ###
    """

    asistant_prompt_second = """
    {
        "message": "直近1週間の日別のページビューを出しています",
        "query": "WITH t1 AS ( SELECT DATE(TIMESTAMP_MICROS(event_timestamp), 'Asia/Tokyo') AS hitdate, CONCAT(user_pseudo_id, CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') as STRING)) AS sid FROM `analytics_dataset.events_*` WHERE _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)) AND event_name = 'session_start' ) SELECT hitdate, COUNT(DISTINCT sid) AS session FROM t1 GROUP BY 1 ORDER BY 1"
    }
    """

    # def __init__(self):

    def get_messages(self) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt_first},
            {"role": "assistant", "content": self.asistant_prompt_first},
            {"role": "user", "content": self.user_prompt_second},
            {"role": "assistant", "content": self.asistant_prompt_second},
            {"role": "user", "content": self.get_user_prompt_main()},
            {"role": "user", "content": self.user_prompt_format},
        ]

    def get_user_prompt_set_schema(self) -> str:
        return f"""
        分析対象のテーブルスキーマは次のJSONの通りです。

        ###
        {self.schema_json}
        ###
        """

    def get_user_prompt_main(self) -> str:
        return f"""
        分析対象のtable_id は {self.table_key}です。

        命令は以下です

        ###
        {self.instruction}
        ###
        """
