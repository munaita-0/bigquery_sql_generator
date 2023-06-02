class Prompt:

    def __init__(self, table_key: str, schema_json: str, instruction: str):
        self.table_key = table_key
        self.schema_json = schema_json
        self.instruction = instruction

    system_prompt = """
    あなたは広告分析のプロです。
    命令に従いBigQueryのSQLを出力してください。
    SQLはWithを使って可読性の高いものにしてください。
    期間指定がない場合は直近一週間を期間指定してください。
    BigQueryで実行可能なSQLのみを出力してください。
    """

    # common_user_prompt_zero = "分析対象のtable_id は bigquery-public-data.country_codes.country_codesです。レコード数をカウントするSQLをください"
    # asistant_prompt_zero = """
    # {
    #   "message": "レコード数をカウントするシンプルなSQLです。そのままBigQueryで実行できます",
    #   "query": "SELECT COUNT(*) FROM `bigquery-public-data.country_codes.country_codes`"
    # }
    # """

    user_prompt_format = """
    必ずJSON形式で出力してください。
    キーは query と message です。
    queryキーの値にSQLを出力してください。
    messageキーの値にメッセージを出力してください。
    SQLはbigqueryで実行できる形で出力してください。
    """

    # def __init__(self):

    def get_user_prompt_main(self) -> str:
        return f"""
        分析対象のtable_id は {self.table_key}です。
        テーブルスキーマは次のJSONの通りです。

        ###
        {self.schema_json}
        ###

        命令は以下です

        ###
        {self.instruction}
        ###
        """

    def get_user_prompt_fix(self, query: str, error_msgs: str) -> str:
        return f"""
        SQL作成時に以下のエラーを考慮してしてください。

        ###

        {query}

        このSQLを以前BigQueryで実行した際、以下のようなエラーメッセージが発生しています。

        {error_msgs}
        ###
        """
