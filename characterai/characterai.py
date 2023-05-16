from typing import Dict
import json

from playwright.sync_api import sync_playwright

from characterai import errors
from characterai.pyasynccai import pyAsyncCAI

__all__ = ['pyCAI', 'pyAsyncCAI']

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
    data = json.loads(page.locator('body').inner_text())

    return data


class pyCAI:
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

        def recent(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse('chat/characters/recent/', wait=wait, token=token)

    class character:
        """
        Just a Responses from site for characters

        character.trending()
        character.info('CHAR')
        character.search('SEARCH')
        """
        def trending(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/characters/trending', wait=wait, token=token)

        def recommended(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/characters/recommended', wait=wait, token=token)

        def categories(self, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(link='chat/character/categories', wait=wait, token=token)

        def info(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            data = GetResponse(f'chat/character/info-cached/{char}/', wait=wait, token=token)

            if data != "{'error': 'Server Error (500)'}":
                return data
            else:
                raise errors.CharNotFound('Wrong Char')
        
        def search(self, search, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(f'chat/characters/search/?query={search}', wait=wait, token=token)

    class chat:
        def get_history(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Getting character chat history, return json response

            chat.get_history('CHAR')
            """
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            
            if page.query_selector('h1') == None:
                with page.expect_response(lambda response: response.url.startswith('https://beta.character.ai/chat/history/msgs/user/')) as response_info:
                    goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

                response = response_info.value.text()
                return json.loads(response)
            else:
                raise errors.CharNotFound('Wrong Char')

        def send_message(self, char: str, message: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Sending a message, return json

            chat.send_message('CHAR', 'MESSAGE')
            """
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)
            
            # BIG THANKS - HearYourWaifu
            page.evaluate("""
            const { fetch: origFetch } = window;
            window.fetch = async (...args) => {
            const response = await origFetch(...args);
            const raw_text = await new Response(response.clone().body).text();
            return response;};""")
            
            with page.expect_response("https://beta.character.ai/chat/streaming/") as response_info:
                page.get_by_placeholder("Type a message").fill(message)
                page.get_by_role("button", name="Submit Message").click()

            response = response_info.value.text()
            return json.loads('{"replies": ' + response.split(r'{"replies": ')[-1])

        def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> None:
            """
            Starting new chat, return json

            chat.new_chat('CHAR')
            """
            goto(f'https://beta.character.ai/chat?char={char}', wait=wait, token=token)

            with page.expect_response("https://beta.character.ai/chat/history/create/") as response_info:
                page.wait_for_selector('.col-auto.px-2.dropdown').click()
                page.wait_for_selector('"Save and Start New Chat"').click()

            response = response_info.value.text()
            return json.loads(response)