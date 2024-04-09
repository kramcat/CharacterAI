from .errors import AuthError, ServerError

from curl_cffi.requests import Session
import uuid

URL = 'https://beta.character.ai'

def sendCode(email: str) -> bool:
    with Session(impersonate='chrome120') as s:
        r = s.post(
            'https://identitytoolkit.googleapis.com'
            '/v1/accounts:sendOobCode?key='
            'AIzaSyAbLy_s6hJqVNr2ZN0UHHiCbJX1X8smTws',
            json={
                'requestType': 'EMAIL_SIGNIN',
                'email': email,
                'clientType': 'CLIENT_TYPE_WEB',
                'continueUrl': 'https://beta.character.ai',
                'canHandleCodeInApp': True
            }
        )

    data = r.json()

    try:
        if data['email'] == email:
            return True
    except KeyError:
        raise ServerError(data['error']['message'])

def authUser(link: str, email: str) -> str:
    with Session(impersonate='chrome120') as s:
        r = s.get(link, allow_redirects=True)

        oobCode = r.url.split('oobCode=')[1].split('&')[0]
        
        r = s.post(
            'https://identitytoolkit.googleapis.com'
            '/v1/accounts:signInWithEmailLink?key='
            'AIzaSyAbLy_s6hJqVNr2ZN0UHHiCbJX1X8smTws',
            headers={
                # Firebase key for GoogleAuth API
                'X-Firebase-AppCheck': 'eyJraWQiOiJYcEhKU0EiLCJ'
                '0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIx'
                'OjQ1ODc5NzcyMDY3NDp3ZWI6YjMzNGNhNDM2MWU5MzRkYWV'
                'iOWQzYiIsImF1ZCI6WyJwcm9qZWN0c1wvNDU4Nzk3NzIwNjc'
                '0IiwicHJvamVjdHNcL2NoYXJhY3Rlci1haSJdLCJwcm92aWR'
                'lciI6InJlY2FwdGNoYV9lbnRlcnByaXNlIiwiaXNzIjoiaHR0'
                'cHM6XC9cL2ZpcmViYXNlYXBwY2hlY2suZ29vZ2xlYXBpcy5jb'
                '21cLzQ1ODc5NzcyMDY3NCIsImV4cCI6MTcxMTAxNzE2MiwiaWF'
                '0IjoxNzEwNDEyMzYyLCJqdGkiOiJkSXlkWVFPZEhnaTRmc2ZGU'
                'DMtWHNZVU0zZG01eFY4R05ncDItOWxCQ2xVIn0.o2g6-5Pl7rj'
                'iKdQ4X9bdOe6tDSVmdODFZUljHDnF5cNCik6masItwpeL3Yh6h'
                '78sQKNwuKzCUBFjsvDsEIdu71gW4lAuDxhKxljffX9nRuh8d0j-'
                'ofmwq_4abpA3LdY12gIibvMigf3ncBQiJzu4SVQUKEdO810oUG8'
                'G4RWlQfBIo-PpCO8jhyGZ0sjcklibEObq_4-ynMZnhTuIN_J183'
                '-RibxiKMjMTVaCcb1XfPxXi-zFr2NFVhSM1oTWSYmhseQ219ppH'
                'A_-cQQIH6MwC0haHDsAAntjQkjbnG2HhPQrigdbeiXfpMGHAxLR'
                'XXsgaPuEkjYFUPoIfIITgvkj5iJ-33vji2NgmDCpCmpxpx5wTHOC'
                '8OEZqSoCyi3mOkJNXTxOHmxvS-5glMrcgoipVJ3Clr-pes3-aI5Y'
                'w7n3kmd4YfsKTadYuE8vyosq_MplEQKolRKj67CSNTsdt2fOsLCW'
                'Nohduup6qJrUroUpN35R9JuUWgSy7Y4MI6NM-bKJ'
            },
            json={
                'email': email,
                'oobCode': oobCode
            }
        )

    data = r.json()

    try:
        idToken = data['idToken']
    except KeyError:
        raise AuthError(data['error']['message'])


    with Session(impersonate='chrome120') as s:
        r = s.post(
            f'{URL}/dj-rest-auth/google_idp/',
            json={
                'id_token': idToken
            }
        )

    data = r.json()

    try:
        return data['key']
    except KeyError:
        raise AuthError(data['error'])

def authGuest() -> str:
    with Session(impersonate='chrome120') as s:
        r = s.post(
            f'{URL}/chat/auth/lazy/',
            json={
                'lazy_uuid': str(uuid.uuid1())
            }
        )

    data = r.json()

    try:
        return data['token']
    except KeyError:
        raise AuthError(data['error'])