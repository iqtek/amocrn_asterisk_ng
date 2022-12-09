from asterisk_ng.system.dispatcher import ICommand

from ...crm_system import CrmUserId


__all__ = ["IOriginationDomainCommand"]


class IOriginationDomainCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        user_id: CrmUserId,
        phone_number: str,
    ) -> None:
        raise NotImplementedError()
