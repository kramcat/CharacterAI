from typing import Dict
import asyncio
import json

from playwright.async_api import async_playwright

from characterai import errors

__all__ = ['pyCAI', 'pyAsyncCAI']

page = None

async def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        await page.set_extra_http_headers({"Authorization": f"Token {token}"})

    await page.goto(link)

    if await page.title() != 'Waiting Room powered by Cloudflare':
        if await page.get_by_role("button", name="Accept").is_visible():
            await page.get_by_role("button", name="Accept").click()

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


class pyAsyncCAI:
    def __init__(self, token: str):
        self.token = token

        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    async def start(self, *, headless: bool = True):
        global page

        self.browser = await (await async_playwright().start()).firefox.launch(headless=headless)
        self.context = await self.browser.new_context(
            extra_http_headers={"Authorization": f"Token {self.token}"}
        )
        page = await self.context.new_page()

    class user:
        """
        Just a Responses from site for user info

        user.info()
        """
        async def info(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse('chat/user', wait=wait, token=token)

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
            data = await GetResponse(f'chat/character/info-cached/{char}/', wait=wait, token=token)

            if data != "{'error': 'Server Error (500)'}":
                return data
            else:
                raise errors.CharNotFound('Wrong Char')
        
        async def search(self, search, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(f'chat/characters/search/?query={search}', wait=wait, token=token)
            
    class chat:
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

        async def send_message(self, char: str, message: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Sending a message, return json

            chat.send_message('CHAR', 'MESSAGE')
            """
            await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            
            # BIG THANKS - HearYourWaifu
            await page.evaluate("""
            const { fetch: origFetch } = window;
            window.fetch = async (...args) => {
            const response = await origFetch(...args);
            const raw_text = await new Response(response.clone().body).text();
            return response;};""")
            
            async with page.expect_response("https://beta.character.ai/chat/streaming/") as response_info:
                await page.get_by_placeholder("Type a message").fill(message)
                await page.get_by_role("button", name="Submit Message").click()

            response = await (await response_info.value).text()
            return json.loads('{"replies": ' + response.split(r'{"replies": ')[-1])

        async def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Starting new chat, return json

            chat.new_chat('CHAR')
            """
            await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

            async with page.expect_response("https://beta.character.ai/chat/history/create/") as response_info:
                await (await page.wait_for_selector('.col-auto.px-2.dropdown')).click()
                await (await page.wait_for_selector('"Save and Start New Chat"')).click()

            response = await (await response_info.value).text()
            return json.loads(response)