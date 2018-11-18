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
        self.auth_token = r.html.find('input[@name="authenticity_token"]')[0].attrs['value']
        self.pages = int(r.html.find('.document-thumb-container')[-1].attrs['data-page-num'])

    def authorize(self, email):
        form = {
            'utf8': '✓',
            '_method': 'patch',
            'authenticity_token': self.auth_token,
            'link_auth_form[email]': email,
            'commit': 'Continue',
        }
        f = self.s.post(self.url, data=form)
        f.raise_for_status()

    def fetch_image_meta(self):
        self.image_urls = []
        for page in range(1, self.pages + 1):
            img = self.s.get(f'{self.url}/page_data/{page}')
            img.raise_for_status()
            self.image_urls.append(img.json()['imageUrl'])

    def fetch_images(self):
        self.images = []
        for url in self.image_urls:
            r = self.s.get(url)
            r.raise_for_status()
            self.images.append(Image.open(BytesIO(r.content)))

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
