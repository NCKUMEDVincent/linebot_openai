import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 用你的 Channel Access Token 和 Channel Secret 替換以下兩行
line_bot_api = LineBotApi('4iHM2jHffKNDEPDTWZYGncX8D7Ddwk2dbEY7OGpkwM3Ux77KXJ+cHpGBn1/psnITpZOpqq3jheGD3Uxh6oMWVz3aHmxvRkde/xu8lvgkLlYZhO+3uGJnAbbEY0w3uOYRDoGvaBuLSmkyGoHcQo7QPAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('351f424bf229962145c7cf3e96d774f0')

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 Line 平台的簽名
    signature = request.headers['X-Line-Signature']

    # 將請求的內文轉為文本
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆使用者相同的訊息
    received_text = event.message.text
    reply_text = TextSendMessage(text=received_text)
    line_bot_api.reply_message(event.reply_token, reply_text)

if __name__ == "__main__":
    # 使用 Render 提供的端口
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
