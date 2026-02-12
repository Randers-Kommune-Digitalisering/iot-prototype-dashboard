<script setup>
    import { ref, defineEmits } from 'vue'
    import { useSettings } from '@/settingsStore.js'

    const emit = defineEmits(['close'])
    const isVisible = ref(false)

    const { state } = useSettings()

    defineProps({
        device: {
            type: Object,
            required: true
        }
    })

    function toggleSidebar() {
        isVisible.value = !isVisible.value
        if (!isVisible.value)
            emit('close')
    }

    function showSidebar() {
        isVisible.value = true
    }

    defineExpose({
        showSidebar
    })

    const recentlyCopiedKey = ref(null)
    const copyValueToClipboard = (value, key) => {
        navigator.clipboard.writeText(value)
            .then(() => {
                // Optionally, you can show a success message or visual feedback here
                console.log('Value copied to clipboard:', value);
                recentlyCopiedKey.value = key; // Store the recently copied key
                setTimeout(() => {
                    recentlyCopiedKey.value = null; // Clear the recently copied value after a short delay
                }, 2000); // Adjust the delay as needed
            })
            .catch(err => {
                // Handle errors if the copy action fails
                console.error('Failed to copy value:', err);
            });
    };
</script>

<template>
    <div
        class="sidebar"
        :style="{ transform: isVisible ? 'translateX(0)' : 'translateX(100%)' }"
    >
        <button @click="toggleSidebar">
            <i class="fa-solid fa-xmark"></i>
        </button>

        <template v-if="device">
            <div class="header">{{ device.name }}</div>
            
            <div class="device-model">{{ device.deviceModel }}</div>

            <div class="device-details">

                <div class="detail-item">
                    <span class="detail-label">Status</span>
                    <span class="detail-value">{{ device.status }}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Sidst set</span>
                    <span class="detail-value">{{ device.lastSeen }} siden</span>
                </div>
                <div :class="['detail-item', { 'error': device.rssi !== undefined && device.rssi <= state.values.thresholds.rssi.error, warning: device.rssi !== undefined && device.rssi <= state.values.thresholds.rssi.warning }]">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.rssi, 'rssi')">
                            <i :class="[recentlyCopiedKey === 'rssi' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">RSSI</span>
                    <span class="detail-value">{{ device.rssi }}</span>
                </div>
                <div :class="['detail-item', { 'error': device.battery !== undefined && device.battery <= state.values.thresholds.battery.error, warning: device.battery !== undefined && device.battery <= state.values.thresholds.battery.warning }]" v-if="device.battery">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.battery, 'battery')">
                            <i :class="[recentlyCopiedKey === 'battery' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">Batteri</span>
                    <span class="detail-value">{{ device.battery }}%</span>
                </div>

                <div class="seperator"></div>

                <div class="detail-item wide">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.name, 'name')">
                            <i :class="[recentlyCopiedKey === 'name' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">Navn</span>
                    <span class="detail-value">{{ device.name }}</span>
                </div>
                <div class="detail-item wide">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.type, 'type')">
                            <i :class="[recentlyCopiedKey === 'type' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">Type</span>
                    <span class="detail-value">{{ device.type }}</span>
                </div>
                
                <div class="seperator"></div>

                <div class="detail-item wide">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.eui, 'eui')">
                            <i :class="[recentlyCopiedKey === 'eui' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">EUI</span>
                    <span class="detail-value">{{ device.eui ?? '&nbsp;' }}</span>
                </div>
                <div class="detail-item wide">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(device.appKey, 'appKey')">
                            <i :class="[recentlyCopiedKey === 'appKey' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">AppKey</span>
                    <span class="detail-value">{{ device.appKey ?? '&nbsp;' }}</span>
                </div>

                <div class="detail-item wide" v-if="state.values.developerMode">
                    <div class="copy-button-wrapper">
                        <div class="copy-button button" tabindex="-1" @click="copyValueToClipboard(JSON.stringify(device, null, 2), 'json')">
                            <i :class="[recentlyCopiedKey === 'json' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">JSON</span>
                    <span class="detail-value" style="overflow: auto;font-size:10px;"><pre>{{ JSON.stringify(device, null, 2) }}</pre></span>
                </div>

            </div>

        </template>


    </div>
</template>

<style scoped>
    .sidebar {
        position: fixed;
        top: 0;
        right: 0;
        width: 35rem;
        height: 100vh;
        background: #2e2e2e;
        border-left: 0.1rem solid #363636;
        transition: transform 0.3s ease;
        z-index: 1000;
        margin-top: calc(4.5rem + 3.5rem); /* 4.5 for navbar + 3.5rem for device toolbar */
        padding: 1.2rem 1.5rem;
    }
    .sidebar button {
        float: right;
        width: 2.5rem;
        height: 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar .header {
        font-size: 1.4rem;
        line-height: 2.5rem;
        font-weight: 500;
        padding-left: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .device-model {
        color: #aaa;
        margin-bottom: 2rem;
        padding-left: 0.5rem;
        font-size: 1.15rem;
    }







    .device-details:not(:last-child) {
        margin-bottom: 2rem;
    }
    .device-details {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin-bottom: 2rem;
        margin-left: -0.5rem;
        margin-right: -0.5rem;
        /* background-color: #3b3b3b; */
        /* border-radius: 0.5rem; */
    }
    .device-details .seperator {
        grid-column: span 2;
        height: 0.1rem;
        background-color: #363636;
        margin: 0.5rem 0;
    }
    .device-details .detail-item {
        display: flex;
        gap: 0.5rem;
        flex-direction: column;
        padding: 0.8rem 1.5rem;
        border-radius: 0.4rem;
        transition: background-color 0.2s ease;
        position: relative;
    }
    .device-details .detail-item:hover {
        background-color: #323232;
    }
    .device-details .detail-item.wide {
        grid-column: span 2;
    }
    .device-details .detail-item.error {
        background-color: rgba(190, 70, 70, 0.25);
    }
    .device-details .detail-item.warning {
        background-color: rgba(190, 140, 70, 0.25);
    }
        .device-details .detail-label {
            color: #aaa;
        }
        .device-details .detail-value {
            font-size: 1.25rem;
            font-weight: 500;
            color: #eee;
        }

    
    .detail-item .copy-button-wrapper {
        position: absolute;
        top: 0rem;
        right: 0rem;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        padding-right: 0.5rem;
        opacity: 0;
        transition: opacity 0.2s ease;
    }
    .detail-item:hover .copy-button-wrapper {
        opacity: 1;
        pointer-events: all;
    }
    .detail-item .copy-button {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 3rem;
        width: 3rem;
        background-color: inherit;
    }
    .detail-item .copy-button:hover {
        color: #ddd;
        background-color: #373737;
    }
    .detail-item .copy-button:focus,
    .detail-item .copy-button:focus-visible {
        outline: 0;
        border-color: transparent !important;
        background-color: inherit;
    }


</style>
