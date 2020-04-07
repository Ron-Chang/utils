import os
import time
import base64
import requests

from io import BytesIO

from urllib3.exceptions import MaxRetryError
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image

from spyder_common.debugtool import DebugTool
from spyder_common.const import SOURCE


class ImageRequestProcessor:
    """
        Aim to get response and parse the error content
    """
    SCREEN_WIDTH = os.get_terminal_size(0)[0]

    supported_extension = set(Image.registered_extensions())
    image_content_minimum_size = 50

    def __init__(self, url, timeout=60):
        self.start = time.time()
        self.url = url
        self.timeout = timeout
        self.extension = self._get_extension()
        self.image_content = self.get_image_content()

    def _is_timeout(self):
        now = time.time()
        duration = now - self.start
        if duration > self.timeout:
            return True
        return False

    def _is_supported(self):
        """
        Supported Format:[
        '.blp', '.bmp', '.dib', '.bufr', '.cur', '.pcx', '.dcx', '.dds',
        '.ps', '.eps', '.fit', '.fits', '.fli', '.flc', '.ftc', '.ftu',
        '.gbr', '.gif', '.grib', '.h5', '.hdf', '.png', '.apng', '.jp2',
        '.j2k', '.jpc', '.jpf', '.jpx', '.j2c', '.icns', '.ico', '.im',
        '.iim', '.tif', '.tiff', '.jfif', '.jpe', '.jpg', '.jpeg', '.mpg',
        '.mpeg', '.mpo', '.msp', '.palm', '.pcd', '.pdf', '.pxr', '.pbm',
        '.pgm', '.ppm', '.pnm', '.psd', '.bw', '.rgb', '.rgba', '.sgi',
        '.ras', '.tga', '.icb', '.vda', '.vst', '.webp', '.wmf', '.emf',
        '.xbm', '.xpm']
        """
        if self.extension in self.supported_extension:
            return True
        return False

    def _get_extension(self):
        extension = os.path.splitext(self.url)[1]
        if extension:
            return extension.lower()
        return None

    def _request_image_content(self):
        while True:
            timeout = self.timeout
            url = self.url
            start = self.start
            if self._is_timeout():
                DebugTool.error(f'REQUEST TIMEOUT ({timeout} Secs.): {url}')
                response_content = None
                break
            try:
                response = requests.get(url)
                response_content = response.content
                break
            except MaxRetryError as e:
                DebugTool.error(e)
                response_content = None
                break
            except Exception as e:
                DebugTool.error(e)
                time.sleep(0.5)
        return response_content

    def get_image_content(self):
        if not self._is_supported:
            DebugTool.info(f'{self.extension} IS NOT SUPPORTED: {self.url}')
            return None
        image_content = self._request_image_content()
        minimum_size = self.image_content_minimum_size
        if len(image_content) < self.image_content_minimum_size:
            DebugTool.info(f'IMAGE LENGTH IS TOO SHORT: {len(image_content)} {self.url}')
            return None
        if b'Error' in image_content:
            #  error URL request from FOTMOB
            DebugTool.info(f'IMAGE CONTENT NOT FOUND: {self.url}')
            return None
        if b'Not Found' in image_content:
            #  error URL request from GOAL
            DebugTool.info(f'IMAGE CONTENT NOT FOUND: {self.url}')
            return None
        return image_content


class ImagePathProcessor:
    """
        Aim to easily create a path through few parameters:
        format: static/<category>/<prefix>_<subject>/<source>/
        e.g.
            f'static/image/league_logo/{SOURCE.FOTMOB}/'
            f'static/image/news_image/{SOURCE.GOAL}/'

        StaticPathHandler(prefix='league', subject='logo', source='goal').path
        :return:'static/image/league_logo/3/'
    """
    SCREEN_WIDTH = os.get_terminal_size(0)[0]

    PREFIX = ['league', 'team', 'player', 'news']

    SUBJECT = {
        'image': {'logo', 'image'},
        'document': {'csv', 'xml'}
    }

    DEFAULT_CATEGORY = 'temp'

    def __init__(self, prefix, subject, source):
        self.prefix = prefix.lower()
        self.subject = subject.lower()
        self.source = source.upper()
        self.source_code = self.get_source_code()
        self.category = self.get_category()
        self.path = self.get_path()

        self.create_dir()

    def get_category(self):
        for key, value in self.SUBJECT.items():
            if self.subject in value:
                return key
        return self.DEFAULT_CATEGORY

    def get_source_code(self):
        source_code = getattr(SOURCE, self.source, None)
        if not source_code:
            error_info = f' INVALID SOURCE ATTRIBUTE: "{source}" '
            raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')
        return source_code

    def get_path(self):
        return (f'static/{self.category}/{self.prefix}_{self.subject}/{self.source_code}/')

    def create_dir(self):
        os.makedirs(self.path, exist_ok=True)

    @staticmethod
    def get_filename(prefix, target_id, extension):
        """
        Accept 'jpg', 'JPG', '.jpg'.
        """
        width = os.get_terminal_size(0)[0]
        if type(prefix) is str:
            prefix = prefix.lower()
        else:
            error_info = f' INVALID PREFIX TYPE: {prefix} {type(prefix)} '
            raise Exception(f'\n{error_info:-^{width}}')
        if type(extension) is str:
            extension = extension.lower()
            extension = extension.lstrip('.')
        else:
            error_info = f' INVALID EXTENSION TYPE: {extension} {type(extension)} '
            raise Exception(f'\n{error_info:-^{width}}')
        return f'{prefix}_{target_id}.{extension}'


