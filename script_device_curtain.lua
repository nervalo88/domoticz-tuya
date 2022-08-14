-- demo device script
-- script names have three name components: script_trigger_name.lua
-- trigger can be 'time' or 'device', name can be any string
-- domoticz will execute all time and device triggers when the relevant trigger occurs
-- 
-- copy this script and change the "name" part, all scripts named "demo" are ignored. 
--
-- Make sure the encoding is UTF8 of the file
--
-- ingests tables: devicechanged, otherdevices,otherdevices_svalues
--
-- device changed contains state and svalues for the device that changed.
--   devicechanged['yourdevicename']=state 
--   devicechanged['svalues']=svalues string 
--
-- otherdevices and otherdevices_svalues are arrays for all devices: 
--   otherdevices['yourotherdevicename']="On"
--	otherdevices_svalues['yourotherthermometer'] = string of svalues
--
-- Based on your logic, fill the commandArray with device commands. Device name is case sensitive. 
--
-- Always, and I repeat ALWAYS start by checking for the state of the changed device.
-- If you would only specify commandArray['AnotherDevice']='On', every device trigger will switch AnotherDevice on, which will trigger a device event, which will switch AnotherDevice on, etc. 
--
-- The print command will output lua print statements to the domoticz log for debugging.
-- List all otherdevices states for debugging: 
--   for i, v in pairs(otherdevices) do print(i, v) end
-- List all otherdevices svalues for debugging: 
--   for i, v in pairs(otherdevices_svalues) do print(i, v) end
--
-- TBD: nice time example, for instance get temp from svalue string, if time is past 22.00 and before 00:00 and temp is bloody hot turn on fan. 


commandArray = {}
if (devicechanged['CurtainSelector']) then
	value = tonumber(otherdevices_svalues['CurtainSelector'])
	if value == 10 then 
		print('open shutters here') 
		os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py open")
	end
	if value == 20 then 
		print('close shutters here') 
		os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py close")
	end
	if value == 30 then 
		os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py stop")
	end
	if value == 40 then 
		print('SUN mode :)')
		os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py sun") 
	end
end

if(devicechanged['0x84ba20fffeda722a action_on']) then
	os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py open")
end

if(devicechanged['0x84ba20fffeda722a action_off']) then
	os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py close")
end

if(devicechanged['0x84ba20fffeda722a action_brightness_move_up']) then
	os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py stop")
end

if(devicechanged['0x84ba20fffeda722a action_brightness_move_down']) then
	os.execute("/home/pi/domoticz/scripts/lua/domoticz-tuya/shutter.py sun")
end


return commandArray

