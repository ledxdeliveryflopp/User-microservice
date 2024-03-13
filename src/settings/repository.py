from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    session: AsyncSession
    object: dict

    async def save_update_object(self):
        self.session.add(instance=self.object)
        await self.session.commit()
        await self.session.refresh(instance=self.object)

    async def delete_object(self):
        await self.session.delete(instance=self.object)
        await self.session.commit()
