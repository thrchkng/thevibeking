class Phone:

    line_type = 'проводной'

    def __init__(self, dial_type_value):
        self.dial_type = dial_type_value

    def ring(self):
        print('Дзззззыыыыыыыынь!')

    def call(self, phone_number):
        print(f'Звоню по номеру {phone_number}! Тип связи - {self.line_type}.')

    def dial_type_upgrade(self, new_dial_type):
        self.dial_type = new_dial_type


rotary_phone = Phone(dial_type_value='дисковый')

print(rotary_phone)
