<script setup>
    import { nextTick, ref, computed } from 'vue'
    import { useSettings } from '@/settingsStore.js'
    import { toStringOrNull } from '../helper'

    const { state } = useSettings()
    const emit = defineEmits(['device-added'])
    const isVisible = ref(false)

    function closeAddDevice() {
        // Close the overlay and reset the draft values
        device.value = { ...newDevice }
        isVisible.value = false
        hasValidationError.value = false
        errorMessage.value = ''
    }
    function overlayClick() {
        // Close overlay on background click but do NOT reset values — preserve draft.
        isVisible.value = false
        hasValidationError.value = false
        errorMessage.value = ''
    }

    const newDevice = {
        name: '',
        deviceEUI: '',
        OTAAapplicationKey: '',
        deviceModelId: null,
        commentOnLocation: '',
        comment: ''
    }
    const device = ref({ ...newDevice })
    const latestRegisteredDevices = ref([])

    const nameEditable = ref(null)
    const nameEditableValue = ref('')
    const onNameInput = (e) => {
        nameEditableValue.value = e.target.innerText
        device.value.name = nameEditableValue.value
    }
    const locationEditable = ref(null)
    const locationEditableValue = ref('')
    const onLocationInput = (e) => {
        locationEditableValue.value = e.target.innerText
        device.value.commentOnLocation = locationEditableValue.value
    }
    const commentEditable = ref(null)
    const commentEditableValue = ref('')
    const onCommentInput = (e) => {
        commentEditableValue.value = e.target.innerText
        device.value.comment = commentEditableValue.value
    }
    const euiEditable = ref(null)
    const euiEditableValue = ref('')
    const onEuiInput = (e) => {
        euiEditableValue.value = e.target.innerText
        device.value.deviceEUI = euiEditableValue.value
    }
    const appKeyEditable = ref(null)
    const appKeyEditableValue = ref('')
    const onAppKeyInput = (e) => {
        appKeyEditableValue.value = e.target.innerText
        device.value.OTAAapplicationKey = appKeyEditableValue.value
    }
    const isEditingModel = ref(false)

    const openAddDevice = () => {
        // Preserve existing `device.value`
        // Populate the editable refs from the current device values so the
        // contenteditable fields show the last-entered draft.
        console.log('Opening Add Device with current device state:', JSON.parse(JSON.stringify(device.value)))
        nameEditableValue.value = device.value.name || ''
        euiEditableValue.value = device.value.deviceEUI || ''
        appKeyEditableValue.value = device.value.OTAAapplicationKey || ''
        locationEditableValue.value = device.value.commentOnLocation || ''
        commentEditableValue.value = device.value.comment || ''

        isVisible.value = true

        nextTick(() => {
            // ensure DOM updated (for contenteditable fields)
            if (nameEditable.value) nameEditable.value.innerText = nameEditableValue.value
            if (euiEditable.value) euiEditable.value.innerText = euiEditableValue.value
            if (appKeyEditable.value) appKeyEditable.value.innerText = appKeyEditableValue.value
            if (locationEditable.value) locationEditable.value.innerText = locationEditableValue.value
            if (commentEditable.value) commentEditable.value.innerText = commentEditableValue.value
            focusNameInput()
        })
    }
    function focusNameInput() {
        if (nameEditable.value) {
            nameEditable.value.focus()
        }
    }

    const keyValidity = computed(() => ({
        name: !!(device.value.name || '').trim(),
        deviceEUI: /^[0-9A-Fa-f]{16}$/.test(device.value.deviceEUI || ''),
        OTAAapplicationKey: /^[0-9A-Fa-f]{32}$/.test(device.value.OTAAapplicationKey || '')
    }))

    const isValid = computed(() => Object.values(keyValidity.value).every(Boolean))
    const hasValidationError = ref(false)
    const errorMessage = ref('')
    const isAwaitingResponse = ref(false)

    function addDevice() {
        // Use reactive computed validity
        if (!isValid.value) {
            // If any required field is invalid, do not proceed
            hasValidationError.value = true
            return
        }
        errorMessage.value = ''

        // Emit event to parent component with new device details
        emit('device-added', { ...device.value })
        isAwaitingResponse.value = true
    }

    const onDeviceAdded = (addedDevice) => {
        console.log('Device event triggered successfully:', JSON.parse(JSON.stringify(addedDevice)))
        isAwaitingResponse.value = false

            // In case of error, repopulate editable fields
            if (addedDevice.error) {
                nextTick(() => {
                    errorMessage.value = addedDevice.error
                    if (nameEditable.value) nameEditable.value.innerText = nameEditableValue.value
                    if (euiEditable.value) euiEditable.value.innerText = euiEditableValue.value
                    if (appKeyEditable.value) appKeyEditable.value.innerText = appKeyEditableValue.value
                    if (locationEditable.value) locationEditable.value.innerText = locationEditableValue.value
                    if (commentEditable.value) commentEditable.value.innerText = commentEditableValue.value
                })

            // If successful, show success message
            // and clear fields for next entry
            } else {
                latestRegisteredDevices.value.push({ ...addedDevice })
                setTimeout(() => {
                    latestRegisteredDevices.value.shift()
                }, 10000)
                nextTick(() => {
                    device.value = { ...newDevice }
                    nameEditableValue.value = ''
                    euiEditableValue.value = ''
                    appKeyEditableValue.value = ''
                    locationEditableValue.value = ''
                    commentEditableValue.value = ''
                    nextTick(() => {
                        if (nameEditable.value) nameEditable.value.innerText = ''
                        if (euiEditable.value) euiEditable.value.innerText = ''
                        if (appKeyEditable.value) appKeyEditable.value.innerText = ''
                        if (locationEditable.value) locationEditable.value.innerText = ''
                        if (commentEditable.value) commentEditable.value.innerText = ''
                    })
                })
            }

    }

    defineExpose({
        openAddDevice, onDeviceAdded
    })
