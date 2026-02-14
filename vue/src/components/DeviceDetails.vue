<script setup>
    import { ref, defineEmits, nextTick } from 'vue'
    import { useSettings } from '@/settingsStore.js'
    import { formatTimeAgo, timeAgoHours } from '../helper'

    const { state } = useSettings()

    const emit = defineEmits(['close', 'patch'])
    const isVisible = ref(false)
    const isPatching = ref(false)
    const patchingKey = ref(null)
    const isEditing = ref(false)
    const editingKey = ref(null)

    const nameEditable = ref(null)
    const nameEditableValue = ref('')
    const onNameInput = (e) => {
        nameEditableValue.value = e.target.innerText
    }
    const locationEditable = ref(null)
    const locationEditableValue = ref('')
    const onLocationInput = (e) => {
        locationEditableValue.value = e.target.innerText
    }
    const commentEditable = ref(null)
    const commentEditableValue = ref('')
    const onCommentInput = (e) => {
        commentEditableValue.value = e.target.innerText
    }


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

    const recentlyCopiedKey = ref(null)
    const copyValueToClipboard = (value, key) => {
        navigator.clipboard.writeText(value)
            .then(() => {
                // Optionally, you can show a success message or visual feedback here
                console.log('Value copied to clipboard:', value)
                recentlyCopiedKey.value = key // Store the recently copied key
                setTimeout(() => {
                    recentlyCopiedKey.value = null // Clear the recently copied value after a short delay
                }, 2000) // Adjust the delay as needed
            })
            .catch(err => {
                // Handle errors if the copy action fails
                console.error('Failed to copy value:', err)
            })
    }

    
    const editKey = (key) => {
        editingKey.value = key
        isEditing.value = true
        nextTick(() => {
            // Map keys to their corresponding editable refs
            const editableRefs = {
                name: nameEditable,
                commentOnLocation: locationEditable,
                comment: commentEditable
            }
            const editableRef = editableRefs[key]
            if (editableRef && editableRef.value) {
                editableRef.value.focus()
                try {
                    const range = document.createRange()
                    range.selectNodeContents(editableRef.value)
                    range.collapse(false)
                    const sel = window.getSelection()
                    sel.removeAllRanges()
                    sel.addRange(range)
                } catch (e) {
                    // ignore selection errors
                }
            }
        })
    }

    const patchKey = (key, value) => {
        patchingKey.value = key
        isPatching.value = true
        emit('patch', { key, value })
    }

    const cancelEdit = () => {
        isEditing.value = false
        editingKey.value = null
    }

    const onKeyEdited = (key, success, message = null) => {
        isPatching.value = false
        patchingKey.value = null
    }

    defineExpose({
        showSidebar,
        onKeyEdited
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
            
            <div class="device-model">{{ device.deviceModel?.body?.name }}</div>

            <div class="device-details">

                <!-- Error message -->
                <div v-if="device.error" class="detail-item error error-message wide">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.error, 'error')">
                            <i :class="[recentlyCopiedKey === 'error' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">Fejl</span>
                    <span class="detail-value">{{ device.error }}</span>
                </div>

                <!-- <div :class="['detail-item', { 'offline': device.status === 'Offline' || device.status == undefined }]">
                    <span class="detail-label">Status</span>
                    <span class="detail-value">{{ device.status ?? 'Ukendt' }}</span>
                </div> -->

                <!-- Last seen -->
                <div :class="['detail-item', 'wide', { 'offline': device.latestReceivedMessage?.sentTime == undefined || timeAgoHours(device.latestReceivedMessage?.sentTime) > state.values.thresholds.lastSeen.offline, 'warning': device.latestReceivedMessage?.sentTime !== undefined && timeAgoHours(device.latestReceivedMessage?.sentTime) > state.values.thresholds.lastSeen.warning }]">
                    <span class="detail-label">Sidst set</span>
                    <span class="detail-value">
                        <template v-if="device.latestReceivedMessage?.sentTime">{{ formatTimeAgo(device.latestReceivedMessage?.sentTime) }} siden</template>
                        <template v-else>Ukendt</template>
                    </span>
                </div>

                <!-- RSSI -->
                <div :class="['detail-item', { warning: device.latestReceivedMessage?.rssi !== undefined && device.latestReceivedMessage?.rssi <= state.values.thresholds.rssi.warning, 'error': device.latestReceivedMessage?.rssi !== undefined && device.latestReceivedMessage?.rssi <= state.values.thresholds.rssi.error }]">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.latestReceivedMessage?.rssi, 'rssi')">
                            <i :class="[recentlyCopiedKey === 'rssi' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">RSSI</span>
                    <span class="detail-value">{{ device.latestReceivedMessage?.rssi ?? '&nbsp;' }}</span>
                </div>

                <!-- Batteri -->
                <div :class="['detail-item', { 'error': device.lorawanSettings?.deviceStatusBattery !== undefined && device.lorawanSettings?.deviceStatusBattery <= state.values.thresholds.battery.error, warning: device.lorawanSettings?.deviceStatusBattery !== undefined && device.lorawanSettings?.deviceStatusBattery <= state.values.thresholds.battery.warning }]"
                    v-if="device.lorawanSettings?.deviceStatusBattery !== undefined && device.lorawanSettings?.deviceStatusBattery !== -1">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.lorawanSettings?.deviceStatusBattery, 'battery')">
                            <i :class="[recentlyCopiedKey === 'battery' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">Batteri</span>
                    <span class="detail-value">{{ parseInt(device.lorawanSettings?.deviceStatusBattery ?? 0) }}%</span>
                </div>

                <div class="separator"></div>

                <!-- Name -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper" v-if="!(isEditing && editingKey === 'name')">
                        <div class="value-button button always-show" tabindex="-1" v-if="isPatching && patchingKey === 'name'">
                            <i class="fa-solid fa-spinner fa-spin"></i>
                        </div>
                        <template v-else>
                            <div class="value-button button" tabindex="-1" @click="editKey('name')">
                                <i class="fa-regular fa-edit"></i>
                            </div>
                            <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.name, 'name')">
                                <i :class="[recentlyCopiedKey === 'name' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                            </div>
                        </template>
                    </div>
                    <span class="detail-label">Navn</span>
                    <span class="detail-value" v-if="isEditing && editingKey === 'name'">
                            <div ref="nameEditable"
                                v-plain-text
                                class="edit-input"
                                @input="onNameInput"
                                @keydown.enter.prevent="patchKey('name', nameEditableValue);cancelEdit()"
                                @blur="cancelEdit()">{{ nameEditableValue.value ?? device.name }}</div>
                    </span>
                    <span v-else :class="['detail-value', { 'text-faded': isPatching && patchingKey === 'name' }]">{{ device.name ?? '&nbsp;' }}</span>
                </div>

                <!-- Model -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper" v-if="!isEditing || editingKey !== 'deviceModelId'">
                        <div class="value-button button always-show" tabindex="-1" v-if="isPatching && patchingKey === 'deviceModelId'">
                            <i class="fa-solid fa-spinner fa-spin"></i>
                        </div>
                        <template v-else>
                            <div class="value-button button" tabindex="-1" @click="editKey('deviceModelId')">
                                <i class="fa-regular fa-edit"></i>
                            </div>
                            <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.deviceModel?.body?.name, 'deviceModelId')">
                                <i :class="[recentlyCopiedKey === 'deviceModelId' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                            </div>
                        </template>
                    </div>
                    <span class="detail-label">Model</span>
                    <span class="detail-value" v-if="isEditing && editingKey === 'deviceModelId'">
                        <div class="dropdown-wrapper">
                            <div class="edit-dropdown">
                                <div class="dropdown-option default" @click="cancelEdit()">
                                    {{ device.deviceModel?.body?.name ?? 'Ingen' }}
                                    <span class="current-selection">Nuværende model</span>
                                </div>
                                <div class="dropdown-option"
                                     v-for="model in state.values.deviceModels.filter(model => model.id !== device.deviceModel?.id)"
                                     :key="model.id"
                                     @click="patchKey('deviceModelId', model.id);cancelEdit()">
                                        {{ model.name ?? model.id }}
                                </div>
                            </div>
                        </div>
                        &nbsp;
                    </span>
                    <span class="detail-value" v-else>{{ device.deviceModel?.body?.name ?? '&nbsp;' }}</span>
                </div>

                <!-- Location -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper" v-if="!(isEditing && editingKey === 'commentOnLocation')">
                        <div class="value-button button always-show" tabindex="-1" v-if="isPatching && patchingKey === 'commentOnLocation'">
                            <i class="fa-solid fa-spinner fa-spin"></i>
                        </div>
                        <template v-else>
                            <div class="value-button button" tabindex="-1" @click="editKey('commentOnLocation')">
                                <i class="fa-regular fa-edit"></i>
                            </div>
                            <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.commentOnLocation, 'location')">
                                <i :class="[recentlyCopiedKey === 'location' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                            </div>
                        </template>
                    </div>
                    <span class="detail-label">Lokation</span>
                    <span class="detail-value" v-if="isEditing && editingKey === 'commentOnLocation'">
                        <div
                            ref="locationEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onLocationInput"
                            @keydown.enter.prevent="patchKey('commentOnLocation', locationEditableValue);cancelEdit()"
                            @blur="cancelEdit()"
                        >{{ locationEditableValue.value ?? device.commentOnLocation }}</div>
                    </span>
                    <span v-else :class="['detail-value', { 'text-faded': isPatching && patchingKey === 'commentOnLocation' }]">{{ device.commentOnLocation ?? '&nbsp;' }}</span>
                </div>

                <!-- Comment -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper" v-if="!(isEditing && editingKey === 'comment')">
                        <div class="value-button button always-show" tabindex="-1" v-if="isPatching && patchingKey === 'comment'">
                            <i class="fa-solid fa-spinner fa-spin"></i>
                        </div>
                        <template v-else>
                            <div class="value-button button" tabindex="-1" @click="editKey('comment')">
                                <i class="fa-regular fa-edit"></i>
                            </div>
                            <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.comment, 'comment')">
                                <i :class="[recentlyCopiedKey === 'comment' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                            </div>
                        </template>
                    </div>
                    <span class="detail-label">Kommentar</span>
                    <span class="detail-value" v-if="isEditing && editingKey === 'comment'">
                        <div
                            ref="commentEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onCommentInput"
                            @keydown.enter.prevent="patchKey('comment', commentEditableValue);cancelEdit()"
                            @blur="cancelEdit()"
                        >{{ commentEditableValue.value ?? device.comment }}</div>
                    </span>
                    <span v-else :class="['detail-value', { 'text-faded': isPatching && patchingKey === 'comment' }]">{{ device.comment == "" || device.comment == "\n" ? '&nbsp;' : device.comment }}</span>
                </div>

                <div class="separator"></div>

                <!-- EUI -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.deviceEUI, 'eui')">
                            <i :class="[recentlyCopiedKey === 'eui' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">EUI</span>
                    <span class="detail-value">{{ device.deviceEUI ?? '&nbsp;' }}</span>
                </div>

                <!-- AppKey -->
                <div class="detail-item wide">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(device.OTAAapplicationKey, 'appKey')">
                            <i :class="[recentlyCopiedKey === 'appKey' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div>
                    <span class="detail-label">AppKey</span>
                    <span class="detail-value">{{ device.OTAAapplicationKey ?? '&nbsp;' }}</span>
                </div>

                <!-- JSON (Developer mode) -->
                <div class="detail-item wide" v-if="state.values.developerMode">
                    <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(JSON.stringify(device, null, 2), 'json')">
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
        z-index: 2;
        margin-top: calc(4.5rem + 3.5rem); /* 4.5 for navbar + 3.5rem for device toolbar */
        padding: 1.2rem;
        overflow-y: auto;
        max-height: calc(100vh - (4.5rem + 3.5rem));
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




    .text-faded {
        color: #aaa !important;
    }


</style>
