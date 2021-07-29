from enum import unique, Enum


@unique
class Plugin(Enum):
    notice_plugin = "notice_plugin"
    qmpparser = "qmpparser"
    weather = "weather"

print("weather" in list(Plugin))
print(Plugin.weather in list(Plugin))
print(list(Plugin))