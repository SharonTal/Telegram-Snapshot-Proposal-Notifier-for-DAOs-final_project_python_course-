import requests
from datetime import datetime
import os

# File handling functions
def read_sent_proposal_ids(file_name="sent_proposal_ids.txt"):
    """Reads sent proposal IDs from the file."""
    try:
        with open(file_name, 'r') as file:
            return set(file.read().splitlines())  
    except FileNotFoundError:
        return set()

def write_sent_proposal_id(file_name, proposal_id):
    """Writes a new proposal ID to the file."""
    try:
        with open(file_name, 'a') as file:
            file.write(proposal_id + '\n')
        print(f"✅ Proposal ID {proposal_id} saved to {file_name}")
    except Exception as e:
        print("❌ Error writing proposal ID:", e)

# Telegram messaging
def send_telegram_message(bot_token, chat_ids, message):
    """Sends a message via Telegram bot."""
    base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    for chat_id in chat_ids:
        params = {'chat_id': chat_id, 'parse_mode': 'Markdown', 'text': message}
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                print(f"✅ Message sent to chat {chat_id}")
            else:
                print("❌ Telegram API Error:", response.status_code, response.text)
        except Exception as e:
            print("❌ Error sending Telegram message:", e)

# Fetch proposals
def fetch_proposals(space_ids):
    """Fetches proposals from the Snapshot API."""
    url = 'https://hub.snapshot.org/graphql'
    all_proposals = []
    for space_id in space_ids:
        query = '''
        {
          proposals(first: 100, where: {space_in: ["%s"]}) {
            id
            title
            body
            start
            end
          }
        }
        ''' % space_id
        try:
            response = requests.post(url, json={'query': query})
            if response.status_code == 200:
                proposals = response.json().get('data', {}).get('proposals', [])
                if proposals:
                    for proposal in proposals:
                        proposal['space_id'] = space_id
                    all_proposals.extend(proposals)
                    print(f"✅ Fetched {len(proposals)} proposals from {space_id}")
            else:
                print(f"❌ Error fetching proposals for {space_id}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching proposals for {space_id}:", e)
    return all_proposals

# Check and send new proposals
def send_new_proposals(proposals, bot_token, chat_ids, sent_ids_file):
    """Sends new proposals that haven't been sent before."""
    sent_ids = read_sent_proposal_ids(sent_ids_file)

    for proposal in proposals:
        proposal_id = proposal['id']
        if proposal_id in sent_ids:
            continue

        message = f"📢 New Proposal Alert!\n\n" \
                  f"🌍 *Space:* {proposal['space_id']}\n" \
                  f"📌 *Title:* {proposal['title']}\n"

        send_telegram_message(bot_token, chat_ids, message)
        write_sent_proposal_id(sent_ids_file, proposal_id)

# Configuration
space_ids = [
    "beanstalkdao.eth",
    "balancer.eth",
    "gmx.eth",
    "cakevote.eth",
    "aave.eth",
    "uniswap.eth",
    "compound.eth",
    "sushigov.eth",
    "yearn.eth",
    "synthetix.eth",
]

bot_token = '6959566469:AAGAwM8v8nFn-KuID99ek0cVYFeMEboOUDc'
chat_ids = ['###insert your token here']
file_name = "sent_proposal_ids.txt"

proposals = fetch_proposals(space_ids)
send_new_proposals(proposals, bot_token, chat_ids, file_name)
