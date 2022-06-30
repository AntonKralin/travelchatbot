from loadservice import bot
from classes.models import TableCommand, TableHotel, TableState
import commands


TableCommand.create_table()
TableHotel.create_table()
TableState.drop_table()
TableState.create_table()
bot.polling(none_stop=True, interval=0)
