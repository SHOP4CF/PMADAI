# Alert Data model

## Common properties of alerts

- category - constant value "predictiveMaintenance"
- dateIssued - timestamp identifying when an alert was created
- dateModified – timestamp identifying when an alert was modified
    (initially equal to dateIssued)
- humanVerified – indication that an alert was verified by human (two
    possible values: true/false) (optional)
- id - unique ID of an alert
- location - where an alert happened (optional - probably not needed)
- seeAlso - URL in PMADAI component
- severity - indication of importance of an alert (optional), allowed
    values: (informational, low, medium, high, critical)
- source - source of data describing alert - in our case component
    generating the alert - constant value "PMADAI" (or an URI)
- validFrom - timestamp equal dateIssued
- type - NGSI type - constant value: "Alert"

## Properties specific for "incorrectPaintingProcessInKTL" alert

Alert issued when an incorrect painting process in the KTL area is
detected.

- alertSource - unique ID of painted car body (it allows to identify
    skid and pendulum)
- description - detailed textual description of the problem includes
    all identifiers Skid ID, Pendulum ID, Car body ID, Car body TYPE,
    Voltage program TYPE, and additional information like time of
    entering the KTL process.
- subcategory - sub-category of alert: "incorrectPaintingProcessInKTL"

## Properties specific for "incorrectPaintingData" alert

Alert issued when data describing painting process are incorrect.

- alertSource - unique ID of painted car body (it allows to identify
    skid and pendulum)
- description - detailed textual description of the problem includes
    all identifiers Skid ID, Pendulum ID, Car body ID, Car body TYPE,
    Voltage program TYPE, and additional information like time of
    entering the KTL process.
- subcategory - sub-category of alert: "incorrectPaintingData"

## Properties specific for "skidMaintanance" alert

Alert issued when a maintenance action for a skid is suggested.

- alertSource - unique ID of skid
- description - detailed textual description: skid ID and description
    of suggested maintenance action
- subcategory - sub-category of alert: "skidMaintenance"

## Example

```
{
    "id": "urn:ngsi-ld:Alert:company-xyz:pred-maint-3x29md89",
    "type": "Alert",
    "category": {
        "type": "Property",
        "value": "predictiveMaintenance"
    },
    "subCategory": {
        "type": "Property",
        "value": "incorrectPaintingProcessInKTL"
    },
    "description": {
        "type": "Property",
        "value": "Skid no. 12345 needs maintenance"
    },
    "dateIssued": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2017-01-02T09:25:55.00Z"
        }
    },
    "alertSource": {
        "type": "Relationship",
        "object": "urn:ngsi-ld:Asset:skid-12345"
    },
    "source": {
        "type": "Property",
        "value": "PMADAI"
    },
    "validFrom": {
        "type": "Property",
        "value": {
            "@type": "DateTime",
            "@value": "2017-01-02T09:25:55.00Z"
        }
    },
    "severity": {
        "type": "Property",
        "value": "high"
    },
    "humanVerified": {
        "type": "Property",
        "value": false
    },
    "@context": [
        "https://smartdatamodels.org/context.jsonld"
    ]
}
```
