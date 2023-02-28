import requests
import json
from notion_client import Client


def get_block_data(token, block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def find_text(data, start_idx, end_idx):
    text = []
    for i in range(start_idx, end_idx):
        block = data["results"][i]
        if block["type"] == "paragraph":
            text.append(block["paragraph"]["rich_text"][0]["plain_text"])
    return text


def format_text(text):
    return " ".join(text).replace("—", "").replace("  ", " ")


def write_text(client, page_id, header, text):
    client.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": header}}]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            },
        ],
    )


def update_notion(api_key, my_score, deepl_score):
    notion_page_id = "b965a7473ab845a9a9b826e98a52ca3c"
    client = Client(auth=api_key)
    header = "Translation Scores"
    text = f"My translation score: {my_score:.2f}\nDeepL translation score: {deepl_score:.2f}"
    write_text(client, notion_page_id, header, text)