class ImageProcessor:
    """
        Aim to convert, download image and get converted content as base64 into database
    """

    PREFIX = ImagePathProcessor.PREFIX

    EXTENSION_DICT = Image.registered_extensions()

    SCREEN_WIDTH = os.get_terminal_size(0)[0]

    def __init__(self, image_content, mode, extension, download_image=False, path=None, prefix=None, target_id=None):
        self.image_content = image_content
        self.mode = mode
        self.extension = extension

        self.image = self.get_image()
        self.image_base64 = self.get_image_base64()

        self.download_image = download_image
        self.path = path
        self.prefix = prefix
        self.target_id = target_id

        self._validate()
        self.filename = self.get_filename()
        self.download()

    ## CHECK VALIDATE

    def _validate(self):
        """
        檢查
        若請求下載，必須包含 path, prefix, target_id 且 prefix 必須包含在 ['league', 'team', 'player', 'news']
        """
        if self.download_image:
            if not self.path:
                error_info = f' "path" is required if download image! '
                raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')
            if not self.prefix:
                error_info = f' "prefix" is required if download image! '
                raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')
            if not self.target_id:
                error_info = f' "target_id" is required if download image! '
                raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')
        if self.prefix.lower() not in self.PREFIX:
            error_info = f' INVALID FILENAME ATTRIBUTE: "{self.prefix}" '
            raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')

    ## PARSE method

    @classmethod
    def _parse_extension(cls, extension):
        '''
        convert extension
        '''
        extension = str(extension)
        extension = extension.lower()
        extension = extension.lstrip('.')
        return cls.EXTENSION_DICT.get(f'.{extension}', None)

    ## CONVERT method

    @classmethod
    def _convert_mode(cls, image, extension):
        """
        Returns PIL image object with specific mode.
        :image: The requested PIL image object.
        :mode: An optional parameter. This can be one of
            ['L', 'P', ,'RGBX', ,'RGBA', ,'CMYK', 'I;16', ,'I;16L', ,'I;16B']
            and the default value is 'RGBA'
        :returns: An :class:'~PIL.Image.Image' object.
        """
        extension = cls._parse_extension(extension=extension)

        if not extension:
            image
        if extension == 'JPEG':
            mode = 'RGB'
        elif extension == 'GIF' or extension == 'PNG':
            mode = 'RGBA'
        else:
            mode = 'L'

        if image.mode != mode:
            return image.convert(mode)
        return image

    @staticmethod
    def convert_base64_to_content(image_base64):
        """
        convert BASE64 into bytes
        """
        return base64.b64decode(image_base64)

    @staticmethod
    def convert_content_to_base64(image_content):
        """
        convert bytes into a BASE64 BLOB string
        """
        return base64.b64encode(image_content)

    @classmethod
    def convert_content_to_image(cls, image_content, extension):
        """
        convert bytes into PIL image object.
        The mode can be one of
        ['L', 'P', ,'RGBX', ,'RGBA', ,'CMYK', 'I;16', ,'I;16L', ,'I;16B']
        """
        image = Image.open(BytesIO(image_content))
        return cls._convert_mode(image=image, extension=extension)

    def convert_image_to_content(self):
        """
        convert PIL image object into bytes
        """
        extension = self._parse_extension(extension=self.extension)
        if not extension:
            error_info = f' UNSUPPORTED EXTENSION: {self.extension} '
            raise Exception(f'\n{error_info:-^{self.SCREEN_WIDTH}}')
        canvas = BytesIO()
        self.image.save(canvas, format=extension)
        image_bytes = canvas.getvalue()
        return image_bytes

    ## GET method

    def get_image_base64(self):
        image_content = self.convert_image_to_content()
        return self.convert_content_to_base64(image_content=image_content)

    def get_filename(self):
        filename = ImagePathProcessor.get_filename(
            prefix=self.prefix.lower(),
            target_id=self.target_id,
            extension=self.extension
        )
        return filename

    def get_image(self):
        return self.convert_content_to_image(image_content=self.image_content, extension=self.extension)

    ## ACTIONS

    @staticmethod
    def save_image(image, path, filename):
        """
        save PIL image object as a file
        """
        try:
            image.save(os.path.join(path, filename))
            return True
        except Exception as e:
            DebugTool.error(e, msg=f'path: {path} | filename: {filename}')
            return False

    def download(self):
        if not self.download_image:
            return False
        return self.save_image(image=self.image, path=self.path, filename=self.filename)

    @classmethod
    def export(cls, image_base64, extension, path, filename):
        image_content = cls.convert_base64_to_content(image_base64=image_base64)
        image = cls.convert_content_to_image(image_content=image_content, extension=extension)
        return cls.save_image(image=image, path=path, filename=filename)

