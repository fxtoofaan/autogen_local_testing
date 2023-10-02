#Header Block
import autogen
from autogen import AssistantAgent, UserProxyAgent, oai, GroupChat, GroupChatManager

config_list = [
    {
        "model": "/mnt/model/",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "NULL"
    }
]

response = oai.Completion.create(
    config_list=config_list,
    prompt="hi",
)
print(response)

response = oai.ChatCompletion.create(
    config_list=config_list,
    messages=[{"role": "user", "content": "hi"}]
)
print(response)

# Construct agents
assistant = autogen.AssistantAgent(
    name ="assistant",
    llm_config={"config_list": config_list},
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config={"config_list": config_list},
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

groupchat = autogen.GroupChat(agents=[user_proxy, assistant], messages=[], max_round=3)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

# Start a conversation
user_proxy.initiate_chat(
    manager,
    message="""
Tell me about this project, and the libary, then also tell me what I can use it for: https://python.langchain.com/docs/get_started/introduction
""",
)
