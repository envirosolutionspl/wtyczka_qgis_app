def urlIdToGmlId(uri):
    identyf = '/'.join(uri.split('https://www.gov.pl/static/zagospodarowanieprzestrzenne/app/')[-1].split('/')[1:])
    return identyf.replace('/', '_')