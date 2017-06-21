# import urlparse
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.text import force_unicode
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.utils.six.moves.urllib import parse as urlparse
# from django.utils.text import force_unicode

from storages.utils import setting

try:
    import oss2
except ImportError:
    raise ImproperlyConfigured("Could not load aliyun oss2 sdk dependency.\
        \nSee https://help.aliyun.com/document_detail/32026.html")


class OSS2Storage(Storage):

    custom_domain = setting('ALIYUN_CUSTOM_DOMAIN')
    access_key = setting('ALIYUN_ACCESS_KEY')
    access_secret = setting('ALIYUN_ACCESS_KYE_SECRET')
    endpoint = setting('OSS_ENDPOINT')
    bucket_name = setting('OSS_BUCKET')

    def __init__(self, base_url=settings.MEDIA_URL):
        self.base_url = base_url

    @property
    def bucket(self):
        if self._bucket is None:
            auth = oss2.Auth(self.access_key, self.access_secret)
            self._bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        return self._bucket

    def _open(self, filename, mode='rb'):
        f   = self.bucket.get_object(filename)
        return File(file=f, name=filename)

    def filesize(self, filename):
        raise NotImplemented

    def exists(self, filename):
        f = oss2.ObjectIterator(self.bucket, prefix=filename)
        for row in f:
            if filename == row.key:
                return True
        return False

    def save(self, filename, raw_contents):
        filename = self.get_available_name(filename)
        success = self.bucket.put_object(filename, raw_contents)
        if (success.status == 200):
            return force_unicode(filename.replace('\\', '/'))
        else:
            print ("FAILURE writing file {filename}".format(filename= filename))

    def delete(self, filename):
        success     = self.bucket.delete_object(filename)
        if (success.status == 200):
            return True
        return False

    def url(self, filename):
        return urlparse.urljoin(self.base_url, filename).replace('\\', '/')


