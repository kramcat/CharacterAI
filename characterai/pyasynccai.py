import asyncio
import json

from playwright.async_api import async_playwright, \
    TimeoutError as PlaywrightTimeoutError

from characterai import errors

_page = None

__all__ = ['PyCAI', 'PyAsyncCAI']

async def _goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        await _page.set_extra_http_headers(
            {"Authorization": f"Token {token}"}
        )

    try:
        await _page.goto(link)
    except Exception as E:
        raise errors.UnknownError(E)

    content = await (_page.locator('body').inner_text())

    if content.startswith('Not Found'):
        raise errors.NotFoundError(content.split('\n')[-1])
    elif content == 'No history found for id provided.':
        raise errors.NotFoundError(content)
    elif content.startswith('{"error":'):
        raise errors.ServerError(json.loads(content)['error']) 
    elif content.startswith('{"detail":'):
        raise errors.AuthError(json.loads(content)['detail']) 

    if await _page.title() != 'Waiting Room powered by Cloudflare':
        return _page
    else:
        if wait:
            await _page.wait_for_selector(
                'div#wrapper', state='detached', timeout=0
            )
            await _goto(link=link, wait=wait, token=token)
        else:
            raise errors.NoResponse('The Site is Overloaded')

async def _GetResponse(
        link: str, *, wait: bool = False,
        token: str = None
    ):
    await _goto(link, wait=wait, token=token)
    return json.loads(await (_page.locator('body').inner_text()))

async def _PostResponse(
        post_link: str, data: str, *,
        send_json: bool = True, method: str = 'POST',
        wait: bool = False, token: str = None
    ):
    await _goto('', wait=wait, token=token)

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }

    data = json.dumps(data)
    
    async with _page.expect_response(post_link) as response_info:
        await _page.evaluate(
            "fetch('"
            + post_link + "', {method: '"
            + method + "',body: JSON.stringify("
            + data + "),headers: new Headers("
            + str(headers) + "),})"
        )

    response = await response_info.value

    if response.status != 200:
        raise errors.ServerError(response.status_text) 

    if send_json: return await response.json()
    else: return await response.text()

