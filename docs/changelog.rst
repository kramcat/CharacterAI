#########
Changelog
#########

1.0.0a1
=======

- Adding authorization via mail and as a guest
- Fix old bugs related to authorization by token and chat2
- Added ability to download and upload pictures
- Improved performance by switching to `curl_cffi`
- Adding typing via Pydantic
- Added new features: modify and pin character messages
- Moved documentation to Sphinx Furo
- PyAsyncCAI name changed to AioCAI

0.8.0 - Much faster, chat2, Fixes
=================================

- There is no Playwright anymore, another library is used that does not load the system (!!!)
- Added chat2 support (new chats with a different design)
- Deleted ``client.upload_image()``, ``client.start()``
- chat2 is only available in the asynchronous version
- Fixes and improvements


0.7.0 - Managing Posts and Characters, Upload Images, Create Rooms 
==================================================================

- Small fixes by KubaPro010
- Private variables
- ``start()`` for PyCAI
- Added plus for ``start()``
- Added timeout for ``start()``
- Added ``ping()``, ``upload_image('PATH')``, ``user.update('USERNAME')``, ``character.create(...)``, ``character.update(...)``, ``character.voices()``, ``character.create_room(...)``
- Added the post class
    - ``post.get_post('POST_ID')``
    - ``post.my_posts()``
    - ``post.get_posts('USERNAME')``
    - ``post.upvote('POST_ID')``
    - ``post.undo_upvote('POST_ID')``
    - ``post.send_comment('POST_ID', 'TEXT')``
    - ``post.delete_comment('MESSAGE_ID', 'POST_ID')``
    - ``post.create('HISTORY_ID', 'TITLE')``
    - ``post.delete('POST_ID')``
- Some fixes for parameters, check documentation
- Some optimization
- Added kwargs for functions


0.6.0 - Documentation, New Functions, Fixes
===========================================

- Name of pyCAI changed to PyCAI
- Name of pyAsyncCAI changed to PyAsyncCAI
- Written documentation
- Fix error 500
- Added more errors
- Added ``chat.rate('CHAR', RATE)``
- Added ``chat.next_message('CHAR')``
- Added ``chat.get_chat('CHAR')``
- Added ``chat.delete_message('HISTORY_ID', 'UUIDS_TO_DELETE')``
- Fixed showing filtered messages
- Code changed to PEP8


0.5.0 - POST methods, New chat.get_histories()
===============================================

- Now some functions work via POST requests, it's faster and more reliable
- Fixed ``chat.new_chat()``
- ``chat.send_message()`` was rewritten
    - Instead of an error, it returns an error page
    - This function can show a message even if it is filtered
    - Fixed bugs with JSON
- New ``chat.get_histories('CHAR')``
    - This function returns all the stories with the character
- Find users by nickname with ``user.info('NICKNAME')``
    - This function returns information about the user


0.4.0 - New chat.send_message(), Async, Fixes 
=============================================

- Add user.get_history in async
- Fix ``chat.new_chat()``
- New ``chat.send_message()``
- New chat.get_history()
- ``character.get_info()`` rename to ``character.info()`` and rewritten
- Add character.search()
- Add ``user.recent()``
- Fix small bugs


0.3.0 - Fixed Functions, New Parameters
=======================================

- Fix broken functions
- Remove ``user.get_history`` in async (I'll add in next version)
- Add token parameter on all functions for custom token
- Add wait parameter on all functions for waiting a responce when site is overloaded
- Add headless parameter on pyCAI for browser (I don't know why, but suddenly you need)
- Other changes (I don't remember which ones)