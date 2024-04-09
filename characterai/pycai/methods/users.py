from ...errors import NotFoundError
from ...types import user

from .utils import caimethod

class Users:
    @caimethod
    def get_user(
        self, username: str, *, token: str = None
    ):
        """User info by nickname

        EXAMPLE::

            await client.get_user('USERNAME')

        Args:
            username (``str``):
                User nickname

        Returns:
            :obj:`~characterai.types.user.User`
        """
        data = self.request(
            'chat/user/public/', token=token,
            data={'username': username}
        )

        if data['public_user'] == []:
            raise NotFoundError(
                f'User {username} not found.'
            )

        return user.User.model_validate(
            data['public_user']
        )