class PyAsyncCAI:
    def __init__(self, token: str = None):
        self.token = token

        self.user = self.user()
        self.post = self.post()
        self.character = self.character()
        self.chat = self.chat()

    async def start(
        self, *, headless: bool = True,
        plus: bool = False, timeout: int = 0
    ):
        global _page

        if plus: url = 'https://plus.character.ai'
        else: url = 'https://beta.character.ai'

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(
            headless=headless)
        self.context = await self.browser.new_context(
            extra_http_headers={"Authorization": f"Token {self.token}"},
            base_url=url
        )
        _page = await self.context.new_page()
        _page.set_default_timeout(timeout)

    async def ping(self):
        await _page.goto('https://neo.character.ai/ping/')
        return json.loads(await (_page.locator('body').inner_text()))

    async def upload_image(
        self, path, *, wait: bool = False
    ):
        await _page.goto('chat')

        close1 = _page.locator('//*[@id="mobile-app-modal-close"]')
        close2 = _page.locator('//*[@id="#AcceptButton"]')

        if await close1.is_visible(): await close1.click()
        if await close2.is_visible(): await close2.click()

        await _page.click("div.col-auto.ps-2.dropdown.dropup")
        await _page.get_by_text("🖼").click()

        async with _page.expect_response(
            'chat/upload-image/'
        ) as response_info:
            async with _page.expect_file_chooser() as file_info:
                await _page.click("[name='img']")

            file_chooser = await file_info.value
            await file_chooser.set_files(path)

        response = await response_info.value
        return await response.json()

    class user:
        """Just a responses from site for user info

        user.info()
        user.get_profile('USERNAME')
        user.followers()
        user.following()
        user.update('USERNAME')

        """
        async def info(
            self, *, wait: bool = False, token: str = None
        ):
            return await _GetResponse('chat/user/', wait=wait, token=token)

        async def get_profile(
            self, username: str, *,
            wait: bool = False
        ):
            return await _PostResponse(
                post_link='chat/user/public/',
                data={'username': username},
                wait=wait
            )

        async def followers(self, *, wait: bool = False, token: str = None):
            return await _GetResponse(
                'chat/user/followers/', wait=wait, token=token
            )

        async def following(self, *, wait: bool = False, token: str = None):
            return await _GetResponse(
                'chat/user/following/',
                wait=wait, token=token
            )
        
        async def recent(self, *, wait: bool = False, token: str = None):
            return await _GetResponse(
                'chat/characters/recent/',
                wait=wait, token=token
            )

        async def update(
            self, username: str, *,
            wait: bool = False, token: str = None,
            **kwargs
        ):
            return await _PostResponse(
                post_link='chat/user/update/',
                data={
                    'username': username,
                    **kwargs
                },
                wait=wait, token=token
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
        async def get_post(
            self, post_id: str, *,
            wait: bool = False
        ):
            return await _GetResponse(
                f'chat/post/?post={post_id}',
                wait=wait
            )
        
        async def my_posts(
            self, *, posts_page: int = 1,
            posts_to_load: int = 5, wait: bool = False,
            token: str = None
        ):
            return await _GetResponse(
                f'chat/posts/user/?scope=user&page={posts_page}'
                f'&posts_to_load={posts_to_load}/',
                wait=wait, token=token
            )

        async def get_posts(
            self, username: str, *,
            posts_page: int = 1, posts_to_load: int = 5,
            wait: bool = False
        ):
            return await _GetResponse(
                f'chat/posts/user/?username={username}'
                f'&page={posts_page}&posts_to_load={posts_to_load}/',
                wait=wait
            )

        async def upvote(
            self, post_external_id: str, *,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/post/upvote/',
                data={
                    'post_external_id': post_external_id
                },
                wait=wait, token=token
            )

        async def undo_upvote(
            self, post_external_id: str, *,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/post/undo-upvote/',
                data={
                    'post_external_id': post_external_id
                },
                wait=wait, token=token
            )

        async def send_comment(
            self, post_id: str, text: str, *,
            parent_uuid: str = None, wait: bool = False,
            token: str = None
        ):
            return await _PostResponse(
                post_link='chat/comment/create/',
                data={
                    'post_external_id': post_id,
                    'text': text,
                    'parent_uuid': parent_uuid
                },
                wait=wait, token=token
            )

        async def delete_comment(
            self, message_id: int, post_id: str, *,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/comment/delete/',
                data={
                    'external_id': message_id,
                    'post_external_id': post_id
                },
                wait=wait, token=token
            )

        async def create(
            self, post_type: str, external_id: str,
            title: str, text: str = '', wait: bool = False,
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
                raise errors.PostTypeError('Wrong post_type')

            return await _PostResponse(
                post_link=post_link,
                data=data, wait=wait, token=token
            )

        async def delete(
            self, post_id: str, *,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/post/delete/',
                data={'external_id': post_id},
                wait=wait, token=token
            )

        async def get_topics(
            self, *, wait: bool = False
        ):
            return await _GetResponse(
                'chat/topics/',
                wait=wait, token=token
            )

        async def feed(
            self, topic: str, num_page: int = 1, 
            posts_to_load: int = 5, sort: str = 'top', *,
            wait: bool = False, token: str = None
        ):
            return await _GetResponse(
                f'posts/?topic={topic}&page={num_page}'
                f'&posts_to_load={posts_to_load}&sort={sort}',
                wait=wait, token=token
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
        async def create(
            self, greeting: str, identifier: str,
            name: str, *, avatar_rel_path: str = '',
            base_img_prompt: str = '', categories: list = [],
            copyable: bool = True, definition: str = '',
            description: str = '', title: str = '',
            img_gen_enabled: bool = False,
            visibility: str = 'PUBLIC', wait: bool = False,
            token: str = None, **kwargs
        ):
            return await _PostResponse(
                post_link='../chat/character/create/',
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
                },
                wait=wait, token=token
            )

        async def update(
            self, external_id: str, greeting: str,
            identifier: str, name: str, title: str = '',
            categories: list = [], definition: str = '',
            copyable: bool = True, description: str = '',
            visibility: str = 'PUBLIC', *,
            wait: bool = False, token: str = None, **kwargs
        ):
            return await _PostResponse(
                post_link='../chat/character/update/',
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
                },
                wait=wait, token=token
            )
        
        async def trending(self, *, wait: bool = False):
            return await _GetResponse(
                'chat/characters/trending/', wait=wait
            )

        async def recommended(
            self, *, wait: bool = False,
            token: str = None
        ):
            return await _GetResponse(
                'chat/characters/recommended/', 
                wait=wait, token=token
            )

        async def categories(
            self, *, wait: bool = False
        ):
            return await _GetResponse(
                'chat/character/categories/', 
                wait=wait
            )

        async def info(
            self, char: str, *, wait: bool = False
        ):
            return await _GetResponse(
                f'chat/character/info-cached/{char}/', 
                wait=wait
            )

        async def search(
            self, query: str, *, wait: bool = False
        ):
            return await _GetResponse(
                f'chat/characters/search/?query={query}/', 
                wait=wait
            )

        async def voices(
            self, *, wait: bool = False
        ):
            return await _GetResponse(
                'chat/character/voices/', wait=wait
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
        async def create_room(
            self, characters: list, name: str,
            topic: str = '', *, wait: bool = False,
            token: str = None, **kwargs
        ):
            return await _PostResponse(
                post_link='../chat/room/create/',
                data={
                    'characters': characters,
                    'name': name,
                    'topic': topic,
                    'visibility': 'PRIVATE',
                    **kwargs
                },
                wait=wait, token=token
            )

        async def rate(
            self, rate: int, history_id: str,
            message_id: str, *, wait: bool = False,
            token: str = None, **kwargs
        ):
            if rate == 0: label = [234, 238, 241, 244] #Terrible
            elif rate == 1: label = [235, 237, 241, 244] #Bad
            elif rate == 2: label = [235, 238, 240, 244] #Good
            elif rate == 3: label = [235, 238, 241, 243] #Fantastic
            else: raise errors.LabelError('Wrong Rate Value')

            return await _PostResponse(
                post_link='chat/annotations/label/',
                data={
                    'label_ids': label,
                    'history_external_id': history_id,
                    'message_uuid': message_id,
                    **kwargs
                },
                wait=wait, send_json=False,
                token=token, method='PUT'
            )

        async def next_message(
            self, history_id: str, parent_msg_uuid: str,
            tgt: str, *, wait: bool = False,
            token: str = None, **kwargs
        ):
            response = await _PostResponse(
                post_link='chat/streaming/',
                data={
                    "history_external_id": history_id,
                    "parent_msg_uuid": parent_msg_uuid,
                    "tgt": tgt,
                    **kwargs
                },
                wait=wait, send_json=False, token=token
            )

            if response.split('\n')[-2].startswith('{"abort"'):
                raise errors.FilterError('No eligible candidates')
            else:
                return json.loads(response.split('\n')[-2])

        async def get_histories(
            self, char: str, *,
            number: int = 50,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/character/histories_v2/',
                data={"external_id": char, "number": number},
                wait=wait, token=token
            )

        async def get_history(
            self, history_id: str = None, *,
            wait: bool = False, token: str = None
        ):
            return await _GetResponse(
                f'chat/history/msgs/user/?history_external_id={history_id}',
                wait=wait, token=token
            )

        async def get_chat(
            self, char: str = None, *,
            wait: bool = False, token: str = None,
            **kwargs
        ):
            return await _PostResponse(
                post_link='chat/history/continue/',
                data={
                    'character_external_id': char,
                    **kwargs
                },
                wait=wait, token=token
            )

        async def send_message(
            self, history_id: str, tgt: str, text: str, *,
            wait: bool = False, token: str = None,
            **kwargs
        ):
            response = await _PostResponse(
                post_link='chat/streaming/',
                data={
                    'history_external_id': history_id,
                    'tgt': tgt,
                    'text': text,
                    **kwargs
                },
                wait=wait, send_json=False, token=token
            )

            if response.split('\n')[-2].startswith('{"abort"'):
                raise errors.FilterError('No eligible candidates')
            else:
                return json.loads(response.split('\n')[-2])

        async def delete_message(
            self, history_id: str, uuids_to_delete: list,
            *, wait: bool = False, token: str = None, **kwargs
        ):
            return await _PostResponse(
                post_link='chat/history/msgs/delete/',
                data={
                    'history_id': history_id,
                    'uuids_to_delete': uuids_to_delete,
                    **kwargs
                },
                wait=wait, token=token
            )

        async def new_chat(
            self, char: str, *,
            wait: bool = False, token: str = None
        ):
            return await _PostResponse(
                post_link='chat/history/create/',
                data={'character_external_id': char},
                wait=wait, token=token
            )