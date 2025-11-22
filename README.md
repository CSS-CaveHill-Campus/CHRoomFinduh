# FindYuhRoom
This is an API service that will expose information regarding to the availability of classes within the University of the West Indies Cavehill Campus. This is for research purposes only (please don't sue).

## Features

This API will provide the data for classes, alongside options for filters.

There are four endpoints listed as follows:

**/api/v1/schedule**
**/api/v1/free**
**/api/v1/rooms**
**/api/v1/prefixes**

Note: Each endpoint will only have access to data for the current semester.

> [!NOTE]
> While I may refer to them as `/free` and `/schedule`, each will have the prefix `/api/v1`.
> As such, when I say `/schedule`, I am indeed referring to `/api/v1/schedule`. Ty.

### Schedule

The `/schedule` endpoint will take a variety of query parameters, split into the categories of "mandatory" and "optional".

Mandatory parameters are:

Haven't decided yet. So far, each parameter will be optional.

Optional parameters include:

- faculty: What faculty to get the schedule for. Will return all rooms that will have a class from the specified faculty in it.
- limit: How many results to return. Will default to 20.
- day: 3 letter weekday of which to return the schedule for (Mon, Tue, Wed, Thu). Will default to all.
- room: A specific room to check the schedule for. Will default to `all`. Refer to `/rooms` for a list of all rooms.
- prefix: 4 character Course prefix (Example: PSCY, COMP, MATH) to filter by.

> [!NOTE]
> If `faculty` and `prefix` are both provided, the `prefix` will take precedence.

### Free

The `/free` endpoint will return a list of rooms that are free based on the following query parameters.

Mandatory:

- day: The day to check for.

Optional:

- hour: Hour in 24 hour format to check for room availabilities.
- duration: Number of hours a room should be available for, in order to be shown. Will default to 1, IF `hour` is set.
- room: A specific room to check for. (Refer to `/rooms`)

Such that, if we wanted to find all rooms that will be available between 1pm and 5pm on Tuesday, we can call the following route:
    `/api/v1/free?day=tue&hour=13&duration=4`

Similarly, if we wanted to see when ML4 would be available on Wednesdays, we would call the following route:
    `/api/v1/free?day=wed&room=ml4`

### Rooms

The `/rooms` endpoint, will return an array of *all* rooms, for which schedules exist.
This is purely for reference purposes, when calling the `/schedule` or `/free` route.
The information provided here will also be accessible within the `rooms.json` file.

### Prefixes

The `/prefixes.json` file, will contain a list of all course prefixes, grouped by faculty.

This will accept an optional parameter `faculty`, which will then return the prefixes related to the faculty.

## Data Structures

This section will outline the format for the data that the API will return, along with data the API will expect when making requests.

### Making Requests

When requesting data from the API, the query parameters you can send, will need to match the following formats:

`faculty` will be one of the following values:

```dart
enum Faculty {
    fccpa, // Faculty of Culture, Creative and Performing Arts
    fhe, // Faculty of Humanities and Education
    law, // Faculty of Law
    fms, // Faculty of Medical Sciences
    fst, // Faculty of Science and Technology
    fss, // Faculty of Social Sciences
}

`limit` will be a positive integer. Setting limit to 0 will return ALL results.

`day` will be one of the following values:

```dart
enum Day{
    mon,
    tue,
    wed,
    thu,
    fri,
    sat,
    sun
}
```

For example: `/api/v1/schedule?limit=5&day=mon`, will return the first 5 schedules for Monday.

`prefix` will be a 4 character string, that will be used to filter for rooms being used for specific types of courses.

Prefixes will be placed in `prefixes.md` for your reference, and similarly, accessible via `/prefixes`.

Such that, if we wanted to figure out where all COMP courses will be held for the semester on mondays, we can do:
    `/api/v1/schedule?limit=0&day=mon&prefix=COMP`

`room` will be one of the room options. Refer to the `/rooms` endpoint (or `/rooms.json` which will be created later) for a list of available rooms.

### Receiving Responses

Generally, successful responses will have the following format:

```json
{ 
    "status": "success",
    "data": [], # All routes will return an array as their data.
}
```

If any errors were to occur, then the following data format will be returned:

```json
{
    "status": "failed",
    "error": {
        "code": 500, # The error code
        "message": "A descriptive error message",
        "type": "user_friendly_error_type"
    }
}
```

The `/schedule` endpoint, will return an array of data in the following format:

```json
{
    "data": [
        {
            "course_code": "PSYC1020",
            "day": "mon",
            "start_time": "14", # Only storing the hours
            "end_time": "16",
            "class_type": "L|T", # L -> Lecture, T -> Tutorial
            "start_date": "mm/dd/yyyy",
            "end_date": "mm/dd/yyyy",
            "room": "LR21",
            "building": "Roy Marshall"
        }
    ]
}
```

The `/free` endpoint, will return a response matching the following format:

```json
{
    "data": [
        {
            "room": "The name of the available room",
            "day": "The day the room is available",
            "building": "The name of the building the room is in",
            "available_from": "The hour in which the room becomes available",
            "available_to": "The hour in which the room is no longer available",
        }
    ]
}
```

The `/rooms` endpoint will return an array of room names as follows:

```json
{
    "data": [
        "LR10",
        "LR9",
        "MSR2",
    ]
}
```

The `/prefixes` endpoint, will return a structure containing all course names prefixes in the following format:

```json
{
    "data": [
        {
            "faculty": "FST",
            "prefix": "COMP",
            "desc": "Computer Science",
        },
        {
            "faculty": "FST",
            "prefix": "CHEM",
            "desc": "Chemistry",
        }
    ]
}
```

## Extra

Thank you, have fun!
