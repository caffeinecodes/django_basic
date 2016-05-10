from requests import request, HTTPError

from django.core.files.base import ContentFile


def save_profile_picture(strategy, user, response, details, is_new=False,
                         *args, **kwargs):
    # Save Facebook profile photo into a user profile, assuming a profile model
    # with a profile_photo file-type attribute
    if is_new and strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        print(url)
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile = user.get_profile()
            print(profile)
            profile.profile_photo.save('{0}_social.jpg'.format(user.username),
                                       ContentFile(response.content))
            print(ContentFile(response.content))
            profile.save()


def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
        print(url)
        # print(user)
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        user.display_image = url
        print(user)
        print(user.display_image)
        user.save()