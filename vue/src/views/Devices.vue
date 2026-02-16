<script setup>
    import { ref, computed, onMounted } from 'vue'
    import DeviceToolbar from '@/components/DeviceToolbar.vue'
    import DeviceDetails from '@/components/DeviceDetails.vue'
    import { useSettings } from '@/settingsStore.js'
    import OS2IoTService from '@/backendService.js'
    import { formatTimeAgo, timeAgoHours, sortGroups, toStringOrNull } from '../helper'

    const currentView = ref('lokation') // 'lokation' or 'model'
    const deviceToolbar = ref(null)
    const deviceDetails = ref(null)
    const selectedDevice = ref({})

    const { state } = useSettings()

    const devices = ref([])

    onMounted(async () => {
        try {
            console.log('Loading devices from backend...')
            const data = await OS2IoTService.getDevices()
            // Verify data format
            if (!Array.isArray(data.devices)) {
                throw new Error('Invalid devices data format')
            }
            console.log('Devices loaded:', data.devices)
            devices.value = data.devices
        } catch (err) {
            console.error('Failed to load devices:', err)
        }
    })


    /* Device grouping and sorting */

    const devicesByType = computed(() => {
        const groups = {}
        const list = Array.isArray(devices.value) ? devices.value : []
        list.forEach(device => {
            const type = device?.deviceModel?.body?.name ?? 'Ukendt'
            if (!groups[type]) groups[type] = []
            groups[type].push(device)
        })
        return sortGroups(groups)
    })

    const devicesByLocation = computed(() => {
        const groups = {}
        const list = Array.isArray(devices.value) ? devices.value : []
        list.forEach(device => {
            const location = toStringOrNull(device?.commentOnLocation) ?? 'Ukendt'
            if (!groups[location]) groups[location] = []
            groups[location].push(device)
        })
        return sortGroups(groups)
    })

    const deviceList = computed(() => {
        return currentView.value === 'model' ? devicesByType.value : devicesByLocation.value
    })


    /* Toggle device details */

    const showDeviceDetails = (device) => {
        if (deviceDetails.value) {
            selectedDevice.value = device
            deviceDetails.value.showSidebar()
        }
    }


    /* Device search and filtering */ 

    const searchQuery = ref('')

    const filteredDevices = computed(() => {
        const q = searchQuery.value.trim().toLowerCase()
        if (!q) return deviceList.value
        let filteredList = {}
        for (const [group, devs] of Object.entries(deviceList.value)) {
            const matchedDevices = devs.filter(device => {
                const name = (device.name || '').toLowerCase()
                const location = (device.commentOnLocation || '').toLowerCase()
                const model = (device.deviceModel?.body?.name || '').toLowerCase()
                const eui = (device.deviceEUI || '').toLowerCase()
                return name.includes(q) || location.includes(q) || model.includes(q) || eui.includes(q)
            })
            if (matchedDevices.length > 0) {
                filteredList[group] = matchedDevices
            }
        }
        console.log('Filtered devices:', filteredList)
        return filteredList
    })

    const onSearchChanged = (val) => {
        searchQuery.value = val
    }

    const onViewChanged = (val) => {
        // console.log('View changed to:', val)
        currentView.value = val
    }


    /* Patch device details */

    const onDevicePatch = async ({ key, value }) => {
        if (!selectedDevice.value || !selectedDevice.value.id) return
        const deviceId = selectedDevice.value.id
        try {
            const response = await OS2IoTService.patchDevice(deviceId, { [key]: value })
            // Update local state after successful update
            selectedDevice.value[key] = value
            // Also update the main devices list to reflect changes in the UI
            const deviceIndex = devices.value.findIndex(d => d.id === deviceId)
            if (deviceIndex !== -1) {
                if (key === 'deviceModelId') {
                    // If device model was changed, we need to update the whole device model object in the devices list
                    const newModel = response.deviceModel
                    if (newModel) {
                        devices.value[deviceIndex]['deviceModel'] = newModel
                    }
                } else
                    devices.value[deviceIndex][key] = value
            }
            deviceDetails.value.onKeyEdited(key, true)
        } catch (err) {
            console.error('Failed to update device:', err)
            deviceDetails.value.onKeyEdited(key, false, 'Opdatering mislykkedes')
        }
    }

    const onAddDevice = async (device) => {
        try {
            const response = await OS2IoTService.addDevice(device)
            if (response.error) {
                throw new Error(response.error)
            }
            console.log('Device added successfully:', response)
            deviceToolbar.value.onDeviceAdded({ ...device, ...response })
            // devices.value.push(response) // Assuming the response contains the newly created device object
            // showDeviceDetails(device)
        } catch (err) {
            console.error('Failed to add device:', err)
            deviceToolbar.value.onDeviceAdded({ ...device, 'error': err.message })
        }
    }

</script>

