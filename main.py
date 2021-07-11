import os
import discord
import requests
from crispy_parakeet import CrispyParakeet
from flask import Flask, jsonify, abort, request
import threading
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from discord_interactions import verify_key_decorator
import asyncio

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
PUBLIC_KEY = os.getenv('APPLICATION_PUBLIC_KEY')


app = Flask(__name__)
crispy_parakeet = CrispyParakeet()
loop = asyncio.get_event_loop()

@app.route('/', methods=['POST'])
@verify_key_decorator(PUBLIC_KEY)
def interactions():
    print(request)
    if request.json['type'] == 1:
        return jsonify({
            'type': 1
        })
    else:
        options = request.json['data']['options']
        loop.run_until_complete(
            crispy_parakeet.distribute(
                next(o for o in options if o.name == 'source').value, 
                next(o for o in options if o.name == 'team-1').value, 
                next(o for o in options if o.name == 'team-2').value, 
            )
        )
        return jsonify({
            'type': 4,
            'data': {
                'tts': False,
                'content': 'You got it!',
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
