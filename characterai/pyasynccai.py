import asyncio
import json

from playwright.async_api import async_playwright

from characterai import errors

__all__ = ['PyCAI', 'PyAsyncCAI']

async def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        await page.set_extra_http_headers(
            {"Authorization": f"Token {token}"}
        )

    await page.goto(f'https://beta.character.ai/{link}')

    content = await (page.locator('body').inner_text())

    if content.startswith('Not Found'):
        raise errors.NotFoundError(content.split('\n')[-1])
    elif content == 'No history found for id provided.':
        raise errors.NotFoundError(content)
    elif content.startswith('{"error":'):
        raise errors.ServerError(json.loads(content)['error']) 
    elif content.startswith('{"detail":'):
        raise errors.AuthError(json.loads(content)['detail']) 

    if await page.title() != 'Waiting Room powered by Cloudflare':
        return page
    else:
        if wait:
            await page.wait_for_selector(
                'div#wrapper', state='detached', timeout=0
            )
            await goto(link=link, wait=wait)
        else:
            raise errors.NoResponse('The Site is Overloaded')

async def GetResponse(
        link: str, *, wait: bool = False,
        token: str = None
    ):
    await goto(link, wait=wait, token=token)
    data = json.loads(await (page.locator('body').inner_text()))

    return data

