from typing import List, Dict
from prompt import Prompt


class FreePrompt(Prompt):

    def __init__(self, table_key: str, schema_json: str, instruction: str):
        super().__init__(table_key, schema_json, instruction)
        self.table_key = table_key
        self.schema_json = schema_json
        self.instruction = instruction

    user_prompt_first = """
    分析対象のtable_id は bigquery-public-data.country_codes.country_codesです。
    テーブルスキーマは次のJSONの通りです。

    ###
    [ { "mode": "NULLABLE", "name": "country_name", "type": "STRING" }, { "mode": "NULLABLE", "name": "alpha_2_code", "type": "STRING" }, { "mode": "NULLABLE", "name": "alpha_3_code", "type": "STRING" } ]
    ###

    命令は以下です。

    ###
    kとeから始まる国名のレコードを抽出したいです
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
      "message": "WITH句で可読性の高いSQLを出力しています",
      "query": "WITH filter_countries AS ( SELECT * FROM `bigquery-public-data.country_codes.country_codes` WHERE LOWER(country_name) LIKE 'k%' OR LOWER(country_name) LIKE 'e%' ) SELECT * FROM filter_countries"
    }
    """

    def get_messages(self) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_prompt_first},
            {"role": "assistant", "content": self.asistant_prompt_first},
            {"role": "user", "content": self.get_user_prompt_main()},
            {"role": "user", "content": self.user_prompt_format},
        ]
