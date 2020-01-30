#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This code example imports offline conversion values for specific clicks to
your account.

To get Google Click ID for a click, use the "click_view" resource:
https://developers.google.com/google-ads/api/fields/latest/click_view.
To set up a conversion action, run the AddConversionAction.php example."""


import argparse
import sys
import requests

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

def main(client,
         customer_id,
         conversion_action_id,
         gcl_id,
         conversion_time,
         conversion_value):
    """Main method, to run this code example as a standalone application.
    Creates a click conversion with a default currency of USD.

    Args:
      client: The Google Ads Client
      customer_id: TODO
      conversion_action_id:
      gcl_id:
      conversion_time:
      conversion_value:
    """

    click_conversion = client.get_type('ClickConversion', version='v2')
    conversion_action_service = client.get_service('ConversionActionService',
                                                   version='v2')
    click_conversion.conversion_action.value = (
        conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id)
    )
    click_conversion.gclid.value = gcl_id
    click_conversion.conversion_value.value = float(conversion_value)
    click_conversion.conversion_date_time.value = conversion_time
    click_conversion.currency_code.value = 'USD'

    conversion_upload_service = client.get_service('ConversionUploadService',
                                                   version='v2')

    try:
        conversion_upload_response = (
            conversion_upload_service.upload_click_conversions(customer_id,
                                        [click_conversion])
        )
        uploaded_click_conversion = (conversion_upload_response.results[0]
                                     .click_conversion_result)
        print(f'Uploaded conversion that occurred at '
              f'''{uploaded_click_conversion.conversion_date_time}'' '
              f'from Google Click ID ''{uploaded_click_conversion.gclid}'' '
              f'to ''{uploaded_click_conversion.conversion_action}''')

    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Upload an offline conversion.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--conversion_action_id', type=str,
                        required=True, help='The conversion action ID.')
    parser.add_argument('-g', '--gcl_id', type=str,
                        required=True, help='The Google Click Identifier ID.')
    parser.add_argument('-t', '--conversion_time', type=str,
                        required=True, help='The conversion time.')
    parser.add_argument('-v', '--conversion_value', type=str,
                        required=True, help='The conversion value.')
    args = parser.parse_args()

    main(google_ads_client, 
         args.customer_id,
         args.conversion_action_id,
         args.gcl_id,
         args.conversion_time,
         args.conversion_value)