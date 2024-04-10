from ...types import account, character
from .utils import flatten, caimethod, validate

import uuid

class Account:
    @caimethod
    async def get_me(self, *, token: str = None):
        """Information about your account

        EXAMPLE::

            await client.get_me()

        Returns:
            :obj:`~characterai.types.account.Profile`
        """
        data = await self.request(
            'chat/user/', token=token
        )

        name = data['user']['user']['username']
        
        if name == 'ANONYMOUS':
            return account.Anonymous()
        elif name.startswith('Guest'):
            return account.Guest.model_validate(
                flatten(data)
            )

        return account.Profile.model_validate(
            flatten(data)
        )

    @caimethod
    async def edit_account(
        self, *, token: str = None, **kwargs
    ) -> bool:
        """Change your account information. Returns ``True`` on success.

        EXAMPLE::
        
            await client.edit_account()

        Args:
            username (``str``, *optional*):
                New nickname
            
            name (``str``, *optional*):
                New name
            
            avatar_type (``str``, *optional*):
                The type of the new avatar
            
            avatar_rel_path (``str``, *optional*):
                A new avatar. You need to provide a link to it. Files are uploaded
                via :obj:`~characterai.aiocai.methods.other.Other.upload_image`
            
            bio (``str``, *optional*):
                New description
        
        Returns:
            ``bool``
        """
        user = await self.request(
            'chat/user/', token=token
        )

        info = user['user']
        avatar = info['user']['account']

        settings = {
            'username': info['user']['username'],
            'name': info['name'],
            'avatar_type': avatar['avatar_type'],
            'avatar_rel_path': avatar['avatar_file_name'],
            'bio': info['bio']
        }

        for k in kwargs:
            settings[k] = kwargs[k]

        await self.request(
            'chat/user/update/',
            token=token, data=settings
        )

        return True
    
    @caimethod
    async def get_personas(
        self, *, token: str = None
    ) -> list:
        """Get all the personas in your account

        EXAMPLE::

            await client.get_personas()

        Returns:
            List of :obj:`~characterai.types.account.PersonaShort`
        """
        data = await self.request(
            'chat/personas/?force_refresh=1',
            token=token
        )

        return validate(
            account.PersonaShort,
            data['personas']
        )

    @caimethod
    async def create_persona(
        self, title: str, *,
        token: str = None,
        definition: str = '',
        custom_id: str = None
    ):
        """Create persona

        EXAMPLE::
        
            await client.create_persona('TITLE')

        Args:
            title (``str``):
                Persona's name
            
            definition (``str``, *optional*):
                Persona's definition
            
            custom_id (``str``, *optional*):
                Your UUID for a persona. If you don't provide it,
                it will be generated automatically

        Returns:
            :obj:`~characterai.types.account.Persona`
        """
        identifier = custom_id or f'id:{uuid.uuid1()}'
        
        data = await self.request(
            'chat/persona/create/',
            token=token, data={
                'title': title,
                'name': title,
                'identifier': identifier,
                'categories': [],
                'visibility': 'PUBLIC',
                'copyable': False,
                'description': 'This is my persona.',
                'greeting': 'Hello! This is my persona',
                'definition': definition,
                'avatar_rel_path': '',
                'img_gen_enabled': False,
                'strip_img_prompt_from_msg': False,
            }
        )
        
        return account.Persona.model_validate(
            data['persona']
        )

    @caimethod
    async def get_persona(
        self, persona_id: str, *, token: str = None
    ):
        """Get information about a persona

        EXAMPLE::
        
            await client.get_persona('ID')

        Args:
            persona_id (``str``):
                Persona's UUID

        Returns:
            :obj:`~characterai.types.account.Persona`
        """
        data = await self.request(
            f'chat/persona/?id={persona_id}',
            token=token
        )

        return account.Persona.model_validate(
            data['persona']
        )
    
    @caimethod
    async def delete_persona(
        self, persona_id: str, *, token: str = None
    ):
        """Delete persona

        EXAMPLE::
        
            await client.delete_persona('ID')

        Args:
            persona_id (``str``):
                Persona's UUID

        Returns:
            :obj:`~characterai.types.account.Persona`
        """
        persona = await self.request(
            f'chat/persona/?id={persona_id}',
            token=token
        )

        data = await self.request(
            'chat/persona/update/',
            token=token, data={
                'archived': True,
                **persona['persona']
            }
        )

        return account.Persona.model_validate(
            data['persona']
        )


    @caimethod
    async def followers(
        self, *, token: str = None
    ) -> list:
        """Get your subscribers

        EXAMPLE::
        
            await client.followers()

        Returns:
            List of ``str``
        """
        return (await self.request(
            'chat/user/followers/',
            token=token
        ))['followers']

    @caimethod
    async def following(
        self, *, token: str = None
    ) -> list:
        """Get those you subscribe to

        EXAMPLE::
        
            await client.following()

        Returns:
            List of ``str``
        """
        return (await self.request(
            'chat/user/following/',
            token=token
        ))['following']

    @caimethod
    async def characters(
        self, *, token: str = None
    ):
        """Get your public characters

        EXAMPLE::
        
            await client.characters()

        Returns:
            List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'chat/characters/?scope=user',
            token=token
        )

        return validate(
            character.CharShort,
            data['characters']
        )
