from typing import Dict
import asyncio
import json

from playwright.async_api import async_playwright

from characterai import errors

__all__ = ['pyCAI', 'pyAsyncCAI']

async def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        await page.set_extra_http_headers({"Authorization": f"Token {token}"})

    await page.goto(link)

    if await page.title() != 'Waiting Room powered by Cloudflare':
        return page
    else:
        if wait:
            await page.wait_for_selector('div#wrapper', state='detached', timeout=0)
            await goto(link=link, wait=wait)
        else:
            raise errors.NoResponse('The Site is Overloaded')

async def GetResponse(link: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
    await goto(f'https://beta.character.ai/{link}/', wait=wait, token=token)
    data = json.loads(await (page.locator('body').inner_text()))

    return data

async def PostResponse(link: str, post_link: str, data: str, headers: str, *, json: bool = True, wait: bool = False) -> Dict[str, str]:
    await goto(link, wait=wait)

    async with page.expect_response(post_link) as response_info:
        # From HearYourWaifu
        await page.evaluate("const {fetch: origFetch} = window;window.fetch = async (...args) => {const response = await origFetch(...args);const raw_text = await new Response(response.clone().body).text();return response;};")
        
        await page.evaluate("fetch('" + post_link + "', {method: 'POST',body: JSON.stringify(" + str(data) + "),headers: new Headers(" + str(headers) + "),})")
    
    if json:
        return await (await response_info.value).json()
    else:
        return await (await response_info.value).text()

class pyAsyncCAI:
    def __init__(self, token: str):
        self.token = token

        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    async def start(self, *, headless: bool = True):
        global page

        self.browser = await (await async_playwright().start()).firefox.launch(headless=headless)
        self.context = await self.browser.new_context(extra_http_headers={"Authorization": f"Token {self.token}"})
        page = await self.context.new_page()

    class user:
        """
        Just a Responses from site for user info

        user.info()
        user.posts()
        user.followers()
        user.following()
        user.recent()
        """
        async def info(self, username: str = None, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            if username == None:
                return await GetResponse('chat/user', wait=wait, token=token)
            else:
                return await PostResponse(
                    link=f'https://beta.character.ai/public-profile/?username={username}',
                    post_link='https://beta.character.ai/chat/user/public/',
                    data={'username': username},
                    headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                    wait=wait
                )

        async def posts(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/posts/user/?scope=user&page=1&posts_to_load=5', wait=wait, token=token)

        async def followers(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/user/followers', wait=wait, token=token)

        async def following(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/user/following', wait=wait, token=token)
        
        async def recent(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/characters/recent', wait=wait, token=token)

    class character:
        """
        Just a Responses from site for characters

        character.trending()
        character.recommended()
        character.categories()
        character.info('CHAR')
        character.search('SEARCH')
        """
        async def trending(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/characters/trending', wait=wait, token=token)

        async def recommended(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/characters/recommended', wait=wait, token=token)

        async def categories(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/character/categories', wait=wait, token=token)

        async def info(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(f'chat/character/info-cached/{char}/', wait=wait, token=token)
        
        async def search(self, search, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(f'chat/characters/search/?query={search}', wait=wait, token=token)
            
    class chat:
        async def get_histories(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Getting all character chat histories, return json response

            chat.get_histories('CHAR')
            """
            return await PostResponse(
                link=f'https://beta.character.ai/chat?char={char}',
                post_link='https://beta.character.ai/chat/character/histories/',
                data={
                    "external_id": char,
                    "number": 50,
                },
                headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                wait=wait
            )

        async def get_history(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Getting character chat history, return json response

            chat.get_history('CHAR')
            """
            await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            
            if await page.query_selector('h1') == None:
                async with page.expect_response(lambda response: response.url.startswith('https://beta.character.ai/chat/history/msgs/user/')) as response_info:
                    await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

                response = await (await response_info.value).text()
                return json.loads(response)
            else:
                raise errors.CharNotFound('Wrong Char')

        async def send_message(self, char: str, message: str, *, history_external_id: str = None, tgt: str = None, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Sending a message, return json

            chat.send_message('CHAR', 'MESSAGE')
            """
            # Get history_external_id and tgt
            if history_external_id == None and tgt == None:
                info = await PostResponse(
                    link=f'https://beta.character.ai/chat?char={char}',
                    post_link='https://beta.character.ai/chat/history/continue/',
                    data={'character_external_id': char},
                    headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                    wait=wait
                )

                history_external_id = info['external_id']
                tgt = info['participants'][1]['user']['username']

            response = await PostResponse(
                link=f'https://beta.character.ai/chat?char={char}',
                post_link='https://beta.character.ai/chat/streaming/',
                data={
                    "history_external_id": history_external_id,
                    "character_external_id": char,
                    "text": message,
                    "tgt": tgt
                },
                headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                wait=wait,
                json=False
            )

            try:
                return json.loads('{"replies": ' + str(response.split('{"replies": ')[-1].split('\n')[0]))
            except:
                return response
        
        async def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Starting new chat, return new chat history

            chat.new_chat('CHAR')
            """
            return await PostResponse(
                link=f'https://beta.character.ai/chat?char={char}',
                post_link='https://beta.character.ai/chat/history/create/',
                data={'character_external_id': char},
                headers={'Authorization': f'Token {token}', 'Content-Type': 'application/json'},
                wait=wait
            )
