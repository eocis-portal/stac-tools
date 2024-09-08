# MIT License
#
# Copyright (c) 2023-2024 National Centre for Earth Observation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
from urllib.parse import urljoin

import argparse
import httpx
from httpx_auth import OAuth2ClientCredentials

API_URL=""

def get_collections(client):
    return client.get(
        urljoin(API_URL, f"collections")
    )

def add_collection(client,path):

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    response = client.post(
            urljoin(API_URL, f"collections"),
            json=data
        )

    print(response.content)

    return response.is_success

def remove_collection(client,path):

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    response = client.delete(
            urljoin(API_URL, f"collections/"+data["id"])
        )

    print(response.content)

    return response.is_success

def modify_collection(client,path):

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    response = client.put(
            urljoin(API_URL, f"collections/"+data["id"])
        )

    print(response.content)

    return response.is_success

def get_collection(client,collection_id):

    response = client.get(
            urljoin(API_URL, f"collections/"+collection_id)
        )

    print(response.content)

    return response.is_success

def add_items(client,item_paths):

    for path in item_paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        response = client.post(
            urljoin(API_URL, f"collections/{data['collection']}/items"),
            content=json.dumps(data)
        )

        print(response.content)
        if not response.is_success:
            return False

    return True

def get_items(client,collection_id):
    response = client.get(
        urljoin(API_URL, f"collections/{collection_id}/items"),
    )
    if response.is_success:
        return json.loads(response.content)["features"]
    else:
        print(response.content)
        return None

def remove_items(client,item_paths):
    for path in item_paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        response = client.delete(
                urljoin(API_URL, f"collections/"+{data['collection']}+"/items/"+data["id"])
            )

        print(response.content)

        if not response.is_success:
            return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--basicauth-username", default="")
    parser.add_argument("--basicauth-password", default="")
    parser.add_argument("--oauth2-tokenurl", default="")
    parser.add_argument("--oauth2-clientid", default="")
    parser.add_argument("--oauth2-clientsecret", default="")
    parser.add_argument("--add-collection")
    parser.add_argument("--modify-collection")
    parser.add_argument("--remove-collection")
    parser.add_argument("--get-collection")
    parser.add_argument("--get-items")
    parser.add_argument("--add-items", nargs="+")
    parser.add_argument("--remove-items", nargs="+")
    parser.add_argument("--list-collections", action="store_true")

    args = parser.parse_args()

    global API_URL
    API_URL = args.url

    if args.basicauth_username and args.basicauth_password:
        auth = httpx.BasicAuth(username=args.basicauth_username, password=args.basicauth_password)
    elif args.oauth2_tokenurl and args.oauth2_clientid and args.oauth2_clientsecret:
        print(f"tokenurl={args.oauth2_tokenurl}")
        print(f"client_id={args.oauth2_clientid}")
        print(f"client_secret={args.oauth2_clientsecret}")
        auth = OAuth2ClientCredentials(
            token_url=args.oauth2_tokenurl,
            client_id=args.oauth2_clientid,
            client_secret=args.oauth2_clientsecret
        )
    else:
        raise Exception("No authentication credentials supplied")

    client = httpx.Client(
        auth=auth,
        verify=False,
        timeout=180,
    )

    if args.remove_collection:
        remove_collection(client,args.remove_collection)

    if args.add_collection:
        add_collection(client,args.add_collection)

    if args.get_collection:
        get_collection(client,args.get_collection)

    if args.get_items:
        print(len(get_items(client,args.get_items)))

    if args.remove_items:
        add_items(client,args.remove_items)

    if args.add_items:
        result = add_items(client,args.add_items)
        if not result:
            print("add_items failed")

    if args.list_collections:
        response = get_collections(client)
        print(response.json())


if __name__ == "__main__":
    main()
