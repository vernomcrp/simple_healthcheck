import os
import sys
import urllib2

SERVICES = {
    'service': {
        'url': 'http://example.com/9999',
        'checkphrase': [
            '2.0'
        ]
    },
    'sanook website': {
        'url': 'http://www.sanook.com',
        'checkphrase': [
            'sanook'
        ]
    },
}

TIMEOUT = 10

def do_check(services=SERVICES):
    for service, config in services.items():
        url = config.get('url', None)
        if url:
            print 'Begin connect service : ', service
            request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                raw = urllib2.urlopen(request, timeout=TIMEOUT)
            except urllib2.URLError:
                print '---> (URLError) Timeout Exception %d seconds' % TIMEOUT
                continue
            except Exception as e:
                print '---> Unknown Error', e
                continue

            if raw.getcode() != 200:
                print '---> Connection Error %d' % raw.getcode()
                continue

            checkwords = config.get('checkphrase', [])
            if len(checkwords) > 0:
                print '-> Check word %s' % ','.join(checkwords)
                check_point = False
                content = raw.read()
                for word in checkwords:
                    if word in content:
                        check_point = True
                    else:
                        check_point = False
                        break
                if check_point:
                    print '-> Service : {} has a good health!'.format(service)
                else:
                    print '-> Service : {} does has a good health!!!'.format(service)
            else:
                print 'Not valid check words'

        else:
            print 'No endpoint provided'
                
def print_usage():
    print "Usage : python {} [all|<service_name>]".format(sys.argv[0])
    

if __name__=='__main__':
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(0)
    filter_service = sys.argv[1]
    if filter_service == 'all':
        do_check()
    elif filter_service in SERVICES.keys():
        do_check({filter_service: SERVICES.get(filter_service)})
    elif filter_service == 'list':
        print 'Valid Services : {}'.format(','.join(SERVICES.keys()))
    else:
        print_usage()
    sys.exit(0)
