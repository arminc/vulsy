"""Couchbase storage exceptions."""


class DocumentRetrievalError(Exception):
    """Exception raised for errors in the document retrieval process."""


class DocumentStorageError(Exception):
    """Exception raised for errors in the document storage process."""
