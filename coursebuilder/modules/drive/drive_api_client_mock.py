# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A fake version of the API client wrapper that won't use the network."""

__author__ = [
    'nretallack@google.com (Nick Retallack)',
]

from modules.drive import drive_api_client
from modules.drive import errors


class _APIClientWrapperMock(object):
    """Mimicks _APIClientWrapper but returns test data."""
    MOCK_FILES = [
        drive_api_client.DriveItem(
            '1', drive_api_client.DOC_TYPE, '1 Test Doc', 1),
        drive_api_client.DriveItem(
            '2', drive_api_client.SHEET_TYPE, '2 Test Sheet', 1),
        drive_api_client.DriveItem(
            '3', drive_api_client.SHEET_TYPE, '3 Another Test Sheet', 1),
        drive_api_client.DriveItem(
            '4', 'unknown', '4 Some Unknown File', 1),
        drive_api_client.DriveItem(
            '5', drive_api_client.DOC_TYPE, '5 Another Test Doc', 1),
        drive_api_client.DriveItem(
            '6', drive_api_client.SHEET_TYPE, '6 Synced Sheet', 1)
    ]

    SHARABLE_FILE = drive_api_client.DriveItem(
        '7', drive_api_client.DOC_TYPE, '7 Sharable Doc', 1)

    ERROR_FILE_ID = 'error'
    SHARE_PERMISSION_ERROR_FILE_ID = 'share-permission-error'
    SHARE_UNKNOWN_ERROR_FILE_ID = 'share-error'

    def list_file_meta(self):
        return drive_api_client.DriveItemList(self.MOCK_FILES)

    def get_file_meta(self, file_id):
        if file_id == self.ERROR_FILE_ID:
            raise errors.Error

        for item in self.MOCK_FILES:
            if item.key == file_id:
                return item

        raise errors.Error


    def get_sheet_data(self, file_id):
        meta = self.get_file_meta(file_id)
        if meta is None or meta.type != drive_api_client.SHEET_TYPE:
            raise errors.Error()
        return drive_api_client.Sheet(
            file_id=meta.key,
            title=meta.title,
            worksheets=[
                drive_api_client.Worksheet(
                    worksheet_id='1',
                    title='Main Worksheet',
                    cells=[
                        ['a', 'b', 'c'],
                        ['1', '2', '3'],
                    ]
                )
            ]
        )

    def get_doc_as_html(self, file_id):
        meta = self.get_file_meta(file_id)
        if meta is None or meta.type != drive_api_client.DOC_TYPE:
            raise errors.Error()

        return '<p>Some HTML</p>'

    def share_file(self, file_id, email):
        if self.SHARABLE_FILE not in self.MOCK_FILES:
            self.MOCK_FILES = self.MOCK_FILES.append(self.SHARABLE_FILE)
        elif file_id == self.SHARE_PERMISSION_ERROR_FILE_ID:
            raise errors.SharingPermissionError(errors.Error)
        elif file_id == self.SHARE_UNKNOWN_ERROR_FILE_ID:
            raise errors.Error