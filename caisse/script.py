import requests
import json

api_manager_url = 'http://localhost:8001/'
api_services_url = 'http://localhost:8000/'


# Add a default route named same as the service name

def unregister(service_name):
    print(" [x] Trying to delete the service name %r" % service_name)
    try:
        delete_route(service_name)
        r = requests.delete(api_manager_url + 'services/' + service_name)
        if r.status_code == 400:
            print(r.text)
            print(" [x] First delete the routes associated.\nUse the function 'delete_route(route_name)'")
            return
    except requests.exceptions.RequestException as err:
        print(err)
    print(" [x] Successfully deleted the service name %r" % service_name)

def delete_route(route_name):
    print(" [x] Trying to delete the route %r" % route_name)
    try:
        id = get_id_from_route(route_name)
        if id == '':
            print(' [x] Route not found')
            return
        else:
            r = requests.delete(api_manager_url + 'routes/' + id)
    except requests.exceptions.RequestException as err:
        print(err)
    print(" [x] Successfully deleted the route %r" % route_name)



def get_service(host):
    print(" [x] Trying to get service with this host %r " % host)
    headers = {'Host': host}
    r = requests.get(api_services_url, headers=headers)
    print(r.status_code)
    print(r.text)


def send_request(host, url):
    print(" [x] Trying to send request to host %r " % host)
    headers = {'Host': host}
    r = requests.get(api_services_url + url, headers=headers)
    print(r.status_code)
    print(r.text)
    return r.text


def post_request(host, url, body):
    print(" [x] Trying to send Get request to host %r " % host)
    headers = {'Host': host}
    r = requests.post(api_services_url + url, headers=headers, data=body)
    if r.status_code == 200:
        print(" [x] Post request successfully sent to host %r " % host)
    else:
        print(" [x] Post request FAILED exited with error code: " % r.status_code)
    return r.status_code


def get_all_routes():
    r = requests.get(api_manager_url + 'routes/')
    routes = json.loads(r.text)
    for route in routes['data']:
        print('Id : %r' % route['id'])
        for host in route['hosts']:
            print('Host: %r' % host)


def get_id_from_route(route_name):
    r = requests.get(api_manager_url + 'routes/')
    routes = json.loads(r.text)
    id = ''
    for route in routes['data']:
        found = 0
        for host in route['hosts']:
            if host == route_name:
                found = 1
        if found == 1:
            id = route['id']
    return id


def get_id_from_service(service_name):
    r = requests.get(api_manager_url + 'routes/')
    routes = json.loads(r.text)
    id = ''
    for route in routes['data']:
        found = 0
        for host in route['hosts']:
            if host == service_name:
                found = 1
        if found == 1:
            id = route['id']
    return id


def add_auth_key_plugin(service_name):
    print(" [x] Trying to add auth-key plugin to service %r" % service_name)
    try:
        payload = {'name': 'key-auth'}
        r = requests.post(api_manager_url + 'services/' + service_name + '/plugins/', data=payload)
        if r.status_code == 404:
            print(" [x] Service name %r not found" % service_name)
            return
    except requests.exceptions.RequestException as err:
        print(err)
    print(" [x] Successfully added auth-key to the service name %r" % service_name)


def add_consumer(consumer_name):
    print(" [x] Trying to add consumer %r" % consumer_name)
    try:
        payload = {'username': consumer_name}
        r = requests.post(api_manager_url + 'consumers/', data=payload)
    except requests.exceptions.RequestException as err:
        print(err)
    print(" [x] Successfully added auth-key to the service name %r" % consumer_name)

# Don't forget to start kong service
if __name__ == '__main__':
    # register('http://mockbin.org', 'test-service3')
    # add_route('test-service3', 'test-example.com')
    # add_auth_key_plugin('test-service3')
    # delete_service_with_route("test-example.com")
    # get_service('test-example.com')
    # get_all_routes()
    # delete_route('test-example.com')
    # delete_service('test-service3')
    unregister('magasin_test')
    unregister('caisse')