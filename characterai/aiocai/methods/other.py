from .utils import caimethod, validate
from ...types import other

from curl_cffi import CurlMime

class Other:
    @caimethod
    async def create_image(
        self, promt: str, *, token: str = None
    ):
        """Image generation by description

        EXAMPLE::

            await client.create_image('PROMT')

        Args:
            promt (``str``):
                Image description

        Returns:
            :obj:`~characterai.types.other.Image`
        """
        data = await self.request(
            'chat/generate-image/',
            token=token, data={
                'image_description': promt
            }
        )

        return other.Image(
            url=data['image_rel_path'],
            type='CREATED'
        )

    @caimethod
    async def upload_image(
        self, file: str, *, token: str = None
    ):
        """Uploading an image to the server

        EXAMPLE::

            await client.upload_image('FILENAME.PNG')

        Args:
            file (``str``):
                File path

        Returns:
            :obj:`~characterai.types.other.Image`
        """
        mp = CurlMime()
        mp.addpart(
            name='image',
            content_type='image/png',
            filename=file,
            local_path=file,
        )

        data = await self.request(
            'chat/upload-image/',
            data={}, multipart=mp,
            token=token
        )

        return other.Image(
            url=data['value']
        )

    @caimethod
    async def ping(
        self, *, token: str = None
    ) -> bool:
        """Performance check

        EXAMPLE::

            await client.ping()

        Returns:
            ``bool``
        """
        data = await self.request(
            'ping/', neo=True,
            token=token
        )

        if data['status'] == 'pong':
            return True

        return False

    @caimethod
    async def get_voices(
        self, *, token: str = None
    ) -> list:
        """List of available ready-made voices

        EXAMPLE::

            await client.get_voices()

        Returns:
            List of :obj:`~characterai.types.other.Voice`
        """
        data = await self.request(
            'chat/character/voices/',
            token=token
        )
        
        return validate(
            other.Voice, data['voices']
        )