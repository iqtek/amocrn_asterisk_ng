from typing import Any
from typing import Mapping

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import IPluginFactory

from .FileConverterPlugin import FileConverterPlugin


__all__ = ["FileConverterPluginFactory"]


class FileConverterPluginFactory(IPluginFactory):

    __slots__ = ()

    def __call__(self, settings: Mapping[str, Any]) -> Plugin:
        return FileConverterPlugin()
