
# Importing libraries
from typing import Any, Dict, List, Optional, Tuple, Union, Callable, Literal, ClassVar
import random
from abc import ABC, abstractmethod
import json
from v1.models.intent_classifier import predict
from v1.src.logger import logger
import requests
from core.models.kb_models import DocumentQuery,DocumentQueyResponse, ModelKwargs, GenerateQuery, GenerateResponse
from core.settings import settings
import markdown
import re
class BaseHandler(ABC):
    feedback: Optional[bool] = False
    def __init__(self,elements:List[Dict|None]|None = None)-> None:
        self.elements = elements


    @abstractmethod
    def execute(self, value: Any, keys: Optional[List[str]] = ["last_utterance"], vars: Optional[Dict[str, Any]] = {}):
        pass
    
    @abstractmethod
    def __call__(self):
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(**data)

    def to_dict(self):
        return self.__dict__
    
    def __call__(
        self,
        value: Any, 
        vars: Optional[Dict[str, Any]] = None,
        ):
        result = self.execute(value,vars)
        return result  
    
    

class TextHandler(BaseHandler):
    type: Literal["text"] = "text"
    show: Optional[bool] = True
    def __init__(
        self,
        text: Union[str, List[str]],
        saving_keys: Optional[List[str]] = ["last_response"]
        ) -> None:
        
        super().__init__()
        self.text: Union[str, List[str]] = text
        self.saving_keys = saving_keys
        
    def execute(
        self,
        value: Optional[Any] = None,  # Value is not used in this handler  but needs to be passed to mantain structure
        vars: Optional[Dict[str, Any]] = None,
        ) -> Tuple[Union[str, None], Union[str, None]]:
        
        text = self.text
        
        if isinstance(text, list):
            text = random.choice(text)
        
        if vars is not None:
            text = text.format(**vars)
        return text , None
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        text = data["text"]
        return cls(text=text)



class ListenHandler(BaseHandler):
    type: Literal["l"] = "l"
    show: Optional[bool] = True
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["last_utterance"],
        elements: Optional[List[Dict]] = None,
        timeout: Optional[str] = None,
        ) -> None:
        super().__init__(elements=elements)
        self.saving_keys = saving_keys
        self.timeout = timeout
    
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        # Does not execute anything, just saves the value
        # TODO: Add DB saving
        return value , None
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        saving_keys = json.loads(data["saving_keys"])
        elements = data["elements"]
        timeout = data["timeout"]
        if isinstance(elements, str):
            elements = json.loads(elements)
        if len(elements) == 0:
            elements = None
        return cls(saving_keys=saving_keys, elements=elements, timeout=timeout)


class EndHandler(BaseHandler):
    type: Literal["end"] = "end"
    show: Optional[bool] = True
    def __init__(
        self,
        text: Union[str, List[str]],
        saving_keys: Optional[List[str]] = ["last_response"]
        ) -> None:
        
        super().__init__()
        self.text: Union[str, List[str]] = text
        self.saving_keys = saving_keys
        
    def execute(
        self,
        value: Optional[Any] = None,  # Value is not used in this handler  but needs to be passed to mantain structure
        vars: Optional[Dict[str, Any]] = None,
        )  -> Tuple[Union[str, None], Union[str, None]]:
        
        text = self.text
        
        if isinstance(text, list):
            text = random.choice(text)
        
        if vars is not None:
            text = text.format(**vars)
        return text , None
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        text = data["text"]
        return cls(text=text)

class DeciderHandler(BaseHandler):
    type: Literal["decider"] = "decider"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["current_intent"],
        labels: Optional[List[str]] = ["help","greeting","goodbye"],
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.labels = labels

    
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        sentence = vars["last_utterance"]
        logger.info(f"Decider handler: {sentence}")
        
        results = predict(text=sentence,labels=self.labels)
        logger.info(f"Decider handler results: {results}")
        scores = results["scores"]
        labels = results["labels"]
        max_score = max(scores)
        # TODO set max score in env var
        num_labels = len(labels)

        score_treshold = 1/num_labels + (1/num_labels)/2 + (1/num_labels)/4
        if max_score > score_treshold:
            intent = labels[scores.index(max_score)]
        else:
            intent = "fail"
        return None , intent
        
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        labels = json.loads(data["intents"])
        return cls(labels=labels)
    
class IntentHandler(BaseHandler):
    type: Literal["intent"] = "intent"
    show: Optional[bool] = False
    
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["current_intent"],
        label: str = "fail",
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.label = label
    
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        
        intent = self.label
        
        
        return intent , None
        
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        label = data["intent"]
        return cls(label=label)
    
    
