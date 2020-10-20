import argparse
import logging
import sys
import time
import requests
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

ua = UserAgent(use_cache_server=False)

def get_event_ids(event_tag):
    url = f'https://app2.sli.do/api/v0.5/events?hash={event_tag}'
    re = requests.get(url)
    d = re.json()[0]
    return d['uuid']


def authenticate(event_uuid):
    url = f'https://app2.sli.do/api/v0.5/events/{event_uuid}/auth'
    re = requests.post(url, json={})
    logger.info(f'{re.status_code}, {re.text}')
    if re.status_code==200:
        token = re.json()['access_token']
        return f'Bearer {token}'
    else:
        return False


def vote(auth,question_id, event_uuid):
    url = f'https://app2.sli.do/api/v0.5/events/{event_uuid}/questions/{question_id}/like'
    re = requests.post(url, json={
        'score': 1
    }, headers={
        'User-Agent': ua.random,
        'Authorization': auth,
    })
    logger.info(f'{re.status_code}, {re.text}')
    return re.json()['event_question_score']


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('event_tag', type=str)
    parser.add_argument('question_id', type=int)
    parser.add_argument('votes', type=int)
    args = parser.parse_args()
    event_uuid = get_event_ids(args.event_tag)
    for i in range(args.votes):
        logger.info(f'vote #{i}')
        if(i==0):
            fourth = authenticate(event_uuid)
            third = authenticate(event_uuid)
            sec = authenticate(event_uuid)
            last = authenticate(event_uuid)
            time.sleep(1)
        vote(fourth,args.question_id, event_uuid)
        fourth = third
        third = sec
        sec = last
        last = authenticate(event_uuid)
        while last==False:
            last = authenticate(event_uuid)

if __name__ == '__main__':
    main()
