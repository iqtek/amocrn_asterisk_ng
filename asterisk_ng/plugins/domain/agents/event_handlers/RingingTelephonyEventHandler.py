from typing import Mapping

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import ISendCallNotificationCommand
from asterisk_ng.interfaces import RingingTelephonyEvent

from asterisk_ng.system.event_bus import IEventHandler


__all__ = ["RingingTelephonyEventHandler"]


class RingingTelephonyEventHandler(IEventHandler):

    __slots__ = (
        "__phone_to_agent_id_mapping",
        "__send_call_notification_command",
    )

    def __init__(
        self,
        phone_to_agent_id_mapping: Mapping[str, CrmUserId],
        send_call_notification_command: ISendCallNotificationCommand,
    ) -> None:
        self.__phone_to_agent_id_mapping = phone_to_agent_id_mapping
        self.__send_call_notification_command = send_call_notification_command

    async def __call__(self, event: RingingTelephonyEvent) -> None:

        try:
            agent_id = self.__phone_to_agent_id_mapping[event.called_phone_number]
        except KeyError:
            return

        await self.__send_call_notification_command(
            phone_number=event.caller_phone_number,
            users=(agent_id,)
        )
