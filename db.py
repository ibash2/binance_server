from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf import AppConfig


engine = create_engine(AppConfig.alchemy_url)

def get_api(user_id: int):

    # Открываем соединение
    connection = engine.connect()

    try:
        query = text(
            f"select value,type from user_api_keys where user_id={user_id}")
        result = connection.execute(query)
        row = result.fetchall()
        if row:
            if row[0][1] == "SECRET_KEY" and row[1][1] == "API_KEY":
                api_key = row[1][0]
                secret_key = row[0][0]
            else:
                api_key = row[0][0]
                secret_key = row[1][0]
                
            return api_key, secret_key
        
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Закрываем соединение
        connection.close()

    # Тестовые Api
    # api_key_t = "7JuvXA8neo677M77iqnJaEDL85cxJ8duX34JmSI1XJrCGmyMqoYUi8dwg7JMz4aY"
    # sicret_key_t = "o40b1Zx2OqJgVSde2MBtWizdkLQwId9KnJessb10x3Lf67ij70uNrvDdYEMgLmm1"

    # return api_key_t, sicret_key_t
