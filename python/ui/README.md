# Create Environment variables

```
export DEVICE_NAMES=.../device_alias
export WIFI_INFO=.../wifi_info
export USER_INFO=.../user_info
export FOCUS_APP_PACKAGE="..."
```

The idea is that these are 'developer' passwords and don't need to be too secure, but you still don't want them in a repo. The files have the following structures:

### DEVICE_NAMES

```
{
  "SERIAL_1" : {
        "name": "Alias 1",
        "scrcpy": ""
    },
  "SERIAL_2" : {
        "name": "Alias 2",
        "scrcpy": "-Sw"
    },
  ...
}
```

### WIFI_INFO

```
{
    "Friendly name": {
        "name":"As in wifi list",
        "password":"your_wifi_password"
    },
    "Another friendly name": {
        "name":"Wifi name",
        "password":"the password"
    },
}

```

### USER_INFO

```
{
    "login":[
        {
             "username" : "user name 1",
             "password" : "password 1"
        },
        {    
             "username" : "user name 2",
             "password" : "password 2"
        }
    ]
}

```
