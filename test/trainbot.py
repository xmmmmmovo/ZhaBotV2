from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    '小扎',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    database_uri='mongodb://127.0.0.1:27017/chat'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.chinese")
