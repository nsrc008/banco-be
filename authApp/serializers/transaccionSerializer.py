from authApp.models.account import Account
from authApp.models.user    import User
from authApp.models.account import Account
from backend.authApp.models import Account
from backend.authApp.models.user import User
from backend.authApp.models.transaccion import Transaccion
from rest_framework         import serializers

class TransaccionSerializer(serializers.ModelSerializaer):
    class Meta:
        models = Transaccion
        fields = ["origin_account", "destiny_account", "ammount", "register_date", "note"]

    def to_representation(self, obj):
        transaccion = Transaccion.objects.get(id=obj.id)
        origin_account = Account.objects.get(id=transaccion.origin_account_id)
        destiny_account = Account.objects.get(id=transaccion.destiny_account_id)
        destiny_user = User.objects.get(id=destiny_account.user_id)
        return {
            'id'            : transaccion.id,
            'amount'        : transaccion.amount,
            'register_date' : transaccion.register_date,
            'note'          : transaccion.note,
            'origin_account': {
                'id'         : origin_account.id,   
                'balanace'   : origin_account.balance
            },
            'destiny_account': {
                'id'    : destiny_account.id,
                'user'  : destiny_user.user
            }
        }
