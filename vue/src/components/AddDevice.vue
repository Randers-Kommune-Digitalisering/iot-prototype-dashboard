<script setup>
    import { nextTick, ref } from 'vue'
    import { useSettings } from '@/settingsStore.js'

    const { state } = useSettings()

    defineEmits(['device-added'])

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
    const euiEditable = ref(null)
    const euiEditableValue = ref('')
    const onEuiInput = (e) => {
        euiEditableValue.value = e.target.innerText
    }
    const appKeyEditable = ref(null)
    const appKeyEditableValue = ref('')
    const onAppKeyInput = (e) => {
        appKeyEditableValue.value = e.target.innerText
    }
    const isEditingModel = ref(false)

    const isVisible = ref(false)
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

    const openAddDevice = () => {
        // device.value = { ...newDevice }
        isVisible.value = true

        nextTick(() => {
            focusNameInput()
        })
    }

    function focusNameInput() {
        if (nameEditable.value) {
            nameEditable.value.focus()
        }
    }

    function addDevice() {
        // Check required fields validity

        // Emit event to parent component with new device details
        // emit('device-added', { ...device.value })

        // Show awaiting state
    }

    defineExpose({
        openAddDevice
    })
</script>

<template>

    <div class="add-device-overlay" v-if="isVisible" @click="isVisible = device == newDevice ? false : isVisible">

        <div class="add-device-body" @click.stop>
            <button @click="isVisible = false" class="close-button">
                <i class="fa-solid fa-xmark"></i>
            </button>

            <div class="header">Registrér enhed</div>

            <div class="device-details">

                <!-- Name -->
                <div class="detail-item wide">
                    <span class="detail-label">Navn</span>
                    <span class="detail-value">
                        <div ref="nameEditable"
                             contenteditable="true"
                             class="edit-input"
                             @input="onNameInput"
                             @keydown.enter.prevent="">{{ nameEditableValue.value ?? device.name }}</div>
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
                <div class="detail-item wide">
                    <span class="detail-label">EUI</span>
                    <span class="detail-value">
                        <div
                            ref="euiEditable"
                            contenteditable="true"
                            class="edit-input"
                            @input="onEuiInput"
                            @keydown.enter.prevent=""
                        >{{ euiEditableValue.value ?? device.deviceEUI }}</div>
                    </span>
                </div>

                <!-- AppKey -->
                <div class="detail-item wide">
                    <span class="detail-label">AppKey</span>
                    <span class="detail-value">
                        <div
                            ref="appKeyEditable"
                            contenteditable="true"
                            class="edit-input"
                            @input="onAppKeyInput"
                            @keydown.enter.prevent=""
                        >{{ appKeyEditableValue.value ?? device.OTAAapplicationKey }}</div>
                    </span>
                </div>

                <div class="separator margin"></div>

                <!-- Location -->
                <div class="detail-item wide">
                    <span class="detail-label">Lokation</span>
                    <span class="detail-value">
                        <div
                            ref="locationEditable"
                            contenteditable="true"
                            class="edit-input"
                            @input="onLocationInput"
                            @keydown.enter.prevent=""
                        >{{ locationEditableValue.value ?? device.commentOnLocation }}</div>
                    </span>
                </div>

                <!-- Comment -->
                <div class="detail-item wide">
                    <span class="detail-label">Kommentar</span>
                    <span class="detail-value">
                        <div
                            ref="commentEditable"
                            contenteditable="true"
                            class="edit-input"
                            @input="onCommentInput"
                            @keydown.enter.prevent=""
                        >{{ commentEditableValue.value ?? device.comment }}</div>
                    </span>
                </div>

            </div>

            <div class="button-wrapper">
                <button class="primary" style="margin-top: 1rem;" @click="isVisible = false">
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

</style>