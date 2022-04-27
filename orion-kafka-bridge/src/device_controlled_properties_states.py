"""
The trend data tuple has two fields "electricCharge" and "electricCurrent" which are updated independently.
When one field is updated (numerical value from the "value" field),
the other field will be equal to the field from the previous update.
It is necessary to store the state in order not to write the same value repeatedly,
which was sent but does not apply to updating this value.

Example of data:

"controlledProperty": {
    "type": "Property",
    "value": [
        "electricCharge",
        "electricCurrent"
      ]
},
"value": {
    "type": "Property",
    "value": [
        "0.34534",
        "5.434",
    ],
    "observedAt": "2020-12-01T11:23:19Z"
},
"""


class ControlledPropertyState:
    _old_value: float = None
    _new_value: float = None

    def is_updated(self, value: float) -> bool:
        self.update_value(value=value)
        return self._old_value != self._new_value

    def update_value(self, value: float) -> None:
        self._old_value, self._new_value = self._new_value, value


electric_current_state = ControlledPropertyState()
electric_charge_state = ControlledPropertyState()
