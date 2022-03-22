import uuid
from datetime import datetime

from models import User, ExchangeRate


class UserRepository:
    model = User

    def create(self, user, password):
        try:
            created_user = self.model.create(
                id=str(uuid.uuid4()),
                username=user,
                password=password,
                request_limit=10
            )
            return created_user
        except Exception as e:
            print(str(e))
            return None

    def auth(self, user_name, password):
        try:
            return self.model.select().where(
                (self.model.username == user_name) &
                (self.model.password == password)).dicts().get()
        except Exception as e:
            print(e)
            return None


class ExchangeRateRepository:
    model = ExchangeRate

    def findByUserId(self, user_id):
        try:
            return self.model.select().where(self.model.user_id == user_id).dicts().get()
        except Exception as e:
            print(e)
            return None

    def create(self, data):
        try:
            inserted_data = self.model.create(
                id=str(uuid.uuid4()),
                user_id=data['user_id'],
                exchange_provider=data['provider'],
                exchange_rate=data['exchange_rate'],
                last_update=data['last_update']
            )

            return inserted_data
        except Exception as e:
            print(e)
            return None

    def upsert(self, fix_data, user_id=''):
        user_exchanges = self.findByUserId(user_id)
        result_data = {'rates': []}
        try:
            if not user_exchanges:

                for dat in fix_data:
                    created_data = self.create({
                        'user_id': user_id,
                        'provider': dat['provider'],
                        'exchange_rate': dat['fix'],
                        'last_update': datetime.now()
                    })

                    result_data['rates'].append({
                        created_data.exchange_provider: {
                            'last_updated': created_data.last_update,
                            'value': created_data.exchange_rate
                        }
                    })
            else:
                for dat in fix_data:
                    exchange = self.model.select().where(
                        (self.model.user_id == user_id) &
                        (self.model.exchange_provider == dat['provider'])
                    ).first()
                    exchange.exchange_rate = dat['fix']
                    exchange.last_update = datetime.now()
                    exchange.save()
                    result_data['rates'].append({
                        exchange.exchange_provider: {
                            'last_updated': exchange.last_update,
                            'value': exchange.exchange_rate
                        }
                    })
        except Exception as e:
            print(str(e))

        return result_data
