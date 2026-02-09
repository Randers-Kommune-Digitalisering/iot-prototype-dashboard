<script setup>
import { ref } from 'vue'
const emit = defineEmits(['search-changed', 'view-changed'])
const selectedView = ref('enhedstype')
const searchQuery = ref('')
</script>

<template>
    <div class="device-toolbar">

        <div class="device-view">
            <span>Visning</span>
            <label class="toggle-radio">
                <input type="radio" name="view" value="enhedstype" v-model="selectedView" @change="emit('view-changed', selectedView)" />
                <span :class="{ active: selectedView === 'enhedstype' }">Enhedstype</span>
            </label>
            <label class="toggle-radio">
                <input type="radio" name="view" value="lokation" v-model="selectedView" @change="emit('view-changed', selectedView)" />
                <span :class="{ active: selectedView === 'lokation' }">Lokation</span>
            </label>
        </div>

        <div class="break"></div>
        
        <div class="device-search">
            Søg
            <input
                type="text"
                placeholder="Søg enhed..."
                class="device-search"
                v-model="searchQuery"
                @input="emit('search-changed', searchQuery)"
            />
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
        margin-left: 1rem;
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
</style>