class QaHandler(BaseHandler):
    type: Literal["qa"] = "qa"
    show: Optional[bool] = True
    feedback: Optional[bool] = True
    def __init__(
        self,
        collection: str = "tenantev",
        question_text: str = "{last_utterance}",
        temperature: float = 0.5,
        max_tokens: int = 2000,
        model: str = "gpt-3.5-turbo",
        saving_keys: Optional[List[str]] = ["last_response"],
        generate = True,
        num_results: int = 5,
        if_fail: str = "Sorry, I don't know the answer to that question"
        ) -> None:
        super().__init__()
        self.collection = collection
        self.question_text = question_text
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        self.saving_keys = saving_keys
        self.generate = generate
        self.num_results = num_results
        self.if_fail = if_fail
        
    def predict(self,value,vars):
        question = self.question_text.format(**vars)
        collection = self.collection
        temperature = self.temperature
        max_tokens = self.max_tokens
        model = self.model
        generate = self.generate
        num_results = self.num_results
        fail_response = self.if_fail
        try:
            document_query = DocumentQuery(
                model=model,
                llm_model_kwargs=ModelKwargs(temperature=temperature, max_tokens=max_tokens),
                question=question,
                generate=generate,
                num_results=num_results,
                )
            payload = document_query.model_dump()
            headers={"Authorization": f"Bearer {settings.kb.CHATBOT_KB_TOKEN}"}
            url_base = settings.kb.CHATBOT_KB_URL
            response = requests.post(
                f"{url_base}/kb/{collection}/query",
                json=payload,
                headers=headers
                )
            response.raise_for_status()
            response = response.json()
            response_parsed = DocumentQueyResponse(**response)
            
            if len(response_parsed.documents) > 0:
                answer = response_parsed.answer
            else:
                answer = fail_response
            return answer
        except Exception as e:
            logger.error(e)
            print(e)
            return None
        
        
        
        
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None,
        ) -> Tuple[Union[str, None], Union[str, None]]:
        
        text = self.predict(value,vars)
        if text is None:
            intent = "fail"
        else:
            intent = "success"
        
        return text , intent
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        collection = data["collection"]
        question_text = data["question"]
        temperature = data["temperature"]
        max_tokens = data["max_tokens"]
        model = data["model"]
        num_results = data["num_docs"]
        if_fail = data["fallback"]
        return cls(
            collection=collection,
            question_text=question_text,
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            num_results=num_results,
            if_fail=if_fail
            )
        
        

class AIHandler(BaseHandler):
    type: Literal["qa"] = "ai"
    def __init__(
        self,
        instruction: str,
        system_message: str,
        saving_keys: Optional[List[str]] = ["last_response"],
        show: Optional[bool] = True,
        temperature: float = 0.5,
        max_tokens: int = 2000,
        model: str = "gpt-3.5-turbo",
        ) -> None:
        super().__init__()
        self.instruction = instruction
        self.system_message = system_message
        self.saving_keys = saving_keys
        self.show = show
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model
        
    def predict(self,value,vars):
        instruction = self.instruction.format(**vars)
        system_message = self.system_message.format(**vars)
        temperature = self.temperature
        max_tokens = self.max_tokens
        model = self.model
        try:
            generate_query = GenerateQuery(
                model=model,
                llm_model_kwargs=ModelKwargs(temperature=temperature, max_tokens=max_tokens),
                system_prompt=instruction,
                human_prompt=system_message
                )
            payload = generate_query.model_dump()
            headers={"Authorization": f"Bearer {settings.kb.CHATBOT_KB_TOKEN}"}
            url_base = settings.kb.CHATBOT_KB_URL
            response = requests.post(
                f"{url_base}/generate",
                json=payload,
                headers=headers
                )
            response.raise_for_status()
            response = response.json()
            response_parsed = GenerateResponse(**response)
            return response_parsed.answer
        except Exception as e:
            logger.error(e)
            print(e)
            return None
        
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None,
        ) -> Tuple[Union[str, None], Union[str, None]]:
        
        text = self.predict(value,vars)
        if text is None:
            intent = "fail"
        else:
            intent = "success"
            
        return text , intent
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        instruction = data["instruction"]
        
        system_message = data["system_message"]
        temperature = data["temperature"]
        max_tokens = data["max_tokens"]
        model = data["model"]
        show = data["show"]
        saving_keys = data["saving_keys"]
        if show == "yes":
            show = True
        elif show == "no":
            show = False
        else:
            raise ValueError("Show must be yes or no")
        return cls(
            instruction=instruction,
            system_message=system_message,
            temperature=temperature,
            max_tokens=max_tokens,
            saving_keys=saving_keys,
            model=model,
            show=show
            )
        