async def PostResponse(
        link: str, post_link: str, data: str, *,
        headers: str = None, json: bool = True,
        wait: bool = False, token: str = None,
        method: str = 'POST'
    ):
    post_link = f'https://beta.character.ai/{post_link}'

    await goto(link, wait=wait, token=token)

    if headers == None:
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }

    async with page.expect_response(post_link) as response_info:
        await page.evaluate(
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

    response = await response_info.value

    if response.status != 200:
        raise errors.ServerError(response.status_text) 

    if json:
        return await response.json()
    else:
        return await response.text()

class PyAsyncCAI:
    def __init__(self, token: str = None):
        self.token = token

        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    async def start(self, *, headless: bool = True):
        global page

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(headless=headless)
        self.context = await self.browser.new_context(
            extra_http_headers={"Authorization": f"Token {self.token}"}
        )
        page = await self.context.new_page()

    class user:
        """Just a Responses from site for user info

        user.info()
        user.posts()
        user.followers()
        user.following()
        user.recent()
        
        """
        async def info(
            self, username: str = None, *,
            wait: bool = False, token: str = None
        ):
            if username == None:
                return await GetResponse('chat/user/', wait=wait, token=token)
            else:
                return await PostResponse(
                    link=f'public-profile/?username={username}',
                    post_link='chat/user/public/',
                    data={'username': username},
                    wait=wait, token=token
                )

        async def posts(
            self, username: str = None, *, 
            wait: bool = False, token: str = None
        ):
            if username == None:
                return await GetResponse(
                    'chat/posts/user/?scope=user&page=1&posts_to_load=5/',
                    wait=wait, token=token
                )
            else:
                return await GetResponse(
                    f'chat/posts/user/?username={username}&page=1&posts_to_load=5/',
                    wait=wait, token=token
                )

        async def followers(self, *, wait: bool = False, token: str = None):
            return await GetResponse(
                'chat/user/followers/',
                wait=wait, token=token
            )

        async def following(self, *, wait: bool = False, token: str = None):
            return await GetResponse(
                'chat/user/following/',
                wait=wait, token=token
            )
        
        async def recent(self, *, wait: bool = False, token: str = None):
            return await GetResponse(
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
        async def trending(
            self, *, wait: bool = False,
            token: str = None
        ):
            return await GetResponse(
                'chat/characters/trending/', 
                wait=wait, token=token
            )

        async def recommended(
            self, *, wait: bool = False,
            token: str = None
        ):
            return await GetResponse(
                'chat/characters/recommended/', 
                wait=wait, token=token
            )

        async def categories(
            self, *, wait: bool = False,
            token: str = None
        ):
            return await GetResponse(
                'chat/character/categories/', 
                wait=wait, token=token
            )

        async def info(
            self, char: str, *, 
            wait: bool = False, token: str = None
        ):
            return await GetResponse(
                f'chat/character/info-cached/{char}/', 
                wait=wait, token=token
            )

        async def search(
            self, query: str, *,
            wait: bool = False, token: str = None
        ):
            return await GetResponse(
                f'chat/characters/search/?query={query}/', 
                wait=wait, token=token
            )

    class chat:
        async def rate(
            self, char: str, rate: int, *,
            message_uuid: str = None,
            wait: bool = False, token: str = None
        ):
            """Rate message, return json

            chat.rate('CHAR', NUM)
            
            """
            async with page.expect_response(
                lambda response: response.url.startswith(
                    'https://beta.character.ai/chat/history/msgs/user/'
                )
            ) as response_info:
                await goto(f'chat?char={char}', wait=wait, token=token)

            if rate == 0: label = [234, 238, 241, 244] #Terrible
            elif rate == 1: label = [235, 237, 241, 244] #Bad
            elif rate == 2: label = [235, 238, 240, 244] #Good
            elif rate == 3: label = [235, 238, 241, 243] #Fantastic
            else: raise errors.LabelError('Wrong Rate Value')

            history_data = await response_info.value

            history = await history_data.json()
            history_external_id = history_data.url.split('=')[-1]

            response = await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/annotations/label/',
                data={
                    "message_uuid": history['messages'][-1]['uuid'],
                    "history_external_id": history_external_id,
                    "label_ids": label
                },
                wait=wait, json=False, token=token, method='PUT'
            )

            return response

        async def next_message(
            self, char: str, *, wait: bool = False,
            token: str = None, filtering: bool = True
        ):
            """Next message, return json

            chat.next_message('CHAR', 'MESSAGE')
            
            # """
            # await goto(f'chat?char={char}', wait=wait, token=token)

            async with page.expect_response(
                lambda response: response.url.startswith(
                    'https://beta.character.ai/chat/history/msgs/user/'
                )
            ) as response_info:
                await goto(f'chat?char={char}', wait=wait, token=token)
            
            history = await (await response_info.value).json()
            url = (await response_info.value).url

            #Get last user message for uuid and text
            for h in history['messages']:
                if h['src__is_human'] == True:
                    last_message = h

            response = await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/streaming/',
                data={
                    "character_external_id": char,
                    "history_external_id": url.split('=')[-1],
                    "text": last_message['text'],
                    "tgt": history['messages'][-1]['src__user__username'],
                    "parent_msg_uuid": last_message['uuid']
                },
                wait=wait, json=False, token=token
            )

            if response.split('\n')[-1].startswith('{"abort"'):
                if filtering:
                    raise errors.FilterError('No eligible candidates')
                else:
                    return json.loads(response.split('\n')[-3])
            else:
                return json.loads(response.split('\n')[-2])

        async def get_histories(
            self, char: str, *,
            wait: bool = False, token: str = None
        ):
            """Getting all character chat histories

            chat.get_histories('CHAR')
            
            """
            return await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/character/histories/',
                data={"external_id": char, "number": 50},
                wait=wait,
                token=token
            )

        async def get_history(
            self, char: str = None, *,
            wait: bool = False, token: str = None
        ):
            """Getting character chat history

            chat.get_history('HISTORY_EXTERNAL_ID')
            
            """
            try:
                return await GetResponse(
                    f'chat/history/msgs/user/?history_external_id={char}',
                    wait=wait, token=token
                )
            except:
                char_data = await PostResponse(
                    link=f'chat?char={char}',
                    post_link='chat/history/continue/',
                    data={"character_external_id": char},
                    wait=wait,
                    token=token
                )

                history_id = char_data['external_id']

                return await GetResponse(
                    f'chat/history/msgs/user/?history_external_id={history_id}',
                    wait=wait, token=token
                )

        async def get_chat(
            self, char: str = None, *,
            wait: bool = False, token: str = None
        ):
            """Getting the main information about the chat

            chat.get_chat('CHAR')
            
            """
            return await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/history/continue/',
                data={"character_external_id": char},
                wait=wait,
                token=token
            )

        async def send_message(
            self, char: str, message: str, *,
            history_external_id: str = None,
            tgt: str = None, wait: bool = False,
            token: str = None, filtering: bool = True
        ):
            """Sending a message, return json

            chat.send_message('CHAR', 'MESSAGE')
            
            """
            # Get history_external_id and tgt
            if history_external_id == None or tgt == None:
                print('none')
                info = await PostResponse(
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

            response = await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/streaming/',
                data={
                    "history_external_id": history_external_id,
                    "character_external_id": char,
                    "text": message,
                    "tgt": tgt
                },
                wait=wait,
                json=False,
                token=token
            )
            
            if response.split('\n')[-1].startswith('{"abort"'):
                if filtering:
                    raise errors.FilterError('No eligible candidates')
                else:
                    return json.loads(response.split('\n')[-3])
            else:
                return json.loads(response.split('\n')[-2])

        async def delete_message(
            self, history_id: str, uuids_to_delete: list, *,
            wait: bool = False, token: str = None
        ):
            """Delete a message

            chat.new_chat('HISTORY_ID')
            
            """
            return await PostResponse(
                link='chat',
                post_link='chat/history/msgs/delete/',
                data={
                    "history_id": history_id,
                    "uuids_to_delete": uuids_to_delete
                },
                wait=wait,
                token=token
            )

        async def new_chat(
            self, char: str, *,
            wait: bool = False, token: str = None
        ):
            """Starting new chat, return new chat history

            chat.new_chat('CHAR')
            
            """
            return await PostResponse(
                link=f'chat?char={char}',
                post_link='chat/history/create/',
                data={'character_external_id': char},
                wait=wait,
                token=token
            )
