# Ingestion Process

## Fetching Raw Data

[Implementation details](../reference/vulsy/vulnerability_pipeline/ingestion/ingest/)

We retrieve the initial list from various sources. The following types of sources are recognized when fetching this initial list:

* **Endpoint with Pagination**: Allows specifying the index of the last fetched item so we can continue from where we left off.
* **Complete Feed Endpoint**: Provides all item links or a limited number of items based on date or size, we need to loop over all items.

Endpoints possess the following characteristics:

* They provide a response which contains links to actual items rather than the full data in the response. (Sometimes they also contain the full data while also linking to actual items)
    * This can be: JSON, HTML, XML, CSV, etc...
* They provide a response that does not link to actual items but includes them within the body of the response.


### The process

####Initial list fetching

```mermaid
flowchart TD
    A[Start] --> B{Source Supports Continuation?}
    
    B -->|Yes| C[Fetch from Last Position]
    B -->|No| D[Fetch Source Data]
    
    C --> E{Contains Item Links?}
    D --> E
    
    E -->|Yes| F[Extract Item URLs]
    E -->|No| G[Use Source Data as Items]
    
    F --> H[List of Items to Process]
    G --> H
```

####Processing Items time based

```mermaid
flowchart TD
    A[List of Items] --> B{Has More Items?}
    B -->|No| D[Record Success or Failure]
    B -->|Yes| G{Item exists for datetime hash?}
    G -->|Yes| B
    G -->|No| H[Fetch Item Data]
    H --> I[Store Item]
    I --> B
```

####Processing Items data based

```mermaid
flowchart TD
    A[List of Items] --> B{Has More Items?}
    B -->|No| D[Record Success or Failure]
    B -->|Yes| E[Fetch Item Data]
    E --> F[Create Data Hash]
    F --> G{Item exists for hash?}
    G -->|Yes| B
    G -->|No| H[Store Item]
    H --> B
```