class ValidatorHandler(BaseHandler):
    type: Literal["validator"] = "validator"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["current_intent"],
        val_type: Literal["email","id"] = "email",
        var: str = "last_utterance",
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.val_type = val_type
        self.var = var
        
    def validate_email(self,email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            return False
        
    def validate_id(self,id):
        if re.match(r"^[0-9]{4,6}$", id):
            return True
        else:
            return False
    
    def execute(
        self,
        value: Optional[Any] = None,
        vars: Optional[Dict[str, Any]] = None, 
        ) -> Tuple[Union[str, None], Union[str, None]]:
        var_value = vars[self.var]
        
        if self.val_type == "email":
            if self.validate_email(var_value):
                intent = "valid"
            else:
                intent = "fail"
        elif self.val_type == "id":
            if self.validate_id(var_value):
                intent = "valid"
            else:
                intent = "fail"
        return None , intent
        
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        val_type = data["type"]
        var = data["variable"]
        return cls(val_type=val_type,var=var)
    
    
class SetValueHandler(BaseHandler):

    type: Literal["set"] = "set"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["last_utterance"],
        set_value: str = "last_utterance",
        data_type: str = "text",
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.set_value = set_value
        self.data_type = data_type
    
    def execute(
        self,
        value: Optional[Any] = None, # There is no value as it is set by the user in the UI, value only for listening
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        # Does not execute anything, just saves the value
        set_value = self.set_value
        set_value = set_value.format(**vars)
        data_type = self.data_type
        if data_type == "text":
            set_value = set_value
        elif data_type == "number":
            set_value = float(set_value)
        elif data_type == "boolean":
            set_value = set_value.lower()
            set_value = True if set_value == "true" else False
        
        return set_value , None
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        saving_keys = json.loads(data["saving_keys"])
        set_value = data["value"]
        data_type = data["type"]

        
        return cls(saving_keys=saving_keys, set_value=set_value, data_type=data_type)


    
class CounterHandler(BaseHandler):

    type: Literal["set"] = "counter"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["last_utterance"],
        add: float = 1,
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.add = add
    
    def execute(
        self,
        value: Optional[Any] = None, # There is no value as it is set by the user in the UI, value only for listening
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        # Does not execute anything, just saves the value
        plus_val = self.add
        var_name = self.saving_keys[0]
        value = vars[var_name] + plus_val
        
        
        return value , None
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        saving_keys = json.loads(data["saving_keys"])
        add = data["add"]
        add = float(add)
        
        return cls(saving_keys=saving_keys, add=add)

   
class IfHandler(BaseHandler):

    type: Literal["set"] = "if"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["current_intent"],
        variable: str = "last_utterance",
        var_value: str = "yes",
        condition: str = "equals",
        var_type: str = "text",
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.variable = variable
        self.var_value = var_value
        self.condition = condition
        self.var_type = var_type
    
    
    def equals(self, value, var_value):
        if value == var_value:
            return True
        else:
            return False
    
    def contains(self, value, var_value):
        if isinstance(var_value, str):
            if var_value in value:
                return True
            else:
                return False
        else:
            raise ValueError("var_value must be a string")
    
    def not_equals(self, value, var_value):
        if value != var_value:
            return True
        else:
            return False
    
    def not_contains(self, value, var_value):
        if isinstance(var_value, str):
            if var_value not in value:
                return True
            else:
                return False
        else:
            raise ValueError("var_value must be a string")
        
    def greater_than(self, value, var_value):
        if isinstance(var_value, str):
            raise ValueError("var_value must be a number")
        else:
            if value > var_value:
                return True
            else:
                return False
    def less_than(self, value, var_value):
        if isinstance(var_value, str):
            raise ValueError("var_value must be a number")
        else:
            if value < var_value:
                return True
            else:
                return False
        
    def compare(self, value, var_value, condition):
        
        funcs = {
            "equals": self.equals,
            "contains": self.contains,
            "not_equals": self.not_equals,
            "not_contains": self.not_contains,
            "greater_than": self.greater_than,
            "less_than": self.less_than,
            }
        
        if condition not in funcs.keys():
            raise ValueError("Condition must be equals, contains, not_equals, not_contains, greater_than or less_than")
        else:
            condition = funcs[condition](value, var_value)
            if condition:
                return "yes"
            else:
                return "no"
        
    def execute(
        self,
        value: Optional[Any] = None, # There is no value as it is set by the user in the UI, value only for listening
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        # Does not execute anything, just saves the value
        
        variable = self.variable
        condition = self.condition
        var_type = self.var_type
        var_value = self.var_value
        if var_type == "text":
            var_value = var_value
        elif var_type == "number":
            var_value = float(var_value)
        elif var_type == "boolean":
            var_value = var_value.lower()
            var_value = True if var_value == "true" else False
        else:
            raise ValueError("var_type must be text, number or boolean")
        
        true_value = vars[variable]
        
        condition = self.compare(true_value, var_value, condition)
        
        return None, condition
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        
        variable = json.loads(data["variable"])[0]
        condition = data["condition"]
        var_type = data["type"]
        var_value = data["value"]
        return cls(
            variable=variable, 
            condition=condition,
            var_type=var_type, 
            var_value=var_value
            )

  
    
class TicketHandler(BaseHandler):

    type: Literal["set"] = "ticket"
    show: Optional[bool] = False
    def __init__(
        self,
        saving_keys: Optional[List[str]] = ["ticket_response"],
        ticket_platform: str = "Support",
        ) -> None:
        super().__init__()
        self.saving_keys = saving_keys
        self.ticket_platform = ticket_platform
        
    def parse_session_chats(self, data):
        chat_history = data['history']
        filtered_messages = []
        for message in chat_history:
            if message['user'] in ['USER', 'AI']:
                filtered_messages.append(message)

        html = """<p>
        <b>Ticket Report</b>
        <br><br>
        <b>User Data</b>
        <br></p>
        """
        html += f"""<p>
        <b>Name:</b> {data["name"]}<br>
        <b>Email:</b> {data["email"]}<br>
        <b>Role:</b> {data["role"]}<br>
        <br>
        <b>Chat History</b>
        <br><br>
        </p>
        """

        for message in filtered_messages:
            text = message['text']
            
            text = re.sub('\\n\\n', '', text)
            html_text = markdown.markdown(text)
            html_text = re.sub('<p>', '', html_text)
            html_text = re.sub('</p>', '', html_text)
            html += "<p><b>%s</b>: %s<br><br></p>" % (message['user'], html_text)

        html = re.sub("\n", "", html)
        
        return html
    
    def save_ticket(self, data, ticket_id):
        from core.models.chatlog_models import TicketCreate
        
        ticket = TicketCreate(
            session_id=data["session_id"],
            data=data["email"],
            ticket_id=ticket_id
        )
        ticket_url = f"{settings.chatlog.CHATBOT_CHATLOG_URL}/tickets"
        ticket_token = settings.chatlog.CHATBOT_CHATLOG_TOKEN
        headers = {"Authorization": f"Bearer {ticket_token}"}
        req_data = ticket.model_dump()
        try:
            r = requests.post(
                url=ticket_url, 
                json=req_data,
                headers=headers
                )
            r.raise_for_status()
        except Exception as e:
            logger.error(e)
        
        
    
    def create_ticket(self, data,platform):
         # Freshdesk API
        html = self.parse_session_chats(data)
        # Freshdesk ENV variable for ticket creation 
        api_key = settings.freshdesk.FRESHDESK_API_KEY
        domain = settings.freshdesk.FRESHDESK_API_DOMAIN
        password = settings.freshdesk.FRESHDESK_API_PASSWORD

        name = data["name"]
        headers = { "Content-Type" : "application/json" }
        email = data["email"]
        chat_history = html
        ticket = {
        "subject": f"Chatbot Ticket from {email}",
        "description": f"{chat_history}",
        "email": f"{email}",
        "name": f"{name}",
        "priority": 1,
        "status": 2,
        "source": 7,
        "custom_fields": {
            "cf_type_of_query_2": f"{platform}",
            "cf_sub_category": "Other"
        }
        }
        try:
        # Requesting Data to URL
            r = requests.post("https://"+ domain +".freshdesk.com/api/v2/tickets", auth = (api_key,password), headers = headers, json=ticket)
            # Checking HTTP Status
            r.raise_for_status()
            # Returning the JSON Response if Status is OK and ID is not 0
            if r.json()['id'] != 0:
                logger.info('Ticket Created Successfully, the ticket ID is {}'.format(r.json()['id']))
                return r.json()['id'] , "success"
        except Exception as e:
            logger.error(e)
            # raise system exit if the ticket is not created to avoid wrong api responses
            return None , "fail"

    def execute(
        self,
        value: Optional[Any] = None, # There is no value as it is set by the user in the UI, value only for listening
        vars: Optional[Dict[str, Any]] = None,  # Vars is not used in this handler
        ) -> Tuple[Union[str, None], Union[str, None]]:
        # Does not execute anything, just saves the value
        ticket_platform = self.ticket_platform
        
        ticket_id , intent = self.create_ticket(vars,ticket_platform)
        if ticket_id:
            self.save_ticket(vars,ticket_id)
        
        return ticket_id, intent
    
    @classmethod
    def from_data(cls, data: Dict[str, Any]):
        return cls(ticket_platform=data["freshdesk_environment"])

