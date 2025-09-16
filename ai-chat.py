import g4f
import asyncio

messages_count = 2 # Количество реплик на каждого бота

MC = {"bot1": messages_count, "bot2": messages_count}

# Стартовые промпты + сохранение реплик
MESSAGES = {
    "bot1":
        [
            {"role": "system", "content": "Представь, что ты - молодой человек на первом свидании. Ты немного стесняешься, но стараешься быть вежливым и немногословным.  Отвечай кратко, спокойно и по делу, как обычный парень. Постарайся давать ответы одним-двумя предложениями."},
            {"role": "system", "content": "Ты на первом свидании с девушкой.  Постарайся завязать разговор, но не будь слишком навязчивым. Начни общение."}
        ],
    "bot2":
        [
           {"role": "system", "content": "Представь, что ты - молодая девушка на первом свидании. Ты немного стесняешься, но стараешься быть приветливой и доброжелательной. Говори как обычная девушка.  Старайся проявлять интерес к собеседнику."},
           {"role": "system", "content": "Ты на первом свидании с парнем.  Жди, когда он начнет общение, но не молчи слишком долго. Покажи, что ты заинтересована в разговоре."}
        ]
    }

# Начало разговора
def get_first_response(bot):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=MESSAGES[f"bot{bot}"],
        )
    
    MESSAGES[f"bot{bot}"].append({"role": "assistant", "content": response})
    return response

# Получение ответа
def get_response(bot, message):
    MESSAGES[f"bot{bot}"].append({"role": "user", "content": message})
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=MESSAGES[f"bot{bot}"],
        )
    
    MESSAGES[f"bot{bot}"].append({"role": "assistant", "content": response})
    return response

async def main():
    first_response = get_first_response(1)
    print(f"Бот-1: {first_response}")
    MC["bot1"] -= 1
    
    while MC["bot1"] >= 0 and MC["bot2"] > 0:
        response2 = get_response(2, first_response)
    
        print(f"Бот-2: {response2}")
        MC["bot2"] -= 1
        if MC["bot2"] <= 0:
            break
            
        response1 = get_response(1, response2)
        
        print(f"Бот-1: {response1}")
        MC["bot1"] -= 1
        if MC["bot1"] < 0:
            break

        first_response = response1
        

asyncio.run(main())