import logging
import json

from telegram import ( Poll, ParseMode, Update)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler, CallbackContext)

# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def poll(update: Update, context: CallbackContext) -> None:
    # Sends a predefined poll
    questions = ["Mon 7-10pm @MPH","Thurs 2-5pm @MPH","Sun 2-5pm @DS1&2"]
    message = context.bot.send_poll(
        update.effective_chat.id,
        "Coming for training this week?",
        questions,
        is_anonymous = False,
        allows_multiple_answers = True,
    )
    # Save some info about the poll for later use in receive_poll_answer
    payload = {
        message.poll.id:{
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)


def add_data_to_json(json_filepath, data):
    json_data = json.load(open(json_filepath, 'r+'))
    json_data.append(data)
    json.dump(json_data, open(json_filepath, 'w'))
    return json_data
   
 
def receive_poll_bot(update: Update, context:CallbackContext) -> None:
    # summarize a users poll vote
    answer = update.poll_answer
    poll_id = answer.poll_id
    context.bot_data['previous_poll_id'] = poll_id
    user = update.effective_user["username"]
    option = answer["option_ids"]
    add_data_to_json("info.json", [user,option]) 

def close(update:Update, context:CallbackContext) -> None:  
    poll_id = context.bot_data['previous_poll_id']    
    context.bot.stop_poll(
        context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
    ) 

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater('963449057:AAHIO6AWfT9SoM6davoXBr2Y1TdRd9eROnQ')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('poll', poll))
    dispatcher.add_handler(PollAnswerHandler(receive_poll_bot))
    dispatcher.add_handler(CommandHandler('close',close))

    updater.start_polling()
    
    updater.idle()


if __name__ == '__main__':
    main()


