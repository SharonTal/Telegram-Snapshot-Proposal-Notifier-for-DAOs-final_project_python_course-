import requests
from datetime import datetime

def read_sent_proposal_ids(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

def write_sent_proposal_id(file_path, proposal_id):
    with open(file_path, 'a') as file:
        file.write(proposal_id + '\n')

def send_telegram_message(bot_token, chat_ids, message):
    for chat_id in chat_ids:
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
        response = requests.get(send_text)
        if response.status_code != 200:
            print("Telegram API Error:", response.status_code, response.text)
        else:
            print(f"Message sent successfully to Telegram chat ID: {chat_id}")

def fetch_proposals(space_ids):
    print("Fetching proposals...")
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
        response = requests.post(url, json={'query': query})
        space_proposals = response.json().get('data', {}).get('proposals', [])
        if space_proposals:
            for proposal in space_proposals:
                proposal['space_id'] = space_id
            all_proposals.extend(space_proposals)
            print(f"Fetched {len(space_proposals)} proposals from {space_id}.")
        else:
            print(f"No proposals fetched from {space_id}.")
    return all_proposals

def send_active_proposals(proposals, bot_token, chat_ids, sent_ids_file):
    sent_ids = read_sent_proposal_ids(sent_ids_file)
    now = datetime.now()
    for proposal in proposals:
        try:
            if proposal['id'] not in sent_ids:
                if isinstance(proposal['start'], int):
                    start_time = datetime.fromtimestamp(proposal['start'])
                    end_time = datetime.fromtimestamp(proposal['end'])
                else:
                    start_time = datetime.fromisoformat(proposal['start'].rstrip('Z'))
                    end_time = datetime.fromisoformat(proposal['end'].rstrip('Z'))

                if start_time <= now <= end_time:
                    message = f"Space: {proposal['space_id']}\nTitle: {proposal['title']}\n"
                    send_telegram_message(bot_token, chat_ids, message)
                    write_sent_proposal_id(sent_ids_file, proposal['id'])
        except Exception as e:
            print(f"Error processing proposal ID {proposal['id']}: {e}")


space_ids = ['beanstalkdao.eth', 'balancer.eth', 'gmx.eth', 'cakevote.eth']
bot_token = '6959566469:AAGAwM8v8nFn-KuID99ek0cVYFeMEboOUDc'
chat_ids = ['1035984563']

sent_ids_file = "sent_proposal_ids.txt"

proposals = fetch_proposals(space_ids)
send_active_proposals(proposals, bot_token, chat_ids, sent_ids_file)

