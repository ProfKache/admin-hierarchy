import math
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from location.models import Location
import requests
from django.shortcuts import render, get_object_or_404

URL = os.getenv('URL')


querystring = {
    "r": "site/admin-hierarchy",
    "reqToken": os.getenv('reqToken'),
    "nodeId": "all",
    "pageSize": 1000,
    "page": 1
}


def add_all_locations():
    response = requests.get(URL, params=querystring)
    data = response.json()
    total_count = data['Count']
    admin_hierarchy = data['AdminHierarchy']
    page_size = querystring.get('pageSize')

    # calculate the ending loop to get the total pages
    total_pages = math.ceil(total_count / page_size)
    print("page size is:", total_pages)

    for page in range(1, (total_pages+1)):
        querystring['page'] = page 
        print("this is page number:" , querystring['page'])
        page_response = requests.get(URL, params=querystring)
        print(page_response)
        data = page_response.json()
        admin_hierarchy = data['AdminHierarchy']
        if admin_hierarchy:
            for item in admin_hierarchy:
                # get the country
                country = item['country']
                country_code = item['country_code']

                c, created = Location.objects.update_or_create(
                    location_name=country,
                    location_code=country_code,
                    location_reference='0'
                )
                c.save()
            country_reference = get_object_or_404(Location, location_name='Tanzania')

            if country_reference:
                regions = []
                for item in admin_hierarchy:
                    # get the region
                    if (item['region'] != None) and (item['region_code'] != None):
                        print("Region creation hitted")
                        region, created = Location.objects.update_or_create(
                            location_name = item['region'],
                            location_level = 1,
                            location_hfr_code = item['region_code'],
                            location_reference = country_reference.id)
                        region.save()
                        if region:
                            if (item['council'] != None) and (item['council_code'] != None):
                                print("The point of creation hitted too")
                                council, council_created = Location.objects.update_or_create(
                                location_name = item['council'],
                                location_hfr_code = item['council_code'],
                                location_level = 2,
                                location_reference = region.id)
                                council.save()
                                if council:
                                    print("The final creation done too")
                                    print(f'Council: {council.location_name} added with id: {council.id}')
                            print(f'Region: {region.location_name} added with id: {region.id}')
                        else:
                            print("Region not Created")

        print('Done insertng Country, Region, Council')

if __name__ == '__main__':
    print('API Service Started')
    add_all_locations()
