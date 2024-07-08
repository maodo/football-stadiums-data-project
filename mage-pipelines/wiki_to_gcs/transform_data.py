if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import re
from geopy import Nominatim

def handle_capacity(text):
    cleaned = re.sub("[\(\[].*?[\)\]]", "", text)
    cleaned_text = cleaned.replace(",","")
    return cleaned_text

def get_geo_loc(stadium, city):
    geolocator = Nominatim(user_agent='football')
    location = geolocator.geocode(f'{stadium}, {city}')
    if location:
        return location.latitude, location.longitude
    return None

def transform_data(data: pd.DataFrame):
    data['capacity'] = data['capacity'].apply(lambda x: handle_capacity(x))
    data['city'] = data['city'].apply(lambda x: x.strip())
    data['country'] = data['country'].apply(lambda x: x.strip())
    data['home_team'] = data['home_team'].apply(lambda x: x.strip())
    data['stadium'] = data['stadium'].apply(lambda x: x.replace("♦","").strip())
    data['capacity'] = data['capacity'].astype(int)
    data['description'] = data['description'].apply(lambda x: re.sub("[\(\[].*?[\)\]]", "", x))
    data['description'] = data['description'].apply(lambda x: x.replace('\n',' ').strip())
    data['location'] = data.apply(lambda x: get_geo_loc(x['stadium'],x['city']), axis=1 )
    # Let's handle empty locations
    rows_with_empty_locations = data[data.duplicated(['location'])]
    rows_with_empty_locations['location'] = rows_with_empty_locations.apply(lambda x : get_geo_loc(x['city'],x['country']), axis=1)
    data.update(rows_with_empty_locations)
    # Let's handle the remaining rows with None locations
    rows_with_none_locations = data[data.duplicated(['location'])]
    rows_with_none_locations['location'] = rows_with_none_locations.apply(lambda x : get_geo_loc(x['stadium'],x['country']), axis=1)
    data.update(rows_with_none_locations)
    return data

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    transformed_data = transform_data(data)

    return transformed_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
