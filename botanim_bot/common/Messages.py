GREETINGS = """Привееет!

Это Telegram-бот книжного клуба Ботаним.

Здесь можно посмотреть список книг, которые мы читали и планируем читать, \
а также проголосовать за следующую книгу.

Присоединяйся к клубу: https://botanim.to.digital

Команды бота:

/start — приветственное сообщение
/help — справка
/allbooks — все книги, который есть в нашем списке
/already — прочитанные книги
/now — книга, которую сейчас читаем
/vote — проголосовать за следующую книгу
/voteresults — текущие результаты текущего голосования
"""

HELP = """Наш книжный клуб работает по ежемесячной подписке, которая \
стоит 1500 руб/мес. Подписка работает через бот @donate, для того, чтобы \
подписаться, перейдите по этой ссылке: https://t.me/+IyGKU9EIGP5jMTky

Если у вас не получается подписаться или есть иные вопросы, напишите на почту \
sterx@rl6.ru
"""

VOTE = """Выше я отправил тебе все книги, которые можно выбрать. Вжууух!

Тебе нужно выбрать три книги.

Пришли в ответном сообщении номера книг, которые ты хочешь прочитать. Номера \
можно разделить пробелами, запятыми или переносами строк.

Обрати внимание, что порядок важен — на первом месте книга, которую ты максимально \
хочешь прочесть сейчас."""

VOTE_PROCESS_INCORRECT_INPUT = """Не смог прочесть твоё сообщение.

Напиши три разных номера книги в одном сообщении, наример, так:

53, 8, 102"""


VOTE_PROCESS_INCORRECT_BOOKS = """Переданы некорректные номера книг, пожалуйста,
проверь их!

Нужно передать номера книг из списка выше.
"""

NO_ACTUAL_VOTING = """Сейчас нет активного голосования.

Голосование обычно запускается на ограниченное время на несколько дней.
"""

NO_VOTE_RESULTS = """Сейчас нет активного голосования, поэтому нет и его
результатов:)
"""

SUCCESS_VOTE = """Ура, ты выбрал {books_count}:

{books}

Ты можешь переголосовать до тех пор, пока голосование активно. Для этого просто \
проголосуй повторно с командой
/vote
"""

SUCCESS_VOTE_BOOK = """{index}. {book.name}"""

VOTE_RESULTS = """ТОП 10 книг голосования

{books}

Даты голосования: с {voting_start} по {voting_finish}
"""

VOTE_RESULT_BOOK = """{index}. {book_name}. Рейтинг: {book_score}"""

ALREADY = """Прочитанные книги:

{books}
"""

ALREADY_BOOK = """{index}. {book.name} (читали с {book.read_start} \
по {book.read_finish})"""

NOW = """Сейчас мы читаем:

{books}
"""

NOW_BOOK = """{index}{book.name} (с {book.read_start} по {book.read_finish})"""