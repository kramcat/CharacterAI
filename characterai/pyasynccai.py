from typing import Dict
import asyncio
import json
import time

from playwright.async_api import async_playwright

from characterai import errors

__all__ = ['pyCAI', 'pyAsyncCAI']

text = []
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
    await goto(f'https://beta.character.ai/{link}/')
    data = json.loads(await (page.locator('pre').inner_text()))

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
        self.context = await self.browser.new_context(extra_http_headers={"Authorization": f"Token {self.token}"})
        page = await self.context.new_page()

    class user:
        """
        Just a Responses from site for user info

        user.info()
        """
        async def info(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/user', wait=wait, token=token)

        async def posts(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/posts/user/?scope=user&page=1&posts_to_load=5', wait=wait, token=token)

        async def followers(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/user/followers', wait=wait, token=token)

        async def following(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/user/following', wait=wait, token=token)

    class character:
        """
        Just a Responses from site for characters

        character.trending()
        character.get_info('CHAR')
        """
        async def trending(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/characters/trending', wait=wait, token=token)

        async def recommended(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/characters/recommended', wait=wait, token=token)

        async def categories(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return await GetResponse(link='chat/character/categories', wait=wait, token=token)

        async def get_info(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            try:
                return GetResponse(link=f'chat/character/info-cached/{char}', wait=wait, token=token)
            except:
                raise errors.CharNotFound('Wrong Char')

    class chat:
        async def send_message(self, char: str, message: str, *, wait: bool = False, token: str = None) -> bool:
            """
            Sending a message

            chat.send_message('CHAR', 'MESSAGE')
            """
            await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

            # time.sleep because the code is running too fast and there are problems with sending the message
            time.sleep(1)
            await page.get_by_placeholder("Type a message").fill(message)
            time.sleep(1)
            await page.get_by_role("button", name="Submit Message").click()

            await (await page.wait_for_selector('.swiper-button-next', timeout=0)).is_visible()
            div = await page.query_selector('div.markdown-wrapper.markdown-wrapper-last-msg.swiper-no-swiping')

            return (await div.inner_text())

        async def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> None:
            """
            Starting new chat, return True when done

            chat.new_chat('CHAR')
            """
            await goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            await (await page.wait_for_selector('.col-auto.px-2.dropdown')).click()
            await page.locator('//html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/div/div/div/div/button[2]').click()