</script>

<template>

    <div class="add-device-overlay" v-if="isVisible" @click="overlayClick">

        <div class="add-device-body" @click.stop>
            <button @click="closeAddDevice" class="close-button">
                <i class="fa-solid fa-xmark"></i>
            </button>

            <div class="header">Registrér enhed</div>

            <div class="device-details">

                <!-- Error message -->
                <div v-if="errorMessage" class="detail-item error error-message wide">
                    <!-- <div class="buttons-wrapper">
                        <div class="value-button button" tabindex="-1" @click="copyValueToClipboard(errorMessage.value, 'error')">
                            <i :class="[recentlyCopiedError === 'error' ? 'fa-solid fa-copy' : 'fa-regular fa-copy']"></i>
                        </div>
                    </div> -->
                    <span class="detail-label">Registrering mislykkedes</span>
                    <span class="detail-value">{{ errorMessage }}</span>
                </div>

                <!-- Success message -->
                <div class="detail-item wide device-added-success"
                    v-if="latestRegisteredDevices.length && !errorMessage && !isAwaitingResponse"
                    v-for="device in latestRegisteredDevices"
                    :key="device.id">
                    <div class="detail-label">
                        <i class="fa-solid fa-check"></i>
                        <span style="font-weight: 500;">{{ device.name }}</span> blev registreret
                        <template  v-if="device.deviceModelId">
                            som
                            <span style="color:rgb(123, 136, 171);">
                                {{ state.values.deviceModels.find(model => model.id === device.deviceModelId)?.name ?? device.deviceModelId }}
                            </span>
                        </template>
                    </div>
                </div>

                <!-- Name -->
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.name }]">
                    <span class="detail-label">Navn</span>
                    <span class="detail-value">
                                <div
                                    v-if="!isAwaitingResponse"
                                    ref="nameEditable"
                                    v-plain-text
                                    class="edit-input"
                                    @input="onNameInput"
                                    @keydown.enter.prevent=""></div>
                                <span v-else>{{ toStringOrNull(device.name) ?? '&nbsp;' }}</span>
                    </span>
                </div>

                <!-- Model -->
                <div class="detail-item wide" @click="isEditingModel = true" :style="isAwaitingResponse ? { cursor: 'default', pointerEvents: 'none' } : { cursor: 'pointer' }">
                    <span class="detail-label">Model</span>
                    <span class="detail-value" v-if="isEditingModel">
                        <div class="dropdown-wrapper" @click.stop>
                            <div class="edit-dropdown">
                            <div class="dropdown-option default" @click="device.deviceModelId = null; isEditingModel = false">
                                    Ingen
                                    <span class="current-selection" v-if="device.deviceModelId == null">Nuværende valg</span>
                                </div>
                                <div class="dropdown-option"
                                     v-for="model in state.values.deviceModels"
                                     :key="model.id"
                                     @click="device.deviceModelId = model.id; isEditingModel = false">
                                        {{ model.name ?? model.id }}
                                        <span class="current-selection" v-if="device.deviceModelId === model.id">Nuværende valg</span>
                                </div>
                            </div>
                        </div>
                        &nbsp;
                    </span>
                    <span class="detail-value" v-else>{{ device.deviceModelId ? state.values.deviceModels.find(model => model.id === device.deviceModelId)?.name ?? device.deviceModelId : 'Ingen' }}</span>
                </div>

                <div class="separator margin"></div>

                <!-- EUI -->
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.deviceEUI }]">
                    <span class="detail-label">EUI</span>
                    <span class="detail-value">
                        <div
                            v-if="!isAwaitingResponse"
                            ref="euiEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onEuiInput"
                            @keydown.enter.prevent=""
                        ></div>
                        <span v-else>{{ toStringOrNull(device.deviceEUI) ?? '&nbsp;' }}</span>
                    </span>
                </div>

                <!-- AppKey -->
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.OTAAapplicationKey }]">
                    <span class="detail-label">AppKey</span>
                    <span class="detail-value">
                        <div
                            v-if="!isAwaitingResponse"
                            ref="appKeyEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onAppKeyInput"
                            @keydown.enter.prevent=""
                        ></div>
                        <span v-else>{{ toStringOrNull(device.OTAAapplicationKey) ?? '&nbsp;' }}</span>
                    </span>
                </div>

                <div class="separator margin"></div>

                <!-- Location -->
                <div class="detail-item wide">
                    <span class="detail-label">Lokation</span>
                    <span class="detail-value">
                        <div
                            v-if="!isAwaitingResponse"
                            ref="locationEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onLocationInput"
                            @keydown.enter.prevent=""
                        ></div>
                        <span v-else>{{ toStringOrNull(device.commentOnLocation) ?? '&nbsp;' }}</span>
                    </span>
                </div>

                <!-- Comment -->
                <div class="detail-item wide">
                    <span class="detail-label">Kommentar</span>
                    <span class="detail-value">
                        <div
                            v-if="!isAwaitingResponse"
                            ref="commentEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onCommentInput"
                            @keydown.enter.prevent=""
                        ></div>
                        <span v-else>{{ toStringOrNull(device.comment) ?? '&nbsp;' }}</span>
                    </span>
                </div>

            </div>

            <div class="button-wrapper">
                <button class="primary" style="margin-top: 1rem;" @click="addDevice()" :disabled="isAwaitingResponse">
                    <i class="fa-solid fa-plus" v-if="!isAwaitingResponse"></i>
                    <div class="fa-spinner-wrapper" v-else><i class="fa-solid fa-spinner fa-spin"></i></div>
                    <span>Registrér enhed</span>
                </button>
            </div>

        </div>

    </div>

</template>

<style scoped>

.add-device-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 5;
}
.add-device-body {
    background: #2e2e2e;
    border: 0.1rem solid #363636;
    padding: 1.2rem;
    border-radius: 0.5rem;
    width: 40rem;
    max-width: 90%;
    z-index: 6;
    max-height: 90%;
    overflow-y: auto;
}
.add-device-body .header { 
    font-size: 1.4rem;
    line-height: 2.5rem;
    font-weight: 500;
    padding-left: 0.5rem;
    margin-bottom: 1.2rem;
}
.close-button {
    float: right;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.button-wrapper {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 1.5rem;
}
button:not(.close-button) {
    padding: 0.8rem 1.6rem; 
    font-size: 1.1rem;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}
button:not(.close-button) > i {
    transform: translateX(-0.4rem);
    margin-right: 0.2rem;
}
button > span {
    display: inline-block;
    transform: translateY(-0.1rem);
}

.error-message {
    margin-bottom: 1rem;
}
.fa-spinner-wrapper {
    transform: translateX(-0.4rem);
    margin-right: 0.2rem;
}

.device-added-success i.fa-check {
    color: #4BB543;
    margin-right: 0.6rem;
    transform: translateY(0.05rem);
}

</style>