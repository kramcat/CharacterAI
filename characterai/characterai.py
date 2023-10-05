from contextlib import contextmanager
import tls_client
import json

from characterai import errors
from characterai.pyasynccai import PyAsyncCAI

__all__ = ['PyCAI', 'PyAsyncCAI']

class PyCAI:
    def __init__(
        self, token: str = None, plus: bool = False
    ):
        self.token = token

        if plus: sub = 'plus'
        else: sub = 'beta'

        self.session = tls_client.Session(
            client_identifier='chrome112'
        )

        setattr(self.session, 'url', f'https://{sub}.character.ai/')
        setattr(self.session, 'token', token)

        self.user = self.user(token, self.session)
        self.post = self.post(token, self.session)
        self.character = self.character(token, self.session)
        self.chat = self.chat(token, self.session)

    def request(
        url: str, session: tls_client.Session,
        *, token: str = None, method: str = 'GET',
        data: dict = None, split: bool = False,
        neo: bool = False
    ):
        if neo:
            link = f'https://neo.character.ai/{url}'
        else:
            link = f'{session.url}{url}'

        if token == None:
            key = session.token
        else:
            key = token

        headers = {
            'Authorization': f'Token {key}'
        }

        if method == 'GET':
            response = session.get(
                link, headers=headers
            )

        elif method == 'POST':
            response = session.post(
                link, headers=headers, json=data
            )

        elif method == 'PUT':
            response = session.put(
                link, headers=headers, json=data
            )

        if split:
            data = json.loads(response.text.split('\n')[-2])
        else:
            data = response.json()

        if str(data).startswith("{'command': 'neo_error'"):
            raise errors.ServerError(data['comment'])
        elif str(data).startswith("{'detail': 'Auth"):
            raise errors.AuthError('Invalid token')
        elif str(data).startswith("{'status': 'Error"):
            raise errors.ServerError(data['status'])
        elif str(data).startswith("{'error'"):
            raise errors.ServerError(data['error'])
        else:
            return data

    def ping(self):
        return self.session.get(
            'https://neo.character.ai/ping/'
        ).json()

    class user:
        """Responses from site for user info

        user.info()
        user.get_profile('USERNAME')
        user.followers()
        user.following()
        user.update('USERNAME')

        """
        def __init__(
            self, token: str, session: tls_client.Session
        ):
            self.token = token
            self.session = session

        def info(self, *, token: str = None):
            return PyCAI.request(
                'chat/user/', self.session, token=token
            )

        def get_profile(
            self, username: str, *,
            token: str = None
        ):
            return PyCAI.request(
                'chat/user/public/', self.session,
                token=token, method='POST',
                data={
                    'username': username
                }
            )

        def followers(self, *, token: str = None):
            return PyCAI.request(
                'chat/user/followers/', self.session, token=token
            )

        def following(self, *, token: str = None):
            return PyCAI.request(
                'chat/user/following/', self.session, token=token
            )
        
        def recent(self, *, token: str = None):
            return PyCAI.request(
                'chat/characters/recent/', self.session, token=token
            )

        def characters(self, *, token: str = None):
            return PyCAI.request(
                'chat/characters/?scope=user',
                self.session, token=token
            )

        def update(
            self, username: str,
            *, token: str = None,
            **kwargs
        ):
            return PyCAI.request(
                'chat/user/update/', self.session,
                token=token, method='POST',
                data={
                    'username': username,
                    **kwargs
                }
            )

    class post:
        """Just a responses from site for posts
        
        post.get_post('POST_ID')
        post.my_posts()
        post.get_posts('USERNAME')
        post.upvote('POST_ID')
        post.undo_upvote('POST_ID')
        post.send_comment('POST_ID', 'TEXT')
        post.delete_comment('MESSAGE_ID', 'POST_ID')
        post.create('HISTORY_ID', 'TITLE')
        post.delete('POST_ID')

        """
        def __init__(
            self, token: str, session: tls_client.Session
        ):
            self.token = token
            self.session = session

        def get_post(
            self, post_id: str
        ):
            return PyCAI.request(
                f'chat/post/?post={post_id}',
                self.session
            )

        def my(
            self, *, posts_page: int = 1,
            posts_to_load: int = 5, token: str = None
        ):
            return PyCAI.request(
                f'chat/posts/user/?scope=user&page={posts_page}'
                f'&posts_to_load={posts_to_load}/',
                self.session
            )

        def get_posts(
            self, username: str, *,
            posts_page: int = 1, posts_to_load: int = 5,
        ):
            return PyCAI.request(
                f'chat/posts/user/?username={username}'
                f'&page={posts_page}&posts_to_load={posts_to_load}/',
                self.session
            )

        def upvote(
            self, post_external_id: str,
            *, token: str = None
        ):
            return PyCAI.request(
                'chat/post/upvote/', self.session,
                token=token, method='POST',
                data={
                    'post_external_id': post_external_id
                }
            )

        def undo_upvote(
            self, post_external_id: str,
            *, token: str = None
        ):
            return PyCAI.request(
                'chat/post/undo-upvote/', self.session,
                token=token, method='POST',
                data={
                    'post_external_id': post_external_id
                }
            )

        def send_comment(
            self, post_id: str, text: str, *,
            parent_uuid: str = None, token: str = None
        ):
            return PyCAI.request(
                'chat/comment/create/', self.session,
                token=token, method='POST',
                data={
                    'post_external_id': post_id,
                    'text': text,
                    'parent_uuid': parent_uuid
                }
            )

        def delete_comment(
            self, message_id: int, post_id: str,
            *, token: str = None
        ):
            return PyCAI.request(
                'chat/comment/delete/', self.session,
                token=token, method='POST',
                data={
                    'external_id': message_id,
                    'post_external_id': post_id
                }
            )

        def create(
            self, post_type: str, external_id: str,
            title: str, text: str = '',
            post_visibility: str = 'PUBLIC',
            token: str = None, **kwargs
        ):
            if post_type == 'POST':
                post_link = 'chat/post/create/'
                data = {
                    'post_title': title,
                    'topic_external_id': external_id,
                    'post_text': text,
                    **kwargs
                }
            elif post_type == 'CHAT':
                post_link = 'chat/chat-post/create/'
                data = {
                    'post_title': title,
                    'subject_external_id': external_id,
                    'post_visibility': post_visibility,
                    **kwargs
                }
            else:
                raise errors.PostTypeError('Invalid post_type')

            return PyCAI.request(
                post_link, self.session,
                token=token, method='POST'
            )

        def delete(
            self, post_id: str, *,
            token: str = None
        ):
            return PyCAI.request(
                'chat/post/delete/', self.session,
                token=token, method='POST',
                data={
                    'external_id': post_id
                }
            )

        def get_topics(self):
            return PyCAI.request(
                'chat/topics/', self.session
            )

        def feed(
            self, topic: str, num: int = 1, 
            load: int = 5, sort: str = 'top', *,
            token: str = None
        ):
            return PyCAI.request(
                f'chat/posts/?topic={topic}&page={num}'
                f'&posts_to_load={load}&sort={sort}',
                self.session, token=token
            )

    class character:
        """Just a responses from site for characters

        character.create()
        character.update()
        character.trending()
        character.recommended()
        character.categories()
        character.info('CHAR')
        character.search('QUERY')
        character.voices()

        """
        def __init__(
            self, token: str, session: tls_client.Session
        ):
            self.token = token
            self.session = session

        def create(
            self, greeting: str, identifier: str,
            name: str, *, avatar_rel_path: str = '',
            base_img_prompt: str = '', categories: list = [],
            copyable: bool = True, definition: str = '',
            description: str = '', title: str = '',
            img_gen_enabled: bool = False,
            visibility: str = 'PUBLIC',
            token: str = None, **kwargs
        ):
            return PyCAI.request(
                '../chat/character/create/', self.session,
                token=token, method='POST',
                data={
                    'greeting': greeting,
                    'identifier': identifier,
                    'name': name,
                    'avatar_rel_path': avatar_rel_path,
                    'base_img_prompt': base_img_prompt,
                    'categories': categories,
                    'copyable': copyable,
                    'definition': definition,
                    'description': description,
                    'img_gen_enabled': img_gen_enabled,
                    'title': title,
                    'visibility': visibility,
                    **kwargs
                }
            )

        def update(
            self, external_id: str, greeting: str,
            identifier: str, name: str, title: str = '',
            categories: list = [], definition: str = '',
            copyable: bool = True, description: str = '',
            visibility: str = 'PUBLIC', *,
            token: str = None, **kwargs
        ):
            return PyCAI.request(
                '../chat/character/update/', self.session,
                token=token, method='POST',
                data={
                    'external_id': external_id,
                    'name': name,
                    'categories': categories,
                    'title': title,
                    'visibility': visibility,
                    'copyable': copyable,
                    'description': description,
                    'greeting': greeting,
                    'definition': definition,
                    **kwargs
                }
            )
        
        def trending(self):
            return PyCAI.request(
                'chat/characters/trending/',
                self.session
            )

        def recommended(
            self, *, token: str = None
        ):
            return PyCAI.request(
                'chat/characters/recommended/',
                self.session, token=token
            )

        def categories(self):
            return PyCAI.request(
                'chat/character/categories/',
                self.session
            )

        def info(
            self, char: str, *,
            token: str = None,
        ):
            return PyCAI.request(
                'chat/character/', self.session,
                token=token, method='POST',
                data={
                    'external_id': char
                }
            )

        def search(
            self, query: str, *,
            token: str = None
        ):
            return PyCAI.request(
                f'chat/characters/search/?query={query}/',
                self.session, token=token
            )

        def voices(self):
            return PyCAI.request(
                'chat/character/voices/',
                self.session
            )

    class chat:
        """Managing a chat with a character

        chat.create_room('CHARACTERS', 'NAME', 'TOPIC')
        chat.rate(NUM, 'HISTORY_ID', 'MESSAGE_ID')
        chat.next_message('CHAR', 'MESSAGE')
        chat.get_histories('CHAR')
        chat.get_history('HISTORY_EXTERNAL_ID')
        chat.get_chat('CHAR')
        chat.send_message('CHAR', 'MESSAGE')
        chat.delete_message('HISTORY_ID', 'UUIDS_TO_DELETE')
        chat.new_chat('CHAR')

        """
        def __init__(
            self, token: str, session: tls_client.Session
        ):
            self.token = token
            self.session = session

        def create_room(
            self, characters: list, name: str,
            topic: str = '', *, token: str = None,
            **kwargs
        ):
            return PyCAI.request(
                '../chat/room/create/', self.session,
                token=token, method='POST',
                data={
                    'characters': characters,
                    'name': name,
                    'topic': topic,
                    'visibility': 'PRIVATE',
                    **kwargs
                }
            )

        def rate(
            self, rate: int, history_id: str,
            message_id: str, *, token: str = None,
            **kwargs
        ):
            if rate == 0: label = [234, 238, 241, 244] #Terrible
            elif rate == 1: label = [235, 237, 241, 244] #Bad
            elif rate == 2: label = [235, 238, 240, 244] #Good
            elif rate == 3: label = [235, 238, 241, 243] #Fantastic
            else: raise errors.LabelError('Wrong Rate Value')

            return PyCAI.request(
                'chat/annotations/label/', self.session,
                token=token, method='PUT',
                data={
                    'label_ids': label,
                    'history_external_id': history_id,
                    'message_uuid': message_id,
                    **kwargs
                }
            )

        def next_message(
            self, history_id: str, parent_msg_uuid: str,
            tgt: str, *, token: str = None, **kwargs
        ):
            response = PyCAI.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'parent_msg_uuid': parent_msg_uuid,
                    'tgt': tgt,
                    **kwargs
                }
            )

        def get_histories(
            self, char: str, *, number: int = 50,
            token: str = None
        ):
            return PyCAI.request(
                'chat/character/histories_v2/', self.session,
                token=token, method='POST',
                data={'external_id': char, 'number': number},
            )

        def get_history(
            self, history_id: str = None,
            *, token: str = None
        ):
            return PyCAI.request(
                'chat/history/msgs/user/?'
                f'history_external_id={history_id}',
                self.session, token=token
            )

        def get_chat(
            self, char: str = None, *,
            token: str = None, **kwargs
        ):
            return PyCAI.request(
                'chat/history/continue/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char,
                    **kwargs
                }
            )

        def send_message(
            self, history_id: str, tgt: str, text: str,
            *, token: str = None, **kwargs
        ):
            return PyCAI.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'tgt': tgt,
                    'text': text,
                    **kwargs
                }
            )

        def delete_message(
            self, history_id: str, uuids_to_delete: list,
            *, token: str = None, **kwargs
        ):
            return PyCAI.request(
                'chat/history/msgs/delete/', self.session,
                token=token, method='POST',
                data={
                    'history_id': history_id,
                    'uuids_to_delete': uuids_to_delete,
                    **kwargs
                }
            )

        def new_chat(
            self, char: str, *, token: str = None
        ):
            return PyCAI.request(
                'chat/history/create/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char
                }
            )
