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

    for page in range(1, (total_pages+1)):
        querystring['page'] = page 
        response = requests.get(URL, params=querystring)
        data = response.json()
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
                for item in admin_hierarchy:
                    # get the region
                    region = item['region']
                    region_code = item['region_code']
                    if (region != None) and (region_code != None):
                        r, created = Location.objects.update_or_create(
                            location_name=region,
                            location_level=1,
                            location_hfr_code=region_code,
                            location_reference=country_reference.id)
                        r.save()
                        print(f'Region: {r.location_name} added with id: {r.id}')
                        for c in admin_hierarchy:
                            # get the councils
                            if c['region'] == region:
                                council = c['council']
                                council_hrf_code = c['council_code']
                                if (council != None) and (council_hrf_code != None):
                                    c, created = Location.objects.update_or_create(
                                        location_name=council,
                                        location_hfr_code=council_hrf_code,
                                        location_level=2,
                                        location_reference=r.id)
                                    c.save()
                                    if created:
                                        print(f'Council: {c.location_name} added with id: {c.id}')

        print('Done insertng Country, Region, Council')

if __name__ == '__main__':
    print('API Service Started')
    add_all_locations()
