
from typing import Dict
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from v1.src.prompts import OPEN_AI_SYSTEM_PROMPT, OPEN_AI_USER_PROMPT

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from core.settings import settings


def create_chain(
    model: str = settings.openai.MODEL,
    api_key :str  = settings.openai.OPENAI_API_KEY,
    model_kwargs: Dict = settings.openai_kwargs.model_dump(),
    system_message_prompt: str = OPEN_AI_SYSTEM_PROMPT,
    human_message_prompt: str = OPEN_AI_USER_PROMPT,
    ) -> LLMChain:
    lc_system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_prompt)
    lc_human_message_prompt = HumanMessagePromptTemplate.from_template(human_message_prompt)
    
    chat_prompt = ChatPromptTemplate.from_messages(
        [lc_system_message_prompt, lc_human_message_prompt]
    )
    print("Chat Prompt: ", chat_prompt)
    model = ChatOpenAI(model=model, openai_api_key=api_key, **model_kwargs)
    llm_chain = LLMChain(
        llm=model,
        prompt=chat_prompt,
    )
    return llm_chain