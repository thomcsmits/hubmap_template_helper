import warnings

import json
import requests


def check_template_compatibility(uuids, accepted_assay_display_names=None, required_filetypes=None,
                                 search_api='https://search.api.hubmapconsortium.org/v3/portal/search'):
    '''
    For a set of HuBMAP UUIDs, check if valid, and return valid UUIDs.
    Checks if UUIDs are present in the search API.
    If accepted_assay_display_names is defined, checks if UUIDs are of any of
        the assay_display_names in accepted_assay_display_names.
    If required_filetypes is defined, checks if UUIDs have all of the
        required filetypes in required_filetypes.

    Parameters
    ----------
    uuids : array of string
        HuBMAP UUIDs to be checked
    accepted_assay_display_names: array of string, optional
        accepted assay_display_names for template
    required_filetypes: array of string, optional
        required datatypes for template
    search_api: string, optional
        URL of search API

    Returns
    -------
    array of string
        valid UUIDs
    '''
    hits = json.loads(
        requests.post(
            search_api,
            json={
                'size': 10000,
                'query': {'ids': {'values': uuids}},
                '_source': ['files', 'assay_display_name']
            },
        ).text
    )['hits']['hits']

    # create mapping for uuid to file_types and data_types
    uuid_to_files = {}
    uuid_to_assay_display_names = {}
    for hit in hits:
        file_paths = [file['rel_path'] for file in hit['_source']['files']]
        uuid_to_files[hit['_id']] = file_paths

        hit_assay_display_name = hit['_source']['assay_display_name']
        uuid_to_assay_display_names[hit['_id']] = hit_assay_display_name

    # save uuids without warnings
    accepted_uuids = uuids.copy()

    # remove unvalid uuids
    for uuid in uuids:
        # check if all uuids are found in the search api
        if uuid not in uuid_to_files.keys():
            warnings.warn('Dataset with UUID "' + uuid + '" not found in Search API')
            accepted_uuids.remove(uuid)
            continue

        if required_filetypes is not None:
            # check if file_types for each uuid are in required_filetypes
            file_types = uuid_to_files[uuid]
            for required_file_type in required_filetypes:
                if required_file_type not in file_types:
                    warnings.warn('Dataset with UUID "' + uuid +
                                  '" does not have required file type: ' + required_file_type)
                    if uuid in accepted_uuids:
                        accepted_uuids.remove(uuid)

        if accepted_assay_display_names is not None:
            # check if data_types for each uuid are in accepted_datatypes
            assay_display_name = uuid_to_assay_display_names[uuid]
            for assay in assay_display_name:
                if assay not in accepted_assay_display_names:
                    warnings.warn('Dataset with UUID "' + uuid + '" has unaccepted data type: ' + assay)
                    if uuid in accepted_uuids:
                        accepted_uuids.remove(uuid)
                    continue

    return accepted_uuids
