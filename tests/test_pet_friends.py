from tests.api import PetFriends
from tests.settings import valid_email, valid_password
import os

pf = PetFriends()

def test_successful_add_new_pet_without_photo(name="Lulu", animal_type='Кошка', age=3):
    """Создание нового питомца без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_pet_without_photo(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    print(pet_id)

    assert status == 200
    assert result['name'] == name

def test_unsuccessful_get_api_key_for_unvalid_user(email='1970sukor@mail.ru', password='123456789'):
    """ Проверка что запрос возвращает статус 403, поскольку введены не существующий данные: email, password"""
    status, result = pf.get_api_key(email, password)

    assert status == 403



def test_successful_add_photo_pet(pet_id ='68faf579-4054-493f-ab49-511f8bb10e92',pet_photo='cat1.jpg'):
    """Добавление фотографии к созданному питомцу по его ID"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200

def test_unsuccessful_add_new_pet(name="Нy, поехали, 69,dhskgfhdjлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghghорывлпрлврпdhskgfhdjghорыворывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghоры",
                                  animal_type='ice', age=-200):
    """Создание нового питомца с некорректными данными, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_pet_without_photo(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)
    assert status == 400  #данные не валидны, но питомец создается
    assert result['name'] == name

def test_successful_delete_self_pet_id(pet_id='a3096c33-9f59-43df-badc-e317d53fc316'):
    """Удаление питомца по его ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_unsuccessful_get_pets(filter='my_pets'):
    """ Проверка возможность получения списка питомцев по несуществующему API ключу"""
    email = '1970sukor@mail.ru'
    password = '123456789'
    _, auth_key = pf.get_api_key(email, password)
    if auth_key != pf.get_api_key(valid_email, valid_password):
        print('Данный API ключ не существует, невозможно вывести список питомцев! ')
    else:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

def test_unsuccessful_delete_pets(pet_id='3f8aa309-57ec-463b-b739-2a00e484a569'):
    """ Проверка удаления питомца по не существующему API ключу"""
    email = '1970sukor@mail.ru'
    password = '12345678'
    _, auth_key = pf.get_api_key(email, password)
    if auth_key != pf.get_api_key(valid_email, valid_password):
        print('Питомец не удален! Так как данный API ключ не существует')
    else:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

def test_unsuccessful_add_new_pet_without_photo(name='Ash', animal_type='Кошка',age= 7, pet_photo=''):
    """Проверка возможности добавления питомца с корректными данными без фотографии"""
    if pet_photo != os.path.join(os.path.dirname(__file__), pet_photo):
        print('Питомец не создан! Загрузите, пожалуйта, его фотографию!')
    else:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

def test_unsuccessful_update_info_pet(name='Лапа',pet_id='23', animal_type='Кролик', age=2):
    """Проверка невозможности обновления информации о питомце при вводе не существующего ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400

def test_unsuccessful_add_new_pet_photo(name='', animal_type='Кошка',
                                     age='ляляля', pet_photo='cat2.jpg'):
    """Проверка добавления питомца с некорректными данными, запрос возвращает статус 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400  #тест провален, вовращается код 500
    assert result['name'] == name