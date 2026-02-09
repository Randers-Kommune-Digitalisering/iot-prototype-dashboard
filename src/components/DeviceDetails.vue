<script setup>
    import { ref, defineEmits } from 'vue'

    const emit = defineEmits(['close'])
    const isVisible = ref(false)

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

            <div class="device-details">

                <div class="detail-item">
                    <span class="detail-label">Status</span>
                    <span class="detail-value">{{ device.status }}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Sidst set</span>
                    <span class="detail-value">{{ device.lastSeen }}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">RSSI</span>
                    <span class="detail-value">{{ device.rssi }}</span>
                </div>            
                <div class="detail-item">
                    <span class="detail-label">Batteri</span>
                    <span class="detail-value">{{ device.battery }}</span>
                </div>
                
            </div>

            <div class="device-details">

                <div class="detail-item">
                    <span class="detail-label">Navn</span>
                    <span class="detail-value">{{ device.name }}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Målertype</span>
                    <span class="detail-value">{{ device.type }}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Model</span>
                    <span class="detail-value">{{ device.deviceModel }}</span>
                </div>

            </div>
            
        </template>


        JSON:
        <pre>{{ JSON.stringify(device, null, 2) }}</pre>

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
        padding: 1.2rem 2rem;
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
        font-size: 1.3rem;
        line-height: 2.5rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .device-details {
        display: flex;
        flex-direction: column;
        font-size: 1.15rem;
    }
    .device-details:not(:last-child) {
        margin-bottom: 2rem;
    }
        .detail-item {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .detail-label {
            font-weight: 500;
            color: #aaa;
            width: 7rem;
        }
        .detail-value {
            color: #eee;
        }
</style>
