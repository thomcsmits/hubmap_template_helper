from csv import DictReader, excel_tab
from io import StringIO
import requests
import pandas as pd


def get_all_uuids(
        metadata_url='https://portal.hubmapconsortium.org/metadata/v0/datasets.tsv'):
    '''
    Retrieve a dictionary mapping uuids to hubmap ids.

    Parameters
    ----------
    uuids : list
        list with uuids

    Returns
    -------
    dictionary mapping uuids to hubmap ids
    '''
    # Fetch metadata, and read it into list
    response = requests.get(metadata_url)
    metadata = list(DictReader(StringIO(response.text), dialect=excel_tab))

    # The first item are the column headers, so remove these
    all_uuids = [hit['uuid'] for hit in metadata[1:]]

    return all_uuids


def get_uuid_to_hubmap_mapping(
        uuids,
        metadata_url='https://portal.hubmapconsortium.org/metadata/v0/datasets.tsv'):
    '''
    Retrieve a dictionary mapping uuids to hubmap ids.

    Parameters
    ----------
    uuids : list
        list with uuids
    metadata_url : string, optional
        URL for HuBMAP Data Portal metadata file

    Returns
    -------
    dictionary mapping uuids to hubmap ids
    '''
    # Fetch metadata, and read it into a dataframe
    response = requests.post(
        metadata_url, json={"uuids": uuids}
    )
    metadata = list(DictReader(StringIO(response.text), dialect=excel_tab))
    metadata = pd.DataFrame(metadata[1:])

    # Create mapping from uuid to hubmap id
    uuid_to_hubmap = dict(zip(metadata['uuid'], metadata['hubmap_id']))
    return uuid_to_hubmap
