from fastapi import APIRouter, Depends
from openai import OpenAI

from app.config import settings
from app.dependencies import api_key_auth
from app.schemas.llm.tags import SimpleQuery
from app.services import memos

router = APIRouter()


def get_tags(content: str):
    client = OpenAI(base_url=settings.GROQ_API_BASE, api_key=settings.GROQ_API_KEY)
    comp = client.chat.completions.create(
        model="llama3-8b-8192",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You always generate a tag list join with a single space like: `#a #b #c #e_f`"  # noqa
                    "DO NOT ADD ANY OTHER THINGS EXCEPT THE HASHTAG STRING."
                    "5~10 proper Tags is enough."
                ),
            },
            {
                "role": "user",
                "content": f"generate a list of #hashtag for content: <CONTENT>{content}</CONTENT>",  # noqa
            },
        ],
    )
    return comp.choices[0].message.content


@router.post("/llm/tagit", dependencies=[Depends(api_key_auth)])
async def llm_tagit(query: SimpleQuery):
    return get_tags(query.content)


@router.post("/llm/memo_with_tag", dependencies=[Depends(api_key_auth)])
async def tags_memo(query: SimpleQuery):
    content = query.content
    tags = get_tags(content)
    final_content = f"{content}\n\n{tags} #from_apizone"
    r = memos.save_to_memos(final_content)
    return r.json()
