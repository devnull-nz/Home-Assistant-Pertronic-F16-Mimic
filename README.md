# Pertronic F16 Fire Alarm Control Panel Integration
This integration allows collecting of panel status and zone data from a [Pertronic F16](https://pertronic.co.nz/products/panels-networking-and-software/fire-alarm-control-panels/conventional-panels//product/14) fire alarm control panel into [Home Assistant](https://www.home-assistant.io) using a [USR-TCP232-304](https://www.aliexpress.com/item/4000296343313.html) RS485 to Ethernet convertor.

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

<b>Note:</b> This integration has been designed for use with the NZS4512:1997 variant F16, and has not been tested on currently avaiable F16E panels (NZS4512:2010 and above)

<br>



# Supported Functions
* Normal Indication
* Defect Indication
* Fire Indication
* Sprinkler Indication 
* Activated Zones Indication (Zones 1 - 8)

# Installation Instructions
## Prerequisites
Installation of this integration can be done either manually, or with [HACS](https://hacs.xyz/).
<br>This guide will provide instructions on installation using HACS.
<br>Follow the instructions, available on the HACS website [https://hacs.xyz/](https://hacs.xyz/) to install and configure HACS.


<br>

## Installation
Once HACS is installed, open it by clicking the icon in the sidebar.
<br>Once loaded, click on the `Integrations` menu, this will open the HACS integration selection menu.
<br>Click the settings icon in the top right hand corner of the page, and select the `Custom Repositories` option.
<br>In the text box labed `Repository`, copy and paste the following:
<br> `https://github.com/devnull-nz/Home-Assistant-Pertronic-F16-Mimic`
<br> select the category as `Integration`, then click add.
<br><br>The integration should now appear in the custom repositories list.
<br>Click on the integration in the list, and then at the bottom of the page, select `Download This Repository With HACS`.
When prompted, confirm this by clicking on the `DOWNLOAD` option.
<br>You will now need to restart Home Assitant, do this by going to the Settings menu -> System, and pressing the restart button in the top right corner.
<br>Home Assistant will now restart, and the integration will be available to configure. 

<br>

## Configuration
In Home Assistant, go to the Settings -> Devices & Services -> Integrations menu.
<br>Click the `Add Integration` button on the lower right side of the screen.
<br>Search for, and click on the `Pertronic F16` option, this will open the configuration menu.
<br>Enter a name for the panel, a short name (prefix) that will be added to the beginning of each entity name for the integration, the IP address of the RS485 to Ethernet Convertor, and the configured port.
