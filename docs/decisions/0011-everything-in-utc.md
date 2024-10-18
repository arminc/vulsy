# 11. Everything in UTC

Date: 2024-10-17

## Status

Accepted on 2024-10-17

## Context

In our application, we deal with data coming from various sources in different time zones.  We need a standardized approach to handle time across our entire system.

## Decision

We have decided to store and process all time-related data in Coordinated Universal Time (UTC) throughout our application. This means:

1. All timestamps in the database will be stored in UTC.
2. All server-side operations involving time will use UTC.
3. All APIs will accept and return time data in UTC.
4. Client-side applications will be responsible for converting UTC to local time for display purposes.

## Consequences

1. Simplified time zone management: By using UTC as a standard, we eliminate the complexity of dealing with multiple time zones in our backend systems.
2. Consistent data storage: All time-related data will be stored uniformly, making it easier to query, compare, and analyze.
3. Easier data migration and replication: UTC timestamps can be easily transferred between different systems without worrying about time zone conversions.
4. Simplified server-side logic: Calculations and comparisons involving time become straightforward when everything is in the same time zone.
5. Daylight Saving Time (DST) independence: UTC is not affected by DST changes, reducing potential bugs related to time shifts.

