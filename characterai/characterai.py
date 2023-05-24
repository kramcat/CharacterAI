from typing import Dict
import json

from playwright.sync_api import sync_playwright

from characterai import errors
from characterai.pyasynccai import pyAsyncCAI

__all__ = ['pyCAI', 'pyAsyncCAI']

def goto(link: str, *, wait: bool = False, token: str = None):
    if token != None:
        page.set_extra_http_headers({"Authorization": f"Token {token}"})

    page.goto(link)

    if page.title() != 'Waiting Room powered by Cloudflare':
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

def PostResponse(link: str, post_link: str, data: str, headers: str, *, json: bool = True, wait: bool = False) -> Dict[str, str]:
    goto(link, wait=wait)

    with page.expect_response(post_link) as response_info:
        # From HearYourWaifu
        page.evaluate("const {fetch: origFetch} = window;window.fetch = async (...args) => {const response = await origFetch(...args);const raw_text = await new Response(response.clone().body).text();return response;};")
        
        page.evaluate("fetch('" + post_link + "', {method: 'POST',body: JSON.stringify(" + str(data) + "),headers: new Headers(" + str(headers) + "),})")

    if json:
        return response_info.value.json()
    else:
        return response_info.value.text()


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
        user.posts()
        user.followers()
        user.following()
        user.recent()
        """
        def info(self, username: str = None, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            if username == None:
                return GetResponse('chat/user', wait=wait, token=token)
            else:
                return PostResponse(
                    link=f'https://beta.character.ai/public-profile/?username={username}',
                    post_link='https://beta.character.ai/chat/user/public/',
                    data={'username': username},
                    headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                    wait=wait
                )

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
        character.recommended()
        character.categories()
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
            return GetResponse(f'chat/character/info-cached/{char}/', wait=wait, token=token)
        
        def search(self, search, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            return GetResponse(f'chat/characters/search/?query={search}', wait=wait, token=token)

    class chat:
        def get_histories(self, char: str, *, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Getting all character chat histories, return json response

            chat.get_histories('CHAR')
            """
            return PostResponse(
                link=f'https://beta.character.ai/chat?char={char}',
                post_link='https://beta.character.ai/chat/character/histories/',
                data={
                    "external_id": char,
                    "number": 50,
                },
                headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                wait=wait
            )

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

        def send_message(self, char: str, message: str, *, history_external_id: str = None, tgt: str = None, wait: bool = False, token: str = None) -> Dict[str, str]:
            """
            Sending a message, return json

            chat.send_message('CHAR', 'MESSAGE')
            """
            # Get history_external_id and tgt
            if history_external_id == None and tgt == None:
                info = PostResponse(
                    link=f'https://beta.character.ai/chat?char={char}',
                    post_link='https://beta.character.ai/chat/history/continue/',
                    data={'character_external_id': char},
                    headers={'Authorization': f'Token {token}','Content-Type': 'application/json'},
                    wait=wait
                )

                history_external_id = info['external_id']
                tgt = info['participants'][1]['user']['username']

            response = PostResponse(
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

        def new_chat(self, char: str, *, wait: bool = False, token: str = None) -> None:
            """
            Starting new chat, return new chat history

            chat.new_chat('CHAR')
            """
            return PostResponse(
                link=f'https://beta.character.ai/chat?char={char}',
                post_link='https://beta.character.ai/chat/history/create/',
                data={'character_external_id': char},
                headers={'Authorization': f'Token {token}', 'Content-Type': 'application/json'},
                wait=wait
            )
