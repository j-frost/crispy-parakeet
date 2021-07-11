import os
import discord
import requests
from crispy_parakeet import CrispyParakeet
from flask import Flask, jsonify, abort, request
import threading
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
APPLICATION_PUBLIC_KEY = os.getenv('APPLICATION_PUBLIC_KEY')


app = Flask(__name__)
crispy_parakeet = CrispyParakeet()


@app.route('/', methods=['POST'])
def handle_command():
    print(request)
    verify_key = VerifyKey(bytes.fromhex(APPLICATION_PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.data.decode("utf-8")

    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, 'invalid request signature')

    if request.json['type'] == 1:
        return jsonify({
            'type': 1
        })
    else:
        return jsonify({
            'type': 4,
            'data': {
                'tts': False,
                'content': 'Congrats on sending your command!',
                'embeds': [],
                'allowed_mentions': {'parse': []}
            }
        })


def register_commands():
    response = requests.post(
        f'https://discord.com/api/v8/applications/{APPLICATION_ID}/guilds/847919277612073071/commands',
        headers={'Authorization': f'Bot {DISCORD_TOKEN}'},
        json={
            'name': 'distribute',
            'description': 'Moves all users from source channel randomly to one of the two target team channels',
            'options': [
                {
                    'name': 'source',
                    'description': 'Channel from which to move users',
                    'type': 7,
                    'required': True
                },
                {
                    'name': 'team-1',
                    'description': 'Target channel of team 1',
                    'type': 7,
                    'required': True
                },
                {
                    'name': 'team-2',
                    'description': 'Target channel of team 2',
                    'type': 7,
                    'required': True
                }
            ]
        }
    )
    if response.status_code not in range(200, 300):
        raise Exception(response)


if __name__ == '__main__':
    daemon = threading.Thread(
        name='bogus web server',
        target=app.run,
        kwargs={'host': '0.0.0.0', 'port': int(os.environ.get('PORT', 8080))}
    )
    daemon.setDaemon(True)
    daemon.start()
    register_commands()
    crispy_parakeet.run(DISCORD_TOKEN)
