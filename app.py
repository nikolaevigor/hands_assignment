import re
import requests
import threading
import queue
import sys
import time

_SITES = ['https://repetitors.info', 'https://hands.ru/company/about/']
_IDLE_PERIOD = 1

_processing_queue = queue.Queue()

def _format_phone(phone):
    return phone.replace(' ', '').replace('-', '').replace('+7', '8').replace('(', '').replace(')', '')


def _request_html(site):
    try:
        print(f'Requesting {site}')
        page_text = requests.get(site, timeout=(3.0, 5.0)).text
    except requests.exceptions.Timeout:
        print(f'Timeout for {site}')
    else:
        print(f'Put {site} in queue')
        _processing_queue.put((site, page_text))

def _process_pages():
    while True:
        try:
            site, page_text = _processing_queue.get(block=True, timeout=_IDLE_PERIOD)
        except queue.Empty:
            print(f'No items for {_IDLE_PERIOD} sec(s).\nExiting')
            sys.exit(0)
        results = re.findall('((\+7|8)(-|\s{1})\({0,1}\d{3}\){0,1}(-|\s{1})\d{3}(-|\s{1})\d{2}(-|\s{1})\d{2})', page_text)
        if results:
            results = [_format_phone(r[0]) for r in results]
            print(f'Found {results} for {site}')
            # check if actual; interact with another services, etc.
        else:
            print(f'Phones not found for {site}')
    

if __name__ == '__main__':
    for site in _SITES:
        thread = threading.Thread(target=_request_html, name=site, args=(site, ))
        thread.start()

    try:
        _process_pages()
    except KeyboardInterrupt:
        print('\nExiting')
        sys.exit(0)

        