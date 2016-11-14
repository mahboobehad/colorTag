# python 2.7
import unirest
import argparse
import re
import os
import json
import logging

logging.basicConfig(filename='request.log', level=logging.INFO)


def post(image, sort_type, palette):
    '''

    :param image: image path for sending to colorTag API.
    :param sort_type: supported sort types : relevance and weight.
    :param palette: supported palettes : simple, w3c and precise.
    :return: response body in json format.

    '''

    # replace key value after 500 requests.

    key = ""

    unirest.clear_default_headers()

    response = unirest.post("https://apicloud-colortag.p.mashape.com/tag-file.json",
                            headers=
                            {
                                "X-Mashape-Key": key
                            },
                            params=
                            {
                                "image": open(image, mode="r"),
                                "palette": palette,
                                "sort": sort_type
                            }
                            )

    logging.info('resoponse code for image: ' + str(image) + ' is: ' + str(response.code))

    return response.raw_body


def check_file_type(file_name):
    '''

    :param file_name: the file name to be check  whether  is image or not.
    :return: return True if file is valid image type, False otherwise.

    '''

    pattern = re.compile('([-\w]+\.(?:jpg|gif|png))')
    match = pattern.match(file_name)

    if match:
        return True

    return False


def send_request(images, args):

    '''
    for each image file send request to API and log the result in a text file with same name.
    :param images: list of files in directory.
    :return: None
    '''

    for i, img in enumerate(images):

        if check_file_type(img):
            file_name = str(img).split('.')[0]
            result = post(args.path + os.sep + img, args.sort_type, args.palette)

            with open(str(file_name) + '.txt', 'w') as output:
                json.dump(result, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('sort_type')
    parser.add_argument('palette')

    args = parser.parse_args()

    images = os.listdir(args.path)

    send_request(images, args)
