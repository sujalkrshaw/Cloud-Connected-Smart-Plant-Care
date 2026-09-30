# Test Plan

| ID | Scenario | Input | Expected Result | Automated |
|---|---|---|---|---|
| T01 | Simulator starts | Python command | Sensor loop starts | Manual |
| T02 | Reading generated | Virtual state | 0–100% moisture etc. | Manual |
| T03 | Valid data | POST valid JSON | HTTP 200 accepted | Yes |
| T04 | Invalid data | Moisture 120 | HTTP 422 | Yes |
| T05 | Data stored | Valid reading | Row appears in history | Yes |
| T06 | Latest reading | GET latest | Most recent reading returned | Yes |
| T07 | History | GET history | Ordered readings returned | Yes |
| T08 | Above threshold | 55% vs 40% | No auto watering | Manual |
| T09 | Below threshold | 25% vs 40% | Auto watering starts | Yes |
| T10 | Pump starts | Dry reading | `pump_on=true` | Yes |
| T11 | Moisture increases | Simulator sees pump | Moisture rises | Manual |
| T12 | Pump stops | Restored moisture/time | Pump becomes OFF | Manual |
| T13 | Cooldown | Rapid repeated dry readings | No repeated rapid event | Logic |
| T14 | Manual watering | POST water | Command accepted | Manual |
| T15 | Alert | Low moisture | Alert stored | Logic |
| T16 | Acknowledge | PUT alert | Status acknowledged | Manual |
| T17 | Offline | Stop simulator | Device becomes offline after timeout | Manual |
| T18 | Dashboard | API available | Current cards render | Manual |
| T19 | Chart | History exists | Trend chart renders | Manual |
| T20 | DB failure | Stop DB | API returns error / service unavailable | Manual |
| T21 | API failure | Stop API | Simulator logs failure | Manual |
| T22 | Retry | Temporary API outage | Next simulator cycle retries | Manual |
| T23 | Unauthorized | Missing API key | HTTP 401 | Yes |
| T24 | Threshold | PUT 35 | Threshold updates | Yes |
| T25 | Multiple devices | Register second device | Independent device data | Manual |
