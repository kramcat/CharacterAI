from typing import Dict
import json
import time

from playwright.sync_api import sync_playwright

from characterai import errors
from characterai.pyasynccai import pyAsyncCAI

__all__ = ['pyCAI', 'pyAsyncCAI']

text = []
page = None

def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        page.set_extra_http_headers({"Authorization": f"Token {token}"})

    page.goto(link)

    if page.title() != 'Waiting Room powered by Cloudflare':
        if page.get_by_role("button", name="Accept").is_visible():
            page.get_by_role("button", name="Accept").click()

            return page

    else:
        if wait:
            page.wait_for_selector('div#wrapper', state='detached', timeout=0)
            goto(link=link, wait=wait)
        else:
            raise errors.NoResponse('The Site is Overloaded')

def GetResponse(link: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
    goto(f'https://beta.character.ai/{link}/', wait=wait, token=token)
    data = json.loads(page.locator('pre').inner_text())

    return data


class pyCAI:
    def __init__(self, token: str, *, headless: bool = True):
        global page

        self.token = token
        self.headless = headless

        self.browser = sync_playwright().start().firefox.launch(headless=headless)
        self.context = self.browser.new_context(
            extra_http_headers={"Authorization": f"Token {self.token}"})
        page = self.context.new_page()

        self.user = self.user()
        self.character = self.character()
        self.chat = self.chat()

    class user:
        """
        Just a Responses from site for user info

        user.info()
        """

        def info(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/user', wait=wait, token=token)

        def posts(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/posts/user/?scope=user&page=1&posts_to_load=5', wait=wait, token=token)

        def followers(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/user/followers', wait=wait, token=token)

        def following(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/user/following', wait=wait, token=token)

    class character:
        """
        Just a Responses from site for characters

        character.trending()
        character.get_info('CHAR')
        """

        def trending(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/characters/trending', wait=wait, token=token)

        def recommended(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/characters/recommended', wait=wait, token=token)

        def categories(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/character/categories', wait=wait, token=token)

        def get_info(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            try:
                return GetResponse(link=f'chat/character/info-cached/{char}', wait=wait, token=token)
            except:
                raise errors.CharNotFound('Wrong Char')

    class chat:
        def get_history(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Getting character chat history, return json Response

            The post method doesn't work, so i get this from page.on('Response')

            chat.get_history('CHAR')
            """
            page.on("response", lambda response: text.append(response.text()) if response.url.startswith(
                'https://beta.character.ai/chat/history/msgs/user/') else None)
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            page.wait_for_selector('.msg.char-msg').is_visible()

            return json.loads(text[0])

        def send_message(self, char: str, message: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Sending a message

            chat.send_message('CHAR', 'MESSAGE')
            """
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

            # time.sleep because the code is running too fast and there are problems with sending the message
            time.sleep(1)
            page.wait_for_selector("textarea", state="visible").fill(message)
            time.sleep(1)
            page.get_by_role("button", name="Submit Message").click()

            page.wait_for_selector('.swiper-button-next',
                                   timeout=0).is_visible()
            div = page.query_selector(
                'div.markdown-wrapper.markdown-wrapper-last-msg.swiper-no-swiping')

            return div.inner_text()

        def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> None:
            """
            Starting new chat

            chat.new_chat('CHAR')
            """
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            page.wait_for_selector('.col-auto.px-2.dropdown').click()
            page.locator('//html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/div[3]/div/div/div/div/div/button[2]').click()
