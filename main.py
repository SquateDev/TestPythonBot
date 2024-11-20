
import telebot

API_TOKEN = '7702376835:AAG7lyfjFwDfQKmirLp3qFxvsWtsbi5m_R8'
bot = telebot.TeleBot(API_TOKEN)
print("Bot Run!");

@bot.message_handler(commands=['start'])
def handle_video(message):
    bot.reply_to(message, f"Привет, отправь мне видео и я сделаю из него кружочек!")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        video_id = message.video.file_id
        file_info = bot.get_file(video_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('input_video.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)

        # Загрузка видео и обрезка до квадратного формата (например, 1:1)
        video = VideoFileClip('input_video.mp4')
        width, height = video.size
        min_dimension = min(width, height)
        square_video = video.crop(x_center=width / 2, y_center=height / 2, width=min_dimension, height=min_dimension)

        # Сохранение обрезанного видео
        square_video.write_videofile('output_video.mp4')

        # Отправка обрезанного видео как обычное видеосообщение
        with open('output_video.mp4', 'rb') as video_file:
            bot.send_video_note(message.chat.id, video_file)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}.")

bot.polling()
