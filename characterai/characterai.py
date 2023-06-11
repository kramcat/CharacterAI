import json

from playwright.sync_api import sync_playwright

from characterai import errors
from characterai.pyasynccai import PyAsyncCAI

__all__ = ['PyCAI', 'PyAsyncCAI']

def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        page.set_extra_http_headers(
            {"Authorization": f"Token {token}"}
        )

    page.goto(f'https://beta.character.ai/{link}')

    content = (page.locator('body').inner_text())

    if content.startswith('Not Found'):
        raise errors.NotFoundError(content.split('\n')[-1])
    elif content == 'No history found for id provided.':
        raise errors.NotFoundError(content)
    elif content.startswith('{"error":'):
        raise errors.ServerError(json.loads(content)['error']) 
    elif content.startswith('{"detail":'):
        raise errors.AuthError(json.loads(content)['detail']) 

    if page.title() != 'Waiting Room powered by Cloudflare':
        return page
    else:
        if wait:
            page.wait_for_selector(
                'div#wrapper', state='detached', timeout=0
            )
            goto(link=link, wait=wait, token=token)
        else:
            raise errors.NoResponse('The Site is Overloaded')

def GetResponse(
        link: str, *, wait: bool = False,
        token: str = None
    ):
    goto(link, wait=wait, token=token)
    return json.loads(page.locator('body').inner_text())

def PostResponse(
        link: str, post_link: str, data: str, *,
        headers: str = None, return_json: bool = True,
        wait: bool = False, token: str = None,
        method: str = 'POST'
    ):
    post_link = f'https://beta.character.ai/{post_link}'

    goto(link, wait=wait, token=token)

    if headers == None:
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

    with page.expect_response(post_link) as response_info:
        page.evaluate(
            """const {fetch: origFetch} = window;
            window.fetch = async (...args) => {
            const response = await origFetch(...args);
            const raw_text = await new Response(response.clone().body).text();
            return response;};"""
            + "fetch('"
            + post_link + "', {method: '"
            + method + "',body: JSON.stringify("
            + str(data) + "),headers: new Headers("
            + str(headers) + "),})"
        )

    response = response_info.value

    if response.status != 200:
        raise errors.ServerError(response.status_text) 

    if return_json:
        return response.json()
    else:
        return response.text()

