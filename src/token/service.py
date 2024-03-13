from dataclasses import dataclass
from src.token.repository import TokenRepository


@dataclass
class TokenService:
    repository: TokenRepository

    async def find_token(self, jwt_token: str):
        token = await self.repository.find_token(jwt_token=jwt_token)
        return token

    async def verify_token(self):
        token = await self.repository.verify_token()
        return token

    async def get_token_payload(self):
        token_payload = await self.repository.get_token_payload()
        return token_payload
