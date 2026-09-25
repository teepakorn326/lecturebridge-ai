from .adapters import AdapterFactory
from .domain import (
    CanonicalDocument,
    SourceFile,
)


class IngestionService:
    def ingest(
        self,
        source: SourceFile,
    ) -> CanonicalDocument:

        adapter = AdapterFactory.get_adapter(source)

        document = adapter.parse(source)

        return document