class PyCAI:
    def __init__(self, token: str, *, headless: bool = True):
        global page

        self.token = token
        self.headless = headless

        self.browser = sync_playwright().start().firefox.launch(headless=headless)
        self.context = self.browser.new_context(
            extra_http_headers={"Authorization": f"Token {self.token}"}
        )
        page = self.context.new_page()

        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    class user:
        """Just a Responses from site for user info

        user.info()
        user.posts()
        user.followers()
        user.following()
        user.recent()
        
        """
        def info(
            self, username: str = None, *,
            wait: bool = False, token: str = None
        ):
            if username == None:
                return GetResponse('chat/user/', wait=wait, token=token)
            else:
                return PostResponse(
                    link=f'public-profile/?username={username}',
                    post_link='chat/user/public/',
                    data={'username': username},
                    wait=wait, token=token
                )

        def posts(
            self, username: str = None, *,
            wait: bool = False, token: str = None, page_: int=1, posts_to_load:int=5
        ):
            if username == None:
                return GetResponse(
                    f'chat/posts/user/?scope=user&page={page_}&posts_to_load={posts_to_load}/',
                    wait=wait, token=token
                )
            else:
                return GetResponse(
                    f'chat/posts/user/?username={username}&page={page_}&posts_to_load={posts_to_load}/',
                    wait=wait, token=token
                )

        def followers(self, *, wait: bool = False, token: str = None):
            return GetResponse(
                'chat/user/followers/',
                wait=wait, token=token
            )

        def following(self, *, wait: bool = False, token: str = None):
            return GetResponse(
                'chat/user/following/',
                wait=wait, token=token
            )
        
        def recent(self, *, wait: bool = False, token: str = None):
            return GetResponse(
                'chat/characters/recent/',
                wait=wait, token=token
            )

    class character:
        """Just a Responses from site for characters

        character.trending()
        character.recommended()
        character.categories()
        character.info('CHAR')
        character.search('SEARCH')
        
        """
        def trending(
            self, *, wait: bool = False,
            token: str = None
        ):
            return GetResponse(
                'chat/characters/trending/', 
                wait=wait, token=token
            )

        def recommended(
            self, *, wait: bool = False,
            token: str = None
        ):
            return GetResponse(
                'chat/characters/recommended/', 
                wait=wait, token=token
            )

        def categories(
            self, *, wait: bool = False,
            token: str = None
        ):
            return GetResponse(
                'chat/character/categories/', 
                wait=wait, token=token
            )

        def info(
            self, char: str, *, 
            wait: bool = False, token: str = None
        ):
            return GetResponse(
                f'chat/character/info-cached/{char}/', 
                wait=wait, token=token
            )

        def search(
            self, query: str, *,
            wait: bool = False, token: str = None
        ):
            return GetResponse(
                f'chat/characters/search/?query={query}/', 
                wait=wait, token=token
            )

    class chat:
        def rate(
            self, char: str, rate: int, *,
            history_external_id: str = None,
            wait: bool = False, token: str = None
        ):
            """Rate message, return json

            chat.rate('CHAR', NUM)
            
            """
            with page.expect_response(
                lambda response: response.url.startswith(
                    'https://beta.character.ai/chat/history/msgs/user/'
                )
            ) as response_info:
                goto(f'chat?char={char}', wait=wait, token=token)

            if rate == 0: label = [234, 238, 241, 244] #Terrible
            elif rate == 1: label = [235, 237, 241, 244] #Bad
            elif rate == 2: label = [235, 238, 240, 244] #Good
            elif rate == 3: label = [235, 238, 241, 243] #Fantastic
            else: raise errors.LabelError('Wrong Rate Value')

            history_data = response_info.value

            history = history_data.json()
            history_external_id = history_data.url.split('=')[-1]

            response = PostResponse(
                link=f'chat?char={char}',
                post_link='chat/annotations/label/',
                data={
                    "message_uuid": history['messages'][-1]['uuid'],
                    "history_external_id": history_external_id,
                    "label_ids": label
                },
                wait=wait, return_json=False, token=token, method='PUT'
            )

            return response

        def next_message(
            self, char: str, *, wait: bool = False,
            token: str = None, filtering: bool = True
        ):
            """Next message, return json

            chat.next_message('CHAR', 'MESSAGE')
            
            """
            with page.expect_response(
                lambda response: response.url.startswith(
                    'https://beta.character.ai/chat/history/msgs/user/'
                )
            ) as response_info:
                goto(f'chat?char={char}', wait=wait, token=token)
            
            history = response_info.value.json()
            url = response_info.value.url

            #Get last user message for uuid and text
            for h in history['messages']:
                if h['src__is_human'] == True:
                    last_message = h

            response = PostResponse(
                link=f'chat?char={char}',
                post_link='chat/streaming/',
                data={
                    "character_external_id": char,
                    "history_external_id": url.split('=')[-1],
                    "text": last_message['text'],
                    "tgt": history['messages'][-1]['src__user__username'],
                    "parent_msg_uuid": last_message['uuid']
                },
                wait=wait, return_json=False, token=token
            )

            if response.split('\n')[-1].startswith('{"abort"'):
                if filtering:
                    raise errors.FilterError('No eligible candidates')
                else:
                    return json.loads(response.split('\n')[-3])
            else:
                return json.loads(response.split('\n')[-2])

        def get_histories(
            self, char: str, *,
            wait: bool = False, token: str = None, number:int=50
        ):
            """Getting all character chat histories

            chat.get_histories('CHAR')
            
            """
            return PostResponse(
                link=f'chat?char={char}',
                post_link='chat/character/histories/',
                data={"external_id": char, "number": number},
                wait=wait,
                token=token
            )

        def get_history(
            self, char: str = None, *,
            wait: bool = False, token: str = None, page_: int=1000000
        ):
            """Getting character chat history

            chat.get_history('HISTORY_EXTERNAL_ID')
            Also page works like this: 1000000 -> 999999 -> 999998
            
            """
            try:
                return GetResponse(
                    f'chat/history/msgs/user/?history_external_id={char}&page_num={page_}',
                    wait=wait, token=token
                )
            except errors.PyCAIError:
                char_data = PostResponse(
                    link=f'chat?char={char}',
                    post_link='chat/history/continue/',
                    data={"character_external_id": char},
                    wait=wait,
                    token=token
                )

                history_id = char_data['external_id']

                return GetResponse(
                    f'chat/history/msgs/user/?history_external_id={history_id}&page_num={page_}',
                    wait=wait, token=token
                )

        def get_chat(
            self, char: str = None, *,
            wait: bool = False, token: str = None
        ):
            """Getting the main information about the chat

            chat.get_chat('CHAR')
            
            """
            return PostResponse(
                link=f'chat?char={char}',
                post_link='chat/history/continue/',
                data={"character_external_id": char},
                wait=wait,
                token=token
            )

        def send_message(
            self, char: str, message: str, *,
            history_external_id: str = None,
            tgt: str = None, wait: bool = False,
            token: str = None, filtering: bool = True, primary_message_uuid: str = None
        ):
            """Sending a message, return json, also primary_message_uuid is like when you ran the next_message function (because if you don't specify this the original message will be the reply-to message)

            chat.send_message('CHAR', 'MESSAGE')
            
            """
            # Get history_external_id and tgt
            if history_external_id == None or tgt == None:
                info = PostResponse(
                    link=f'chat?char={char}',
                    post_link='chat/history/continue/',
                    data={'character_external_id': char},
                    wait=wait,
                    token=token
                )

                if history_external_id == None:
                    history_external_id = info['external_id']
                    
                if tgt == None:
                    # In the list of "participants",
                    # a character can be at zero or in the first place
                    if not info['participants'][0]['is_human']:
                        tgt = info['participants'][0]['user']['username']
                    else:
                        tgt = info['participants'][1]['user']['username']
            if not primary_message_uuid:
                response = PostResponse(
                    link=f'chat?char={char}',
                    post_link='chat/streaming/',
                    data={
                        "history_external_id": history_external_id,
                        "character_external_id": char,
                        "text": message,
                        "tgt": tgt
                    },
                    wait=wait,
                    return_json=False,
                    token=token
                )
            else:
                response = PostResponse(
                    link=f'chat?char={char}',
                    post_link='chat/streaming/',
                    data={
                        "history_external_id": history_external_id,
                        "character_external_id": char,
                        "text": message,
                        "tgt": tgt,
                        "primary_msg_uuid": primary_message_uuid,
                        "seen_msg_uuids": [primary_message_uuid]
                    },
                    wait=wait,
                    return_json=False,
                    token=token,
                )
            
            if response.split('\n')[-1].startswith('{"abort"'):
                if filtering:
                    raise errors.FilterError('No eligible candidates')
                else:
                    return json.loads(response.split('\n')[-3])
            else:
                return json.loads(response.split('\n')[-2])

        def delete_message(
            self, history_id: str, uuids_to_delete: list, *,
            wait: bool = False, token: str = None
        ):
            """Delete a message

            chat.new_chat('CHAR')
            
            """
            return PostResponse(
                link='chat',
                post_link='chat/history/msgs/delete/',
                data={
                    "history_id": history_id,
                    "uuids_to_delete": uuids_to_delete
                },
                wait=wait,
                token=token
            )

        def new_chat(
            self, char: str, *,
            wait: bool = False, token: str = None
        ):
            """Starting new chat, return new chat history

            chat.new_chat('CHAR')
            
            """
            return PostResponse(
                link=f'chat?char={char}',
                post_link='chat/history/create/',
                data={'character_external_id': char},
                wait=wait,
                token=token
            )
