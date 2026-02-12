<script setup>
    import { ref } from 'vue'

    const navItems = ref([
        { name: 'Home', link: '/', submenu: [], collapsed: true },
        { name: 'Test', link: '#', submenu: [
            { name: 'Subitem 1', link: '/subitem1' },
            { name: 'Subitem 2', link: '/subitem2' },
        ], collapsed: true },
        { name: 'Dashboard', link: '/dashboard', submenu: [], collapsed: true },
        { name: 'Settings', link: '/settings', submenu: [], collapsed: true },
    ])

</script>

<template>
    <nav class="navbar fixed-navbar">

        <div class="navbar-brand">
            <a class="navbar-item" href="#">
                <span>I<span></span>oT</span>
            </a>
        </div>

        <div class="navbar-menu">
            <template v-for="item in navItems" :key="item.name">
                <router-link v-if="item.link != '#'"
                    :to="item.link"
                    class="navbar-item"
                >
                    {{ item.name }}
                </router-link>
                <span v-else class="navbar-item" @click="item.collapsed = !item.collapsed">
                    {{ item.name }}
                </span>
                <div v-if="item.submenu.length" :class="['navbar-submenu', item.collapsed ? 'collapsed' : '']">
                    <router-link
                        v-for="subitem in item.submenu"
                        :key="subitem.name"
                        :to="subitem.link"
                        class="navbar-item submenu-item"
                    >
                        {{ subitem.name }}
                    </router-link>
                </div>
            </template>
        </div>

    </nav>
</template>

<style scoped>
.fixed-navbar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 220px;
    background-color: #1b1c1b;
    padding: 0.8rem;
    display: flex;
    flex-direction: column;
    z-index: 1000;
    width: 12rem;
    overflow-x: hidden;
}
    .navbar-brand {
        margin-bottom: 1rem;
        text-align: center;
    }
    .navbar-brand .navbar-item {
        font-size: 1rem;
        font-weight: bold;
        text-align: center;
        transition: all 0.2s ease;
        background-color: transparent;
        color: #ffffff;
        font-size: 1.5rem;
    }
    .navbar-brand .navbar-item:hover {
        filter: drop-shadow(0 0 1rem rgba(177, 177, 177, 0.15));
    }



.navbar-menu {
    margin-top: 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    font-size: 0.9rem;
    gap: 0.05rem;
}
.navbar-menu .navbar-item {
    user-select: none;
    cursor: pointer;
    width: 100%;
    transition: background-color 0.2s ease, color 0.2s ease;
    text-align: left;
    border-radius: 0.3rem;
    text-decoration: none;
    padding: 0.25rem 0.5rem;
}
.navbar-menu > .navbar-item {
    color: #cccccc;
}
.navbar-menu .navbar-item:hover {
    color: #f2f2f2;
    background-color: #232423;
}

.navbar-submenu {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.05rem;
}
    .navbar-submenu.collapsed {
        display: none;
    }
    .submenu-item {
        font-size: 0.8em;
        color: gray;
        font-weight: 400;
        padding-left: 0.8rem !important;
    }
    /* .submenu-item:hover {
    } */
</style>