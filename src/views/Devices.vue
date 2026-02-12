<script setup>
    import { ref, computed } from 'vue'
    import DeviceToolbar from '@/components/DeviceToolbar.vue'
    import DeviceDetails from '@/components/DeviceDetails.vue'
    import { useSettings } from '@/settingsStore.js'

    const currentView = ref('lokation') // 'lokation' or 'enhedstype'
    const deviceDetails = ref(null)
    const selectedDevice = ref({})

    const { state } = useSettings()


    /* Devices */

    const devices = [
        { id: 1, name: 'Energi', status: 'Online', lastSeen: '5 minutter', location: 'Grønhøjskolen', type: 'Energi', isSyncedWithEnto: true, rssi: -70, deviceModel: 'Milesight Energimåler' },
        { id: 2, name: 'Vand kælder', status: 'Offline', lastSeen: '2 timer', location: 'Grønhøjskolen', type: 'Vand', isSyncedWithEnto: false, deviceModel: 'Kamstrup Vandmåler' },
        { id: 3, name: 'Energi', status: 'Online', lastSeen: '10 minutter', location: 'Åbakken', type: 'Energi', isSyncedWithEnto: true, rssi: -60, deviceModel: 'Milesight Energimåler' },
        { id: 4, name: 'Vand', status: 'Online', lastSeen: '1 minut', location: 'Åbakken', type: 'Vand', isSyncedWithEnto: true, rssi: -85, deviceModel: 'Kamstrup Vandmåler' },
        { id: 5, name: 'Indeklima', status: 'Error', lastSeen: '3 dage', error: 'Enheden findes ikke i os2-IoT', location: 'Grønhøjskolen', type: 'Indeklima', isSyncedWithEnto: false, deviceModel: 'Sensirion Indeklimasensor' },
        { id: 6, name: 'Bevægelse', status: 'Online', lastSeen: '30 sekunder', location: 'Åbakken', type: 'Bevægelse', isSyncedWithEnto: true, battery: 18, rssi: -80, deviceModel: 'Milesight Bevægelsessensor' },
        { id: 8, name: 'Indeklima', status: 'Online', lastSeen: '15 minutter', location: 'Åbakken', type: 'Indeklima', isSyncedWithEnto: true, battery: 20, rssi: -65, deviceModel: 'Sensirion Indeklimasensor' },
        { id: 9, name: 'Varme', status: 'Online', lastSeen: '1 minut', location: 'Åbakken', type: 'Varme', isSyncedWithEnto: true, battery: 75, rssi: -75, deviceModel: 'Kamstrup Varmemåler' },
    ]

    const devicesByType = computed(() => {
        const groups = {}
        devices.forEach(device => {
            if (device.type === null)
                device.type = 'Ukendt'
            if (!groups[device.type])
                groups[device.type] = []
            groups[device.type].push(device)
        })
        return groups
    })

    const devicesByLocation = computed(() => {
        const groups = {}
        devices.forEach(device => {
            if (device.location === null)
                device.location = 'Ukendt'
            if (!groups[device.location])
                groups[device.location] = []
            groups[device.location].push(device)
        })
        return groups
    })

    const deviceList = computed(() => {
        return currentView.value === 'enhedstype' ? devicesByType.value : devicesByLocation.value
    })

    /* Toggle device details */

    const showDeviceDetails = (device) => {
        if (deviceDetails.value) {
            selectedDevice.value = device
            deviceDetails.value.showSidebar()
        }
    }


    /* Search and filtering */ 

    const searchQuery = ref('')

    const filteredDevices = computed(() => {
        const q = searchQuery.value.trim().toLowerCase()
        if (!q) return deviceList.value
        let filteredList = {}
        for (const [group, devs] of Object.entries(deviceList.value)) {
            const matchedDevices = devs.filter(device => {
                const name = (device.name || '').toLowerCase()
                const location = (device.location || '').toLowerCase()
                const type = (device.type || '').toLowerCase()
                return name.includes(q) || location.includes(q) || type.includes(q)
            })
            if (matchedDevices.length > 0) {
                filteredList[group] = matchedDevices
            }
        }
        return filteredList
    })

    const onSearchChanged = (val) => {
        searchQuery.value = val
    }

    const onViewChanged = (val) => {
        // console.log('View changed to:', val)
        currentView.value = val
    }
</script>

<template>
    <DeviceToolbar @search-changed="onSearchChanged" @view-changed="onViewChanged" />
    <DeviceDetails ref="deviceDetails" @close="selectedDevice = {}" :device="selectedDevice" />

    <div class="content-margin">

        <div v-for="(group, groupName) in filteredDevices" :key="groupName" class="device-group">
            <div class="device-group-name">{{ groupName }}</div>

            <div class="device-list">
                <div
                    v-for="device in group"
                    :key="device.id"
                    :class="['device-item', device.status.toLowerCase(), { selected: selectedDevice && selectedDevice.id === device.id }]"
                    @click="showDeviceDetails(device)"
                    >
                    <div class="device-name">
                        {{ device.name }}
                        <div class="status">
                            <div v-if="device.rssi !== undefined" :class="{ 'warning': device.rssi !== undefined && device.rssi <= state.values.thresholds.rssi.warning }"><i class="fa-solid fa-wifi"></i> {{ device.rssi }}</div>
                            <div v-if="device.battery !== undefined" :class="{ 'warning': device.battery !== undefined && device.battery <= state.values.thresholds.battery.warning }"><i class="fa-solid fa-battery-three-quarters"></i> {{ device.battery }}%</div>
                        </div>
                        <!-- <span :class="['device-health', device.status.toLowerCase()]">●</span> -->
                    </div>
                    <div class="device-info">
                        <div class="device-model"><i class="fa-solid fa-microchip"></i> {{ device.deviceModel }}</div>
                        <div class="last-seen"><i class="fa-solid fa-clock"></i> Set {{ device.lastSeen }} siden</div>
                        <div :class="['synced-ento', device.isSyncedWithEnto ? 'synced' : 'not-synced']"><i :class="['fa-solid', 'fa-chart-line', ]"></i> {{ device.isSyncedWithEnto ? 'Seneste data findes i Ento' : 'Data mangler i Ento' }}</div>
                        <div class="location"><i class="fa-solid fa-house-chimney"></i> {{ device.location }}</div>
                        
                    </div>

                    <div v-if="device.error || device.status == 'Offline'" :class="['device-message', device.error ? 'error' : 'offline']"  aria-live="polite">
                        <div :class="{ 'scroll-content': device.error?.length > 34 }">
                            <span v-if="device.error" class="text">{{ device.error }}</span>
                            <span v-else class="text">Enheden er offline</span>
                        </div>
                    </div>

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
    /* .device-item.warning {
        background-color: rgb(87, 79, 68);
    } */
    .device-item.offline {
        background-color: rgb(69, 69, 77);
    }
        .device-name {
            font-size: 1.1rem;
            font-weight: 500;
        }
        .status {
            display: flex;
            justify-content: flex-end;
            gap: 0.4rem;
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
            .warning {
                color: rgb(190, 145, 115) !important;
            }
            .error {
                color: rgb(190, 115, 115) !important;
            }

    .device-info {
        margin-top: 0.5rem;
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