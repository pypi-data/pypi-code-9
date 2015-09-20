import bluesky_cli

#Specified your bluesky gateway
BlueskyGateway = "127.0.0.1:8189"

conn = bluesky_cli.blueskyconn(BlueskyGateway, "guest", "guest")
deviceList = conn.list_ed()
for device in deviceList:
    deviceIP = "0.0.0.0"
    connStatus = "offline"
    for key in device.keys():
        if key == "EDIP":
            deviceIP = device[key]
        if key == "connStatus":
            connStatus = device[key]
    if connStatus == "online":
        y = conn.getSensorDatByAdc(deviceIP, "mcp3208")
        print "{} {}".format(deviceIP, y)
        y = conn.getSensorDatByAdcChannel(deviceIP, "mcp3208", "0")
        print y
