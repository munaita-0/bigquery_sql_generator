from google.cloud import bigquery
import streamlit as st
import io


class BQ:
    def __init__(self, project, dataset, table):
        self.client = bigquery.Client()
        self.dataset = self.client.dataset(dataset, project=project)
        table_ref = self.dataset.table(table)
        self.table = self.client.get_table(table_ref)

    def schema_json(self, schema_type: str) -> str:
        if schema_type == 'ga4':
            return ''
        else:
            f = io.StringIO("")
            self.client.schema_to_json(self.table.schema, f)
            schema_json = f.getvalue().replace(' ', '').replace('\n', '')
            st.code('target_schema: ' + schema_json, language='shellSession')
            return schema_json

    def dry_run(self, query: str) -> str:
        job_config = bigquery.QueryJobConfig(dry_run=True)
        query_job = self.client.query(query, job_config=job_config)
        return f'SQL is Valid. Scaning {query_job.total_bytes_processed // 1000000000} GB'
