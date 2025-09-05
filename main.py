from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from elevenlabs.types import ConversationConfig
import os
from dotenv import load_dotenv


load_dotenv()
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")

user_name = "Hana"
schedule = "Wake up Early For Jogging at 5:00 am"
prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {"prompt": prompt},
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
    user_id="alex_user_1",  # required
)


client = ElevenLabs(api_key=API_KEY)


def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript):
    print(f"User (voice): {transcript}")


conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),  
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)


try:
    
    conversation.start_session()

    print("\n✅ Voice assistant is running.")
    print("👉 Speak into your mic OR type a message below.")
    print("👉 Type 'quit' or 'exit' to stop.\n")

    while True:
        user_input = input("You (typed): ")
        if user_input.lower() in ["quit", "exit"]:
            conversation.end_session() 
            break

       
        conversation.send_user_message(user_input)

except Exception as e:
    print("Error:", e)