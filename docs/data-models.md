# Data models

## Work statuses (metadata) data model

This model uses [FIWARE Task](https://shop4cf.github.io/data-models/task.html).

### Example

```
{
    "id": "urn:ngsi-ld:Task:company-xyz:im834wyoen78w37",
    "type": "Task",
    "isDefinedBy": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:TaskDefinition:company-xyz:skid-in-the-pool"
    },
    "workParameters": {
        "type": "Property",
        "value": {
        "skidId": 88,
        "pendulumId": 57,
        "carBodyId"": 123,
        "carBodyType": "CG32",
        "voltageProgramType": 8
        } 
    },
    "status": {
        "type": "Property",
        "value": "inProgress",
        "observedAt": "2020-12-01T11:23:19Z"
    },
    "@context": [
        "https://smartdatamodels.org/context.jsonld",
        "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld"
    ]
}
```

Status values: `pending`, `assigned`, `inProgress`, `completed`, `paused`, `suspended`, `failed`.

Status changes to `inProgress` – skid enters the pool. Status changes to `completed` – skid leaves the pool.

`ObservedAt` is the timestamp of the status change.

## Measurements data model

This model uses [FIWARE Device](https://github.com/smart-data-models/dataModel.Device/blob/master/Device/doc/spec.md).

### Example

```
{
    "id": f"urn:ngsi-ld:Device:company-xyz:12345",
    "type": "Device",
    "source": {"type": "Relationship",
               "object": f"urn:ngsi-ld:Device:company-xyz:busbar-1"},
    "category": {"type": "Property",
                 "value": ["sensor"]},
    "controlledProperty": {"type": "Property",
                           "value": ["electricCurrent"]},
    "value": {"type": "Property",
              "value": 11.54,
              "observedAt": "2020-12-01T11:23:19Z},
    "@context": ["https://smartdatamodels.org/context.jsonld",
                 "https://raw.githubusercontent.com/shop4cf/data-models/master/docs/shop4cfcontext.jsonld"]
}
```
