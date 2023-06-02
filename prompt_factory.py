from prompt import Prompt
from free_prompt import FreePrompt
from ga4_prompt import GA4Prompt


class PromptFactory:

    @staticmethod
    def get(schema_type: str, table_key: str, schema_json: str, instruction: str) -> Prompt:
        if schema_type == 'ga4':
            return GA4Prompt(table_key, schema_json, instruction)
        else:
            return FreePrompt(table_key, schema_json, instruction)
