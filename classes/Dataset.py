from typing import Dict, List, Union

class Resource:
    def __init__(self, fileName: str = None, fileType: str = None, assetUrl: str = None, 
                 fileSize: str = None, fileSizeUnit: str = None, dateCreated: str = None, 
                 dateUpdated: str = None, numRecords: int = None):
        self.fileName = fileName
        self.fileType = fileType
        self.assetUrl = assetUrl
        self.fileSize = fileSize
        self.fileSizeUnit = fileSizeUnit
        self.dateCreated = dateCreated
        self.dateUpdated = dateUpdated
        self.numRecords = numRecords

    def to_dict(self):
            resource_dict = {
                "fileName": self.fileName,
                "fileType": self.fileType,
                "assetUrl": self.assetUrl,
            }
            if self.fileSize is not None:
                resource_dict["fileSize"] = self.fileSize
            if self.fileSizeUnit is not None:
                resource_dict["fileSizeUnit"] = self.fileSizeUnit
            if self.dateCreated is not None:
                resource_dict["dateCreated"] = self.dateCreated
            if self.dateUpdated is not None:
                resource_dict["dateUpdated"] = self.dateUpdated
            if self.numRecords is not None:
                resource_dict["numRecords"] = self.numRecords
            return resource_dict

class Dataset:
    def __init__(self, title: str = None, owner: str = None, pageURL: str = None,
                 dateCreated: str = None, dateUpdated: str = None, license: str = None,
                 description: str = None, tags: List[str] = None, resources: List[Resource] = None):
        self.title = title
        self.owner = owner
        self.pageURL = pageURL
        self.dateCreated = dateCreated
        self.dateUpdated = dateUpdated
        self.license = license
        self.description = description
        self.tags = tags or []
        self.resources = resources

    
    def to_dict(self):
        return {
            'title': self.title,
            'owner': self.owner,
            'pageURL': self.pageURL,
            'dateCreated': self.dateCreated,
            'dateUpdated': self.dateUpdated,
            'license': self.license,
            'description': self.description,
            'tags': self.tags,
            'resources': [r.__dict__ for r in self.resources] if self.resources is not None else None
        }