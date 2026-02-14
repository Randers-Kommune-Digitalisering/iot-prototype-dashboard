<script setup>
    import { nextTick, ref, computed } from 'vue'
    import { useSettings } from '@/settingsStore.js'

    const { state } = useSettings()

    defineEmits(['device-added'])

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
        devEUI: '',
        OTAAapplicationKey: '',
        deviceModelId: '',
        commentOnLocation: '',
        deviceModelId: null,
        comment: ''
    }
    const device = ref({ ...newDevice })

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
        device.value.devEUI = euiEditableValue.value
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
        nameEditableValue.value = device.value.name || ''
        euiEditableValue.value = device.value.devEUI || ''
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
        })
    }
    function focusNameInput() {
        if (nameEditable.value) {
            nameEditable.value.focus()
        }
    }

    const keyValidity = computed(() => ({
        name: !!(device.value.name || '').trim(),
        devEUI: /^[0-9A-Fa-f]{16}$/.test(device.value.devEUI || ''),
        OTAAapplicationKey: /^[0-9A-Fa-f]{32}$/.test(device.value.OTAAapplicationKey || '')
    }))

    const isValid = computed(() => Object.values(keyValidity.value).every(Boolean))
    const hasValidationError = ref(false)
    const errorMessage = ref('')

    function addDevice() {
        
        errorMessage.value = 'Der opstod en fejl under registreringen. Prøv igen senere.'
        return

        // Use reactive computed validity
        if (!isValid.value) {
            // If any required field is invalid, do not proceed
            hasValidationError.value = true
            return
        }
        
        errorMessage.value = ''
        // Emit event to parent component with new device details
        // emit('device-added', { ...device.value })

        // Show awaiting state
    }

    defineExpose({
        openAddDevice
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

                <!-- Name -->
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.name }]">
                    <span class="detail-label">Navn</span>
                    <span class="detail-value">
                                <div ref="nameEditable"
                                    v-plain-text
                                    class="edit-input"
                                    @input="onNameInput"
                                    @keydown.enter.prevent=""></div>
                    </span>
                </div>

                <!-- Model -->
                <div class="detail-item wide" @click="isEditingModel = true" style="cursor: pointer;">
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
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.devEUI }]">
                    <span class="detail-label">EUI</span>
                    <span class="detail-value">
                        <div
                            ref="euiEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onEuiInput"
                            @keydown.enter.prevent=""
                        ></div>
                    </span>
                </div>

                <!-- AppKey -->
                <div :class="['detail-item', 'wide', { 'error': hasValidationError && !keyValidity.OTAAapplicationKey }]">
                    <span class="detail-label">AppKey</span>
                    <span class="detail-value">
                        <div
                            ref="appKeyEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onAppKeyInput"
                            @keydown.enter.prevent=""
                        ></div>
                    </span>
                </div>

                <div class="separator margin"></div>

                <!-- Location -->
                <div class="detail-item wide">
                    <span class="detail-label">Lokation</span>
                    <span class="detail-value">
                        <div
                            ref="locationEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onLocationInput"
                            @keydown.enter.prevent=""
                        ></div>
                    </span>
                </div>

                <!-- Comment -->
                <div class="detail-item wide">
                    <span class="detail-label">Kommentar</span>
                    <span class="detail-value">
                        <div
                            ref="commentEditable"
                            v-plain-text
                            class="edit-input"
                            @input="onCommentInput"
                            @keydown.enter.prevent=""
                        ></div>
                    </span>
                </div>

            </div>

            <div class="button-wrapper">
                <button class="primary" style="margin-top: 1rem;" @click="addDevice()">
                    <i class="fa-solid fa-check"></i> Registrér enhed
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
}
button:not(.close-button) i {
    transform: translateX(-0.4rem);
    margin-right: 0.2rem;
}

.error-message {
    margin-bottom: 1rem;
}

</style>