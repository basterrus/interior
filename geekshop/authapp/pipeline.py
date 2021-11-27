from datetime import datetime
import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    url = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'photo_max', 'sex', 'about', ''])

    api_url = f'{url}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data_json = response.json()['response'][0]
    print(data_json)
    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')
        age = datetime.now().year - birthday.year

        if 18 >= age or age >= 100:
            user.delete()
            raise AuthForbidden('social_core.backend.vk.VKOAuth2')
        user.age = age

    if 'about' in data_json:
        user.shopuserprofile.about_me = data_json['about']

    if 'photo_max' in data_json:
        # user.avatar_url = data_json['photo_max']
        photo_path = f'avatar/{user.pk}.jpeg'
        photo_full_path = f'{settings.MEDIA_ROOT}/{photo_path}'
        photo_data = requests.get(data_json['photo_max'])
        with open(photo_full_path, 'wb') as photo_file:
            photo_file.write(photo_data.content)
        user.avatar = photo_path

    user.save()
