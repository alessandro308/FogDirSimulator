# FogDirSimulator

These lines try to simulate Fog Director in order to prevent you to put in production an application that will destroy your infrastructure.

## How it works?
It simulates Fog Director giving the same [API of Fog Director](https://developer.cisco.com/docs/iox/#!fog-director-api-documentation/cisco-fog-director-rest-api) but executing all the operation only on a Database instead of on your infrastructure.

#### Available API (in progress)
A better (incomplete in this moment) documentation can be found [here](https://documenter.getpostman.com/view/2935895/RzZ4p2B7)

###### Authentication
 - `POST /api/v1/appmgr/tokenservice` To create a new token
    - Use this function to create a new token. A username and password have to be passed as basic HTTP Authentication. For the moment, these credential are hardcoded (admin, admin_123) and the token is not checked by other functions. 
 - `DELETE /api/v1/appmgr/tokenservice/<token>` To delete a valid token
    - Delete the token passed in the URL from the valid tokens. This function needs `x-token-id` field in the header to be executed

###### Devices
 - `POST /api/v1/appmgr/devices` To add a new device
    - Add a device to infrastructure. It requires a json data in the body with the following schema: `{ "port":8880, "ipAddress":"1.1.1.1", "username":"admin", "password":"test_psw"}`
 - `GET /api/v1/appmgr/devices?limit=100&offset=0&searchByTags=ciccio&searchByAnyMatch=123.12.1.2` To get devices from the database (all parameters are optionals)
    - Returns all the devices inserted. The output JSON is `{"data": [{device1}, {device2} ...]}`

###### Tags
 - `POST /api/v1/appmgr/tags` - To add a new tag to tag library
    - Create a new tag. It is not assigned to any device. It requires to pass data as JSON: `{"name": "tagname"}`
 - `GET /api/v1/appmgr/tags` - To get all tags from tag library
    - Returns all tags created in the system, with their ids
 - `POST /api/v1/appmgr/tags/<tagid>/devices` - To add a tag to selected devices (devices are provided as json data)
    - Tag a device with a specific tag. The tag is passed in URL, the device instead in the body as JSON array: `{"devices":[deviceids]}}`

###### Local Applications
 - `POST /api/v1/appmgr/localapps/upload` - To add an application from a file 
    - Use this function to upload an application. It must have a `package.yaml` file formatted as required for the IOX Application. This API accepts the following headers: `x-publish-on-upload`
 - `PUT /api/v1/appmgr/localapps/<appid>:<appversion>` - To update the application metadata, e.g. published status
    - Update an application (i.e. publish it, change description...). The original API requires to have all the field returned by the GET API, this API accepts also only the changed field. The `<appversion>` can be omitted, in that case its value becames 1.
 - `DELETE /api/v1/appmgr/apps/<appid>` - To delete the application (it have to be uninstalled from every device)
    - Delete an application passing its `<appid>` in the URL. This API accepts the following headers: `x-unpublish-on-delete`. If `x-unpublish-on-delete` is not specified, its values is `false`.
 - `GET /api/v1/appmgr/localapps/` - Get all the app (published and unpublished)


## In progress
This is the first project where I use MongoDB. Please, report any mistake on the NoSQL paradigm!

## Limitations / Main difference from Fog Director
 - The simulator doesn't manage multiversions applications. Each application is identified by an ID that is unique among all others application and versions (then in `/api/v1/appmgr/localapps/<appid>:<appversion>` the version is ignored).
 - In the PUT `/api/v1/appmgr/localapps/<appid>:<appversion>` API, also not completed description of application is accepted. In Fog Director this "partial body" returns an error.