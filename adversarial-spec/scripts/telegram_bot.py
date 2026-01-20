#!/usr/bin/env python3
"""Telegram bot utilities for adversarial spec notifications."""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional

TELEGRAM_API_BASE = "https://api.telegram.org/bot"
MAX_MESSAGE_LENGTH = 4096


def get_config() -> tuple[Optional[str], Optional[str]]:
    """Get Telegram bot token and chat ID from environment."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    return token, chat_id


def is_configured() -> bool:
    """Check if Telegram is configured."""
    token, chat_id = get_config()
    return bool(token and chat_id)


def send_message(
    text: str,
    token: Optional[str] = None,
    chat_id: Optional[str] = None,
    parse_mode: str = "Markdown",
) -> bool:
    """Send a message to Telegram."""
    if not token or not chat_id:
        token, chat_id = get_config()

    if not token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set", file=sys.stderr)
        return False

    # Split long messages
    messages = split_message(text)

    for msg in messages:
        url = f"{TELEGRAM_API_BASE}{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": parse_mode,
        }

        try:
            req = urllib.request.Request(
                url,
                data=urllib.parse.urlencode(data).encode(),
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read())
                if not result.get("ok"):
                    print(f"Telegram API error: {result}", file=sys.stderr)
                    return False
        except urllib.error.URLError as e:
            print(f"Error sending to Telegram: {e}", file=sys.stderr)
            return False

        # Rate limit between messages
        if len(messages) > 1:
            time.sleep(0.5)

    return True


def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """Split a message into chunks that fit Telegram's limit."""
    if len(text) <= max_length:
        return [text]

    messages = []
    remaining = text

    while remaining:
        if len(remaining) <= max_length:
            messages.append(remaining)
            break

        # Find a good split point (paragraph, then sentence, then word)
        chunk = remaining[:max_length]

        # Try to split at paragraph
        split_idx = chunk.rfind("\n\n")
        if split_idx < max_length // 2:
            # Try to split at sentence
            split_idx = chunk.rfind(". ")
            if split_idx < max_length // 2:
                # Try to split at word
                split_idx = chunk.rfind(" ")
                if split_idx < max_length // 2:
                    # Just cut at max length
                    split_idx = max_length - 1

        messages.append(remaining[:split_idx + 1].strip())
        remaining = remaining[split_idx + 1:].strip()

    return messages


def poll_for_response(
    token: Optional[str] = None,
    chat_id: Optional[str] = None,
    timeout: int = 60,
    poll_interval: int = 5,
) -> Optional[str]:
    """Poll for a user response within timeout."""
    if not token or not chat_id:
        token, chat_id = get_config()

    if not token or not chat_id:
        return None

    url = f"{TELEGRAM_API_BASE}{token}/getUpdates"
    start_time = time.time()
    last_update_id = 0

    # Get current update offset
    try:
        req = urllib.request.Request(f"{url}?offset=-1&limit=1")
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read())
            if result.get("ok") and result.get("result"):
                last_update_id = result["result"][-1]["update_id"]
    except Exception:
        pass

    while time.time() - start_time < timeout:
        try:
            params = f"?offset={last_update_id + 1}&timeout={poll_interval}"
            req = urllib.request.Request(f"{url}{params}")
            with urllib.request.urlopen(req, timeout=poll_interval + 5) as response:
                result = json.loads(response.read())

            if result.get("ok") and result.get("result"):
                for update in result["result"]:
                    last_update_id = update["update_id"]
                    message = update.get("message", {})

                    # Check if message is from the right chat
                    if str(message.get("chat", {}).get("id")) == str(chat_id):
                        text = message.get("text", "")
                        if text:
                            return text

        except urllib.error.URLError:
            time.sleep(1)
        except Exception as e:
            print(f"Error polling Telegram: {e}", file=sys.stderr)
            time.sleep(1)

    return None


def notify_and_wait(
    message: str,
    timeout: int = 60,
    token: Optional[str] = None,
    chat_id: Optional[str] = None,
) -> dict:
    """Send a notification and wait for response."""
    if not send_message(message, token, chat_id):
        return {"success": False, "error": "Failed to send message"}

    response = poll_for_response(token, chat_id, timeout)

    return {
        "success": True,
        "response": response,
        "timed_out": response is None,
    }


def setup_instructions():
    """Print setup instructions."""
    print("""
Telegram Bot Setup
==================

1. Create a bot via @BotFather:
   - Open Telegram and search for @BotFather
   - Send /newbot and follow the prompts
   - Copy the bot token (looks like: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)

2. Get your chat ID:
   - Start a chat with your new bot
   - Send any message to it
   - Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   - Find "chat":{"id": YOUR_CHAT_ID}

3. Set environment variables:
   export TELEGRAM_BOT_TOKEN="your-bot-token"
   export TELEGRAM_CHAT_ID="your-chat-id"

4. Test:
   echo "Hello from adversarial-spec!" | python3 telegram_bot.py send

Usage:
------
  python3 telegram_bot.py setup     - Show these instructions
  python3 telegram_bot.py send      - Send message from stdin
  python3 telegram_bot.py poll      - Wait for incoming message
  python3 telegram_bot.py notify    - Send message and wait for reply
""")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        setup_instructions()
        sys.exit(0)

    command = sys.argv[1]

    if command == "setup":
        setup_instructions()

    elif command == "send":
        if not is_configured():
            print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set", file=sys.stderr)
            sys.exit(2)

        text = sys.stdin.read().strip()
        if not text:
            print("Error: No message provided on stdin", file=sys.stderr)
            sys.exit(1)

        if send_message(text):
            print("Message sent successfully")
        else:
            sys.exit(1)

    elif command == "poll":
        if not is_configured():
            print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set", file=sys.stderr)
            sys.exit(2)

        timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        print(f"Waiting for message (timeout: {timeout}s)...", file=sys.stderr)

        response = poll_for_response(timeout=timeout)
        if response:
            print(response)
        else:
            print("No response received", file=sys.stderr)
            sys.exit(1)

    elif command == "notify":
        if not is_configured():
            print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set", file=sys.stderr)
            sys.exit(2)

        text = sys.stdin.read().strip()
        if not text:
            print("Error: No message provided on stdin", file=sys.stderr)
            sys.exit(1)

        timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        result = notify_and_wait(text, timeout)
        print(json.dumps(result))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        setup_instructions()
        sys.exit(1)


if __name__ == "__main__":
    main()
