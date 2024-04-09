from .utils import caimethod, validate
from ...types import character

import uuid

class Characters:
    @caimethod
    async def get_char(
        self, external_id: str,
        *, token: str = None
    ):
        """Get information about the character

        EXAMPLE::

            await client.get_char('ID')

        Args:
            external_id (``str``): Character ID

        Returns:
            :obj:`~characterai.types.character.Character`
        """
        data = await self.request(
            'chat/character/info/', token=token,
            data={'external_id': external_id}
        )

        return character.Character.model_validate(
            data['character']
        )

    @caimethod
    async def upvoted(self, *, token: str = None):
        """The list of characters you have given a voice to

        EXAMPLE::

            await client.upvoted()

        Returns:
            List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'chat/user/characters/upvoted/',
            token=token
        )

        return validate(
            character.CharShort,
            data['characters']
        )

    @caimethod
    async def get_category(
        self, name: str = 'All',
        *, token: str = None
    ):
        """Get characters from categories

        EXAMPLE::

            await client.get_category()

        Args:
            name (``str``): Category name

        Returns:
            :obj:`~characterai.types.character.Categories` | List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'chat/curated_categories'
            '/characters/',
        )

        categories = data['characters_by_curated_category']

        if name != 'All':
            return character.CharShort.model_validate(
                categories[name]
            )

        return character.Categories.model_validate(
            categories
        )

    @caimethod
    async def get_recommended(
        self, *, token: str = None
    ):
        """Get a list of recommended characters

        EXAMPLE::

            await client.get_recommended()

        Returns:
            List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'chat/characters/trending/'
        )
        
        return validate(
            character.CharShort,
            data['trending_characters']
        )

    @caimethod
    async def get_trending(
        self, *, token: str = None
    ):
        """Get a list of trending characters

        EXAMPLE::

            await client.get_trending()

        Returns:
            List of :obj:`~characterai.types.character.CharShort`
        """
        data = await self.request(
            'recommendation/v1/user',
            token=token, neo=True
        )

        return validate(
            character.CharShort,
            data['characters']
        )
    
    @caimethod
    async def create_char(
        self,
        name: str,
        greeting: str,
        *,
        tgt: str = None,
        title: str = '',
        visibility: str = 'PRIVATE',
        copyable: bool = True,
        description: str = '',
        definition: str = '',
        avatar_path: str = '',
        token: str = None,
        **kwargs
    ):
        """Create a character

        EXAMPLE::

            await client.create_char('NAME', 'GREETING')

        Args:
            name (``str``):
                Character name
            
            greeting (``str``):
                Character greeting
            
            tgt (``str``, *optional*):
                Old type Character ID
            
            title (``str``, *optional*):
                Short description of the character
            
            visibility (``str``, *optional*):
                Character visibility
            
            copyable (``bool``, *optional*):
                Ability to copy a character
            
            description (``str``, *optional*):
                Character description
            
            definition (``str``, *optional*:
                Character definition (memory, chat examples)
            
            avatar_path (``str``, *optional*):
                Path to the character's avatar on the c.ai server.
                Example: ``uploaded/2022/12/26/some_id.webp`` 

        Returns:
            :obj:`~characterai.types.character.Character`
        """
        tgt = f'id:{uuid.uuid4()}' or tgt

        data = await self.request(
            'chat/character/create/',
            token=token, data={
                'title': title,
                'name': name,
                'identifier': tgt,
                'visibility': visibility,
                'copyable': copyable,
                'description': description,
                'greeting': greeting,
                'definition': definition,
                'avatar_rel_path': avatar_path,
                **kwargs
            }
        )
 
        return character.Character.model_validate(
            data['character']
        )

    @caimethod
    async def update_char(
        self,
        char: str,
        *,
        greeting: str = '',
        name: str = '',
        title: str = '',
        visibility: str = 'PRIVATE',
        copyable: bool = True,
        description: str = '',
        definition: str = '',
        archived: bool = False,
        default_voice_id: str = '',
        voice_id: str = '',
        strip_img_prompt_from_msg: bool = False,
        base_img_prompt: str = '',
        img_gen_enabled: bool = False,
        avatar_rel_path: str = '',
        categories: list = [],
        token: str = None
    ):
        """Editing a character

        EXAMPLE::

            await client.create_char('CHAR_ID', 'NAME', 'GREETING')

        Args:
            char (``str``):
                Character ID
            
            name (``str``, *optional*):
                Character name
            
            greeting (``str``, *optional*):
                Character greeting
            
            title (``str``, *optional*):
                Short description of the character
            
            visibility (``str``, *optional*):
                Character visibility
            
            copyable (``bool``, *optional*):
                Ability to copy a character
            
            description (``str``, *optional*):
                Character description
            
            definition (``str``, *optional*):
                Character definition (memory, chat examples)

            default_voice_id (``str``, *optional*):
                Voice ID for TTS

            voice_id (``str``, *optional*):
                Voice ID for TTS

            strip_img_prompt_from_msg (``bool``, *optional*):
                Remove the picture hint from the message.
                I guess that means the characters
                won't be able to see the pictures (?)

            base_img_prompt (``str``, *optional*):
                Default promt for pictures (?)

            img_gen_enabled (``bool``, *optional*):
                Can pictures be generated

            avatar_rel_path (``str``, *optional*):
                Path to the character's avatar on the c.ai server.
                Example: ``uploaded/2022/12/26/some_id.webp`` 

            categories (``list``, *optional*):
                Character сategories

            archived (``bool``, *optional*):
                Is the character archived

        Returns:
            :obj:`~characterai.types.character.Character`
        """
        charInfo = await self.request(
            'chat/character/info/', token=token,
            data={'external_id': char}
        )
        
        info = charInfo['character']
    
        data = await self.request(
            'chat/character/update/',
            token=token, data={
                'external_id': char or info['external_id']['external_id'],
                'name': name or info['name'],
                'greeting': greeting or info['greeting'],
                'title': title or info['title'],
                'visibility': visibility or info['visibility'],
                'copyable': copyable or info['copyable'],
                'description': description or info['description'],
                'definition': definition or info['definition'],
                'default_voice_id': default_voice_id or info['default_voice_id'],
                'voice_id': voice_id or info['voice_id'],
                'strip_img_prompt_from_msg': strip_img_prompt_from_msg \
                    or info['strip_img_prompt_from_msg'],
                'base_img_prompt': base_img_prompt or info['base_img_prompt'],
                'img_gen_enabled': img_gen_enabled or info['img_gen_enabled'],
                'avatar_rel_path': avatar_rel_path or info['avatar_file_name'],
                'categories': categories or [],
                'archived': archived or None
            }
        )

        return character.Character.model_validate(
            data['character']
        )