import json

from fastapi import APIRouter, Depends
from openai import OpenAI

from app.api.api_v1.endpoints.llm.tags import get_tags
from app.config import settings
from app.dependencies import api_key_auth
from app.schemas.llm.tags import SimpleQuery
from app.services import memos

router = APIRouter()


def edit_it(content: str):
    client = OpenAI(base_url=settings.GROQ_API_BASE, api_key=settings.GROQ_API_KEY)
    comp = client.chat.completions.create(
        model="llama3-8b-8192",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """You are a text editor who edit content in JSON.
                    The source content may from twitter, speech to text output, OCR result...
                    You should output with this JSON schema:
                    {
                        "content_after_editing": ""
                    }

                    for example, if you got `you is a bot` then you should output like:
                    {
                        "content_after_editing": "You are a bot."
                    }

                    If user input has no grammar or format issue, output as is.
                    for example, if you got "这句话没有问题。", then you should output like:
                    {
                        "content_after_editing": "这句话没有问题。"
                    }

                    KEEP Same language as user use.
                    """,  # noqa
            },
            {
                "role": "user",
                "content": "check and edit content: <CONTENT>he run fast.</CONTENT> to fix format, grammar and expression issues only",  # noqa
            },
            {
                "role": "assistant",
                "content": '{"content_after_editing": "He runs fast."}',
            },
            {
                "role": "user",
                "content": f"check and edit content: <CONTENT>{content}</CONTENT> to fix format, grammar and expression issues only",  # noqa
            },
        ],
    )
    return comp.choices[0].message.content


@router.post("/llm/editit", dependencies=[Depends(api_key_auth)])
async def llm_editit(query: SimpleQuery):
    return edit_it(query.content)


@router.post("/llm/memo_with_fix", dependencies=[Depends(api_key_auth)])
async def fix_memo(query: SimpleQuery):
    content = query.content
    tags = get_tags(content)
    fix_content = json.loads(edit_it(content)).get("content_after_editing")
    final_content = f"{fix_content}\n\n{tags} #from_apizone"
    r = memos.save_to_memos(final_content)
    return r.json()
