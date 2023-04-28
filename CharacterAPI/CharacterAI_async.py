from typing import Dict
import asyncio
import json
import time

from playwright.async_api import async_playwright

from errors import *

__all__ = ['pyCAI']

text = []
page = None

class pyCAI:
    def __init__(self, token):
        self.token = token
        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    async def init(self):
        global page

        self.browser = await (await async_playwright().start()).firefox.launch(headless=True)
        self.context = await self.browser.new_context(extra_http_headers={"Authorization": f"Token {self.token}"})
        page = await self.context.new_page()

    # [FOR LIBRARY] Convert site to json
    async def GetResponce(link: str) -> Dict[str, str]:
        await pyCAI.goto(f'https://beta.character.ai/{link}/')
        data = json.loads(await (page.locator('pre').inner_text()))
        
        return data

    # [FOR LIBRARY] Checking the page if it runs for the first time
    async def goto(link: str):
        await page.goto(link)

        if await page.title() != 'Waiting Room powered by Cloudflare':
            if await page.get_by_role("button", name="Accept").is_visible():
                await page.get_by_role("button", name="Accept").click()
                
                return page
        
        else: raise errors.NoResponse('The Site is Overloaded')

    class user:
        """
        Just a responces from site for user info

        user.info()
        """
        async def info(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/user')

        async def posts(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/posts/user/?scope=user&page=1&posts_to_load=5')

        async def followers(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/user/followers')

        async def following(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/user/following')

    class character:
        """
        Just a responces from site for characters

        character.trending()
        character.get_info('CHAR')
        """
        async def trending(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/characters/trending')
        
        async def recommended(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/characters/recommended')

        async def categories(self) -> Dict[str, str]:
            return await pyCAI.GetResponce(link='chat/character/categories')

        async def get_info(self, char: str) -> Dict[str, str]:
            try: return pyCAI.GetResponce(link=f'chat/character/info-cached/{char}')
            except: raise errors.CharNotFound('Wrong Char')

    class chat:
        async def get_history(self, char: str) -> str:
            """
            Getting character chat history, return json responce

            The post method doesn't work, so i get this from page.on('responce')

            chat.get_history('CHAR')
            """
            await page.on("response", lambda response: text.append(response.text()) if response.url.startswith('https://beta.character.ai/chat/history/msgs/user/') else None)
            await pyCAI.goto(f'https://beta.character.ai/chat?char={char}')
            await (await page.wait_for_selector('.msg.char-msg')).is_visible()
            
            return json.loads(text[0])

        async def send_message(self, char: str, message: str) -> bool:
            """
            Sending a message

            chat.send_message('CHAR', 'MESSAGE')
            """
            await pyCAI.goto(f'https://beta.character.ai/chat?char={char}')

            # Time.sleep() because the actions are happening too fast
            time.sleep(1)
            await page.get_by_placeholder("Type a message").fill(message)
            time.sleep(1)
            await page.get_by_role("button", name="Submit Message").click()
            time.sleep(1)

            await (await page.wait_for_selector('.swiper-button-next', timeout=0)).is_visible()
            div = await page.query_selector('div.markdown-wrapper.markdown-wrapper-last-msg.swiper-no-swiping')

            return (await div.inner_text()).replace('\n\n\n\n\n', '\n\n')

        async def new_chat(self, *, char: str) -> bool:
            """
            Starting new chat, return True when done

            chat.new_chat('CHAR')
            """
            await pyCAI.goto(f'https://beta.character.ai/chat?char={char}')
            await page.wait_for_selector('div.col-auto.px-2.dropdown').click()
            await page.locator('"Save and Start New Chat"').click()

            return True