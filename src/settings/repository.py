from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    """Репозиторий для взаимодействия с БД"""
    session: AsyncSession

    async def save_update_object(self, save_object: dict):
        """Сохранить или обновить объект"""
        try:
            self.session.add(instance=save_object)
            await self.session.commit()
            await self.session.refresh(instance=save_object)
        except IntegrityError:
            await self.session.rollback()

    async def delete_object(self, delete_object: dict):
        """Удалить объект"""
        try:
            await self.session.delete(instance=delete_object)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
