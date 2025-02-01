# Telegram Snapshot Proposal Notifier

## Objective Summary
In the world of **DAOs** (Decentralized Autonomous Organizations), staying informed about active proposals is crucial for effective participation in decision-making. A **DAO** is an organization governed by smart contracts and decisions made collectively by its members, typically through voting. [Learn more about DAOs](https://ethereum.org/en/dao/).

The aim of this project is to create a Python-based application that automates the monitoring and notification of active proposals on the **Snapshot** voting platform. **Snapshot** is a decentralized governance platform used by many DAOs to manage proposal-based voting in a gasless and off-chain manner. [Read more about Snapshot](https://docs.snapshot.org/).

The application fetches proposals from specified Snapshot spaces, checks if they are currently active, and sends real-time notifications to specified Telegram users. This solution enhances user engagement in decentralized governance by providing timely updates and reducing the manual effort required to monitor multiple DAO spaces.

---

## Features

1. **Proposal Monitoring**
   - Fetch proposals from multiple Snapshot spaces using their unique space IDs.
   - Filter and identify proposals that are currently active based on start and end times.

2. **Telegram Notifications**
   - Send automated notifications to a list of predefined Telegram chat IDs when active proposals are identified.
   - Notifications include details like the DAO space, proposal title, and other relevant metadata.

3. **Tracking Sent Notifications**
   - Maintain a record of sent proposal notifications to avoid duplicate alerts.
   - Use a local text file to store IDs of proposals already notified.

4. **Error Handling and Logs**
   - Log errors encountered during API calls or notification processing for debugging and optimization.
   - Provide informative messages on failed notifications or data-fetching attempts.

---

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2. Ensure Python 3.x is installed on your machine:
    ```bash
    python --version
    ```

3. Install the required Python libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure the script by updating the following variables in the main script (`main.py` or the primary execution file):

    - **`bot_token`**: Your Telegram bot token (you can create a Telegram bot using [BotFather](https://t.me/botfather)).
    - **`chat_ids`**: List of Telegram chat IDs to send notifications to. You can get your chat ID from [this guide](https://t.me/userinfobot).
    - **`space_ids`**: List of Snapshot space IDs to monitor. You can find space IDs by visiting a DAO’s page on Snapshot (e.g., `aave.eth`).
    - **`sent_ids_file`**: Path to the local file where IDs of sent notifications are tracked (default: `sent_proposals.txt`).

---

## Workflow

1. **Initialization**
   - Set up the list of Snapshot space IDs, Telegram bot token, and Telegram chat IDs.
   - Initialize a local file to track the IDs of notified proposals.

2. **Proposal Fetching**
   - The script queries the Snapshot GraphQL API to retrieve proposals from the specified spaces.
   - Proposal data is parsed and formatted for processing.

3. **Notification Dispatch**
   - The script identifies active proposals based on current time and proposal start/end times.
   - Notifications for new active proposals are sent to the configured Telegram chat IDs.

4. **Tracking and Optimization**
   - Once a notification is sent, the proposal ID is logged to the tracking file to avoid duplicate notifications.
   - The script handles API rate limits and errors gracefully, optimizing performance and reliability.

---

## Example Setup

Here’s a step-by-step example of how to customize and run the project:

1. **Choose Snapshot Spaces:** Decide which DAO spaces you want to track. For example:
    ```python
    space_ids = ['aave.eth', 'uniswap.eth', 'balancer.eth']
    ```

2. **Add Your Telegram Chat IDs:** Insert the chat IDs of users or groups where notifications should be sent:
    ```python
    chat_ids = ['123456789', '987654321']
    ```

3. **Set Up the Bot Token:** Replace `bot_token` with your Telegram bot token from BotFather:
    ```python
    bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'
    ```

4. **Run the Script:** Execute the main script to start monitoring proposals:
    ```bash
    python main.py
    ```

---

## Technical Stack

- **Core Language**: Python
- **APIs**:
  - [Snapshot GraphQL API](https://docs.snapshot.org/graphql) for fetching proposals.
  - [Telegram Bot API](https://core.telegram.org/bots/api) for sending notifications.
- **Libraries**: `requests`, `datetime`
- **File Storage**: Local text file to track notified proposal IDs

---

## Future Enhancements (Planned)

- **Web Interface**: Develop a web-based dashboard to visualize active proposals and notification history.
- **Notification Preferences**: Enable users to set notification preferences, such as only receiving updates for certain DAO spaces or proposal types.
- **Database Integration**: Replace the local text file with a database to enhance scalability and query capabilities.

---

By implementing this project, DAO participants can stay updated on governance activities with minimal effort, fostering increased participation and streamlined decision-making.
