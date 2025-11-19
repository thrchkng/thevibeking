```
Шифратор / Дешифратор текста, основанный на шифре Цезаря
```
class CipherMaster:
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    def process_text(self, text, shift, is_encrypt):  
        if is_encrypt:  # Шифрация текста
            lower_text = text.lower()
            result = []
            for letter in lower_text:
                if letter in list(self.alphabet):
                    ind = self.alphabet.index(letter)
                    shifted = (ind + shift) % len(self.alphabet)
                    new_letter = self.alphabet[shifted]
                    result.append(new_letter)
                else:
                    result.append(letter)
            return ''.join(result)
        else:
            lower_text = text.lower()  # Дешифрация текста
            result = []
            for letter in lower_text:
                if letter in list(self.alphabet):
                    ind = self.alphabet.index(letter)
                    shifted = (ind - shift) % len(self.alphabet)
                    new_letter = self.alphabet[shifted]
                    result.append(new_letter)
                else:
                    result.append(letter)
            return ''.join(result)



is_encrypt = str(input('Шифруем/Дешифруем? (y/n) '))
if is_encrypt == 'y':
    is_encrypt = True
else: 
    is_encrypt = False
text = str(input('Введите текст для шифрования:'))
shift = int(input('Введите шаг шифра:'))
cipher_master = CipherMaster()
print(cipher_master.process_text(text, shift, is_encrypt))
