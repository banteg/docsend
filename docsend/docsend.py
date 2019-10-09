from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image
from requests_html import HTMLSession


class DocSend:

    def __init__(self, doc_id):
        self.doc_id = doc_id.rpartition('/')[-1]
        self.url = f'https://docsend.com/view/{doc_id}'
        self.s = HTMLSession()

    def fetch_meta(self):
        r = self.s.get(self.url)
        r.raise_for_status()
        self.auth_token = None
        if r.html.find('input[@name="authenticity_token"]'):
            self.auth_token = r.html.find('input[@name="authenticity_token"]')[0].attrs['value']
        self.pages = int(r.html.find('.document-thumb-container')[-1].attrs['data-page-num'])

    def authorize(self, email, passcode=None):
        form = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.auth_token,
            'link_auth_form[email]': email,
            'link_auth_form[passcode]': passcode,
            'commit': 'Continue',
        }
        f = self.s.post(self.url, data=form)
        f.raise_for_status()

    def fetch_images(self):
        self.image_urls = []
        pool = ThreadPoolExecutor(self.pages)
        self.images = list(pool.map(self._fetch_image, range(1, self.pages + 1)))

    def _fetch_image(self, page):
        meta = self.s.get(f'{self.url}/page_data/{page}')
        meta.raise_for_status()
        data = self.s.get(meta.json()['imageUrl'])
        data.raise_for_status()
        rgba = Image.open(BytesIO(data.content))
        rgb = Image.new('RGB', rgba.size, (255, 255, 255))
        rgb.paste(rgba)
        return rgb

    def save_pdf(self, name=None):
        self.images[0].save(
            name,
            format='PDF',
            append_images=self.images[1:],
            save_all=True
        )

    def save_images(self, name):
        path = Path(name)
        path.mkdir(exist_ok=True)
        for page, image in enumerate(self.images, start=1):
            image.save(path / f'{page}.png', format='PNG')
