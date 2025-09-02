def remove_reasoning(output):
    return output.split("</think>")[-1].strip()

def clean_json(text):
    return text.replace("```json\n", "").replace("\n```", "")

def clean_markdown(text):
    return text.replace("```markdown\n", "").replace("\n```", "")