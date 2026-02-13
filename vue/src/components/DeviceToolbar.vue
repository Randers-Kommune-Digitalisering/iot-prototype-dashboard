<script setup>
    import { ref } from 'vue'
    const emit = defineEmits(['search-changed', 'view-changed'])
    const selectedView = ref('lokation')
    const searchQuery = ref('')
    const clearSearch = () => {
        searchQuery.value = ''
        emit('search-changed', searchQuery.value)
    }
</script>

<template>
    <div class="device-toolbar">

        <div class="device-view">
            <span>Visning</span>
            <label class="toggle-radio">
                <input type="radio" name="view" value="lokation" v-model="selectedView" @change="emit('view-changed', selectedView)" />
                <span :class="{ active: selectedView === 'lokation' }">Lokation</span>
            </label>
            <label class="toggle-radio">
                <input type="radio" name="view" value="model" v-model="selectedView" @change="emit('view-changed', selectedView)" />
                <span :class="{ active: selectedView === 'model' }">Model</span>
            </label>
        </div>

        <div class="break"></div>
        
        <div class="device-search">
            Søg
            <input
                type="text"
                placeholder="Navn, model, lokation, EUI"
                class="device-search"
                v-model="searchQuery"
                @input="emit('search-changed', searchQuery)"
            />
            <button @click="clearSearch()" v-if="searchQuery">
                <i class="fa-solid fa-xmark"></i>
            </button>
        </div>

    </div>
</template>

<style scoped>
    .device-toolbar {
        position: fixed;
        top: 4.5rem;
        left: 0;
        right: 0;
        height: 3.5rem;
        background-color: rgb(28, 28, 28);
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 0 2rem;
        z-index: 10;
    }
    .break {
        height: 60%;
        width: 0.05rem;
        background-color: rgb(42, 42, 42);
    }
    .device-view {
        display: flex;
        align-items: center;
        gap: .5rem;
    }
        .toggle-radio {
            position: relative;
            display: inline-flex;
            align-items: center;
            cursor: pointer;
        }
        .toggle-radio input[type="radio"] {
            display: none;
        }
        .toggle-radio span {
            padding: 0 .6rem;
            height: 2.45rem;
            display: inline-flex;
            align-items: center;
            border-radius: 0.5rem;
            background: #222;
            color: #fff;
            border: 1px solid #444;
            transition: background 0.2s, color 0.2s, border 0.2s;
            font-size: 1rem;
            user-select: none;
            box-sizing: border-box;
        }
        .toggle-radio span.active {
            background: #fff;
            color: #222;
            border: 1px solid #fff;
        }
        .toggle-radio span:not(.active):hover {
            border-color: #5d5d5d !important;
            background-color: #262626;
        }
    .device-search {
        display: flex;
        align-items: center;
        gap: .5rem;
    }
    .device-search input {
        padding: 0 .6rem;
        height: 2.45rem;
        border-radius: 0.5rem;
        background: #222;
        color: #fff;
        border: 1px solid #444;
        transition: background 0.2s, color 0.2s, border 0.2s;
        font-size: 1rem;
        box-sizing: border-box;
    }

    button {
        border-radius: 50%;
        width: 2.2rem;
        height: 2.2rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #444;
        padding: 0;
    }
</style>