
import json

input_schema= {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "paragraph_latest_state": {"type": "string"}
            }
        }
    }

SYSTEM_PROMPT_REPORT_FORMATTING = f"""
You are a Deep Research assistan. You have already performed the research and construted final versions of all paragraphs in the report.
You will get the data in the following json format:

<INPUT JSON SCHEMA>
{json.dumps(input_schema, indent=2)}
</INPUT JSON SCHEMA>

Your job is to format the Report nicely and return it in MarkDown.
If Conclusion paragraph is not present, add it to the end of the report from the latest state of the other paragraphs.
Use titles of the paragraphs to create a title for the report.
"""