def remove_reasoning_from_output(output):
    return output.split("</think>")[-1].strip()

def clean_json_tags(text):
    return text.replace("```json\n", "").replace("\n```", "")

def clean_markdown_tags(text):
    return text.replace("```markdown\n", "").replace("\n```", "")