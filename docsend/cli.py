import click

from docsend import DocSend


@click.command()
@click.argument('doc_id')
@click.option('-e', '--email', default=None, help='Email to authorize with')
@click.option('-f', '--format', type=click.Choice(['pdf', 'png']), default='pdf', help='Save as PDF (default) or image sequence')
@click.option('-o', '--output', default=None, help='Output file name')
def main(doc_id, email, format, output):
    ds = DocSend(doc_id)
    ds.fetch_meta()
    if email:
        ds.authorize(email)
    ds.fetch_image_meta()
    ds.fetch_images()
    if output is None:
        output = f'docsend_{doc_id}.pdf' if format == 'pdf' else f'docsend_{doc_id}'
    if format == 'pdf':
        ds.save_pdf(output)
    elif format == 'png':
        ds.save_images(output)
    print(f'saved to {output}')


if __name__ == '__main__':
    main()