<template>
    <DeviceToolbar ref="deviceToolbar" @search-changed="onSearchChanged" @view-changed="onViewChanged" @add-device="onAddDevice" />
    <DeviceDetails ref="deviceDetails" @close="selectedDevice = {}" :device="selectedDevice" @patch="onDevicePatch" />

    <div class="content-margin">

        <div v-for="(group, groupName) in filteredDevices" :key="groupName" class="device-group">
            <div class="device-group-name">{{ groupName }}</div>

            <div class="device-list">
                <div
                    v-for="device in group"
                    :key="device.id"
                    :class="['device-item', { 'offline': device.latestReceivedMessage?.sentTime == undefined || timeAgoHours(device.latestReceivedMessage?.sentTime) > state.values.thresholds.lastSeen.offline, 'warning': device.latestReceivedMessage?.sentTime !== undefined && timeAgoHours(device.latestReceivedMessage?.sentTime) > state.values.thresholds.lastSeen.warning, 'selected': selectedDevice && selectedDevice.id === device.id }]"
                    @click="showDeviceDetails(device)"
                    >
                    <div class="device-name">
                        <div class="status">
                            <div v-if="device.latestReceivedMessage?.rssi !== undefined" :class="{ 'warning': device.latestReceivedMessage?.rssi !== undefined && device.latestReceivedMessage?.rssi <= state.values.thresholds.rssi.warning, 'error': device.latestReceivedMessage?.rssi !== undefined && device.latestReceivedMessage?.rssi <= state.values.thresholds.rssi.error }">
                                {{ device.latestReceivedMessage?.rssi }}&nbsp;<i class="fa-solid fa-wifi"></i>
                            </div>
                            <div v-if="device.lorawanSettings?.deviceStatusBattery !== undefined && device.lorawanSettings?.deviceStatusBattery !== -1" :class="{ 'warning': device.lorawanSettings?.deviceStatusBattery !== undefined && device.lorawanSettings?.deviceStatusBattery <= state.values.thresholds.battery.warning }">
                                {{ parseInt(device.lorawanSettings?.deviceStatusBattery ?? 0) }}%&nbsp;<i class="fa-solid fa-battery-three-quarters"></i>
                            </div>
                        </div>
                        {{ device.name }}
                        <!-- <span :class="['device-health', device.status.toLowerCase()]">●</span> -->
                    </div>
                    <div class="device-info">
                        <div class="last-seen"><i class="fa-solid fa-clock"></i>
                            <template v-if="device.latestReceivedMessage?.sentTime">{{ formatTimeAgo(device.latestReceivedMessage?.sentTime) }} siden</template>
                            <template v-else>Ukendt</template>
                        </div>
                        <div :class="['synced-ento', device.isSyncedWithEnto ? 'synced' : 'not-synced']"><i :class="['fa-solid', 'fa-chart-line', ]"></i> {{ device.isSyncedWithEnto ? 'Seneste data findes i Ento' : 'Data mangler i Ento' }}</div>
                        <div class="device-model" v-if="currentView !== 'model'"><i class="fa-solid fa-microchip"></i> {{ device.deviceModel?.body?.name }}</div>
                        <div class="location" v-if="currentView !== 'lokation'"><i class="fa-solid fa-house-chimney"></i> {{ device.commentOnLocation ?? 'Ukendt' }}</div>
                        
                    </div>

                    <!-- Error banner -->
                    <!-- <div v-if="device.error || device.status == 'Offline'" :class="['device-message', device.error ? 'error' : 'offline']"  aria-live="polite">
                        <div :class="{ 'scroll-content': device.error?.length > 34 }">
                            <span v-if="device.error" class="text">{{ device.error }}</span>
                            <span v-else class="text">Enheden er offline</span>
                        </div>
                    </div> -->

                </div><!-- /device-item -->
            </div><!-- /device-list -->
        </div>

    </div>
    <div class="device-details">
        <!-- Placeholder for device details view -->
    </div>
</template>

<style scoped>
    .content-margin {
        margin-top: calc(1.8rem + 3.5rem); /* Add 3.5rem for device toolbar */
        margin-bottom: 2rem;
        padding-right: 35rem; /* Add space for device device details */
    }
    .device-group {
        margin-top: 2rem;
    }
        .device-group-name {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

    .device-list {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .device-item {
        position: relative;
        padding: 0.7rem 1rem;
        width: 15rem;
        height: 12rem;
        /* background-color: rgb(87, 79, 68); */
        background-color: rgb(69, 81, 69);
        border-radius: 0.5rem;
        overflow: hidden;
        user-select: none;
        cursor: pointer;
        transition: outline 0.15s;
        outline: 0.1rem solid transparent;
        display: flex;
        flex-direction: column;
    }
    .device-item:hover {
        outline: 0.1rem solid #8c8c8c;
    }
    .device-item.selected {
        outline: 0.1rem solid #ffffff;
    }
    .device-item.error {
        background-color: rgb(87, 69, 69);
    }
    .device-item.warning {
        background-color: rgb(87, 79, 68);
    }
    .device-item.offline {
        background-color: rgb(69, 69, 77);
    }
        .device-name {
            font-size: 1.1rem;
            font-weight: 500;
        }
        .status {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 0.6rem;
            float: right;
            font-size: 0.7rem;
            padding-top: 0.4rem;
        }
        .status > div {
            display: flex;
            align-items: center;
            gap: 0.2rem;
            color: rgb(150, 150, 150);
        }
            .status .warning {
                color: rgb(190, 145, 115) !important;
            }
            .status .error {
                color: rgb(190, 115, 115) !important;
            }

    .device-info {
        margin-top: auto;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: rgb(180, 180, 180);
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
        .device-info > div {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .device-info i {
            font-size: 0.7rem;
            transform: translateY(15%);
        }
        .device-info .device-model {
            color: rgb(123, 136, 171);
        }
        .device-info .location {
            color: rgb(169, 171, 123);
        }

    .device-message {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 0.4rem 1rem;
        overflow: hidden;
        white-space: nowrap;
    }
    .device-message.error {
        background-color: rgb(139, 72, 72);
    }
    .device-message.warning {
        background-color: rgb(139, 114, 72);
    }
    .device-message.offline {
        background-color: rgb(72, 72, 139);
    }
        .device-message .scroll-wrap {
            width: 100%;
            overflow: hidden;
        }
        .device-message .scroll-content {
            display: inline-block;
            white-space: nowrap;
            transform: translateX(100%);
            animation: marquee 12s linear infinite;
            color: rgb(230, 230, 230);
        }
        .device-message .text {
            margin-right: 1rem;
            color: rgb(230, 230, 230);
            font-size: 0.9rem;
        }
        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
</style>