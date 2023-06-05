from datetime import datetime, timezone, timedelta


def prepare_message_daily(summary, flag, start_date):
    if flag == 1:
        message = "You should be a bull today!"
        image_url = "https://images.unsplash.com/photo-1618325508550-951512a1e82d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8ZmlyZXxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80"
    elif flag == -1:
        message = "You should be a bear today!!"
        image_url = "https://www.pnas.org/cms/10.1073/pnas.2213762119/asset/0f97fae4-c4ce-406c-bb26-1fe058acca2b/assets/images/large/pnas.2213762119fig01.jpg"
    else:
        message = "Today is neutral according to news!"
        image_url = "https://www.tikvahlake.com/wp-content/uploads/Boredom-768x464.jpeg"
    data = {
      "content": "Daily Global Sentiment Analysis",
      "embeds": [
        {
            "title": f"{message} {datetime.strftime(start_date - timedelta(days=1), '%Y-%m-%d')}",
            "description": summary,
            "image": {
                "url": image_url
            }
        }
      ]
    }
    return data


def prepare_message_15m(titles, start_date):
    message = "You should pay attention to the news titles!!"
    image_url = "https://play-lh.googleusercontent.com/XFHFLXe44ikxLT0CLj8vF0DsPRj829qeHQz-6_tSqmbkAZNauGYt03Cc8b4qY7vbfV0"

    data = {
      "content": "News Alert",
      "embeds": [
        {
            "title": f"{message} {datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S`')}",
            "description": titles,
            "image": {
                "url": image_url
            }
        }
      ]
    }
    return data


def generate_summary(obj, input_text):
    # prompt = f"""Assume that you are a crypto investor.
    #     Analyze the market behaviour as positive, negative or neutral.
    #     Prompt only the result, use one word.
    #     """
    prompt = f"""Summarize the below text not less than 200 words:
                {input_text}"""
    response = obj.client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ]
    )
    summary = response.choices[0].message.content
    return summary

def translate_titles(obj, input_text):
    prompt = f"Please translate the following text to English:\n{input_text}\nTranslation:"
    response = obj.client.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ]
    )
    summary = response.choices[0].message.content
    return summary
