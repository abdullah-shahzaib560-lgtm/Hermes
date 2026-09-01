## Fundamental lifecycle

### Define the Hermes data lifecycle
> The data lifecycle of hermes should be clear, it should go from fetching to serving with minimal effort from the user perspective, and run most the complexity internally, the data must go from fetching/ingesting (getting the data from internal or external sources into hermes i.e. one can even get the external data like from an API to hermes or ingest already have data like data.json), parsing (the data should be easy to understand after using the parsing engine like resolving the nested/ugly json making good), normalization (the parsed data will be normalized and putted in the hermes respresentation of data), validation (the data will be validated that are there any missing values, outliers, etc so that further application can be implmented) and then storing it in the DataSet(), it is a representation and reference of the data it will not contain the entire data itself, it will have the reference of the data means where the data lives, so that you can call that data on demand rather then actually putting it in-memory rather from the start, and it will have the data lineage, provenance, metadata, schema, name, UUID and its version

### Define the internal representation shared by all ingestion paths
> 

### Ensure API sources and file sources converge into the same internal representation
> 

### Define Dataset as the central abstraction
> 

### Define clear boundaries between Core and domain packages
> 

### Define extension interfaces for connectors, parsers, schemas, validators, transforms, resolvers and storage
> 