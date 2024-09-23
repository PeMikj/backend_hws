import json
import math
from http import HTTPStatus
from urllib.parse import parse_qs

async def app(scope, receive, send):
    if scope['type'] == 'http':
        method = scope['method']
        path = scope['path']

        # Factorial endpoint
        if method == 'GET' and path == '/factorial':
            query_string = scope['query_string'].decode()
            query_params = parse_qs(query_string)

            if 'n' not in query_params or len(query_params['n']) == 0:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': 'UNPROCESSABLE_ENTITY'}).encode(),
                })
                return

            try:
                n = int(query_params['n'][0])
                if n < 0:
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.BAD_REQUEST,
                        'headers': [(b'content-type', b'application/json')],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({'result': 'BAD_REQUEST'}).encode(),
                    })
                    return

                result = math.factorial(n)

                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.OK,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': result}).encode(),
                })

            except ValueError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': 'UNPROCESSABLE_ENTITY'}).encode(),
                })

        # Fibonacci endpoint
        elif method == 'GET' and path.startswith('/fibonacci/'):
            path_parts = path.split('/')
            
            if len(path_parts) != 3:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.BAD_REQUEST,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': 'BAD_REQUEST'}).encode(),
                })
                return

            n_str = path_parts[-1]
            try:
                n = int(n_str)
                if n < 0:
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.BAD_REQUEST,
                        'headers': [(b'content-type', b'application/json')],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({'result': 'BAD_REQUEST'}).encode(),
                    })
                    return

                a, b = 0, 1
                for _ in range(n):
                    a, b = b, a + b

                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.OK,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': b}).encode(),
                })

            except ValueError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': 'UNPROCESSABLE_ENTITY'}).encode(),
                })

        # Mean endpoint
        elif method == 'GET' and path == '/mean':
            body = await receive()
            body_data = body.get('body')
            try:
                data = json.loads(body_data.decode())

                if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                        'headers': [(b'content-type', b'application/json')],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({'result': 'UNPROCESSABLE_ENTITY'}).encode(),
                    })
                    return
                
                if len(data) == 0:
                    await send({
                        'type': 'http.response.start',
                        'status': HTTPStatus.BAD_REQUEST,
                        'headers': [(b'content-type', b'application/json')],
                    })
                    await send({
                        'type': 'http.response.body',
                        'body': json.dumps({'result': 'BAD_REQUEST'}).encode(),
                    })
                    return

                result = sum(data) / len(data)

                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.OK,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': result}).encode(),
                })

            except ValueError:
                await send({
                    'type': 'http.response.start',
                    'status': HTTPStatus.UNPROCESSABLE_ENTITY,
                    'headers': [(b'content-type', b'application/json')],
                })
                await send({
                    'type': 'http.response.body',
                    'body': json.dumps({'result': 'UNPROCESSABLE_ENTITY'}).encode(),
                })

        else:
            await send({
                'type': 'http.response.start',
                'status': HTTPStatus.NOT_FOUND,
                'headers': [(b'content-type', b'application/json')],
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'result': 'Not Found'}).encode(),
            })
