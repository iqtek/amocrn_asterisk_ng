from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client
from amocrm_api_client.token_provider import StandardTokenProviderFactory
from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import IFactory
from amocrm_asterisk_ng.infrastructure import IKeyValueStorage
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .AmocrmKernelComponent import AmocrmKernelComponent
from .AmocrmKernelComponentConfig import AmocrmKernelComponentConfig
from .calls import CallManagerComponent
from .raise_card import RaiseCardComponent


__all__ = [
    "AmocrmKernelComponentFactory"
]


class AmocrmKernelComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__app",
        "__dispatcher",
        "__event_bus",
        "__storage",
        "__logger",
    )

    def __init__(
        self,
        app: FastAPI,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        storage: IKeyValueStorage,
        logger: ILogger,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage = storage
        self.__logger = logger

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableComponent:

        settings = settings or {}
        component_config = AmocrmKernelComponentConfig(**settings)

        token_provider_factory = StandardTokenProviderFactory()
        token_provider = token_provider_factory.get_instance(settings=component_config.integration)
        amo_client = create_amocrm_api_client(
            config=AmoCrmApiClientConfig(base_url=component_config.integration["base_url"]),
            token_provider=token_provider,
        )

        call_manager_component = CallManagerComponent(
            settings=component_config.call_logging,
            app=self.__app,
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        raise_card_component = RaiseCardComponent(
            amo_client=amo_client,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )

        amocrm_kernel_component = AmocrmKernelComponent(
            dispatcher=self.__dispatcher,
            amo_client=amo_client,
            raise_card_component=raise_card_component,
            call_manager_component=call_manager_component,
        )

        return amocrm_kernel_component
