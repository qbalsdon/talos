# Create Environment variables

```
export TALOS_SETTINGS=[path]
```

The idea is that these are 'developer' passwords and don't need to be too secure, but you still don't want them in a repo. The files have the following structures:

### SETTINGS

```
{
    "FOCUS_APP_PACKAGE": "your.app.package",
    "DEVICE_NAMES": {
      "Serial_1" : {
            "name": "Friendly Name 1",
            "scrcpy": ""
        },
      "Serial_2" : {
            "name": "Friendly Name 2",
            "scrcpy": "-Sw"
        }
    },
    "WIFI_INFO" : {
        "Friendly Wifi Reference": {
            "name":"As appears in network list",
            "password": "password"
        },
        "Friendly Wifi Reference 2": {
            "name":"As appears in network list",
            "password": "password"
        }
    },
    "USER_INFO": {
        "login":[
            {
                 "username" : "user_name_to_type",
                 "password" : "password_to_type"
            },
            {
                 "username" : "user_name_to_type",
                 "password" : "password_to_type"
            }
        ]
    }
}

```
