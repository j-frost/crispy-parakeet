import os
import threading

import discord
import requests
from google.cloud import logging
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from quart import Quart, abort, jsonify, request

from crispy_parakeet import CrispyParakeet

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
PUBLIC_KEY = os.getenv('APPLICATION_PUBLIC_KEY')


web_app = Quart(__name__)
crispy_parakeet = CrispyParakeet()
logger = logging.Client(project='crispy-parakeet').logger('crispy-parakeet')


@web_app.route('/', methods=['POST'])
async def interactions():
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = (await request.data).decode("utf-8")

    try:
        verify_key.verify(
            f'{timestamp}{body}'.encode(),
            bytes.fromhex(signature)
        )
    except BadSignatureError:
        abort(401, 'invalid request signature')

    interaction_json = await request.json

    logger.log_struct({
        'message': 'Received interaction',
        'interaction': interaction_json
    })
    if interaction_json['type'] == 1:
        return jsonify({
            'type': 1
        })
    else:
        options = interaction_json['data']['options']
        await crispy_parakeet.distribute(
            next(o for o in options if o['name'] == 'source')['value'],
            next(o for o in options if o['name'] == 'team-1')['value'],
            next(o for o in options if o['name'] == 'team-2')['value']
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
        raise Exception(response.content)


if __name__ == '__main__':
    client_daemon = threading.Thread(
        name='crispy parakeet bot client',
        target=crispy_parakeet.run,
        args=(DISCORD_TOKEN)
    )
    client_daemon.setDaemon(True)
    client_daemon.start()
    register_commands()
    web_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
