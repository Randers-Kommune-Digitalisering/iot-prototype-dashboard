<script setup>
    const navItems = [
        { name: 'Enheder', link: '/devices', icon: 'fa-solid fa-microchip' },
        { name: 'Bygninger', link: '/buildings', icon: 'fa-solid fa-house-chimney' },
        { name: 'Indstillinger', link: '/settings', icon: 'fa-solid fa-cog' },
    ]
</script>

<template>
    <nav class="top-navbar">
        <!-- <div class="navbar-brand">
            <a class="navbar-item" href="#">
                <span>IoT</span>
            </a>
        </div> -->
        <div class="navbar-items">
            <template v-for="item in navItems" :key="item.name">
                <router-link
                    :to="item.link"
                    class="navbar-item"
                >
                    <i :class="item.icon"></i>
                    <span class="navbar-item-name">{{ item.name }}</span>
                </router-link>
            </template>
        </div>
    </nav>
</template>

<style scoped>
    .top-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 4.5rem;
        background-color: #2c3e50;
        color: rgb(110, 41, 41);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 0 1rem;
        z-index: 10;
    }
        .navbar-items {
            display: flex;
            height: 100%;
        }
        .navbar-items .navbar-item {
            font-size: 1.6rem;
            color: rgb(200, 200, 200);
            padding: 0rem 1.8rem;
            height: 100%;
            transition: background-color 0.15s;
            display: flex;
            align-items: center;
        }
        .navbar-items .navbar-item:hover, .navbar-items .navbar-item:focus {
            background-color: #314456;
            outline: 0;
        }
        .navbar-items .navbar-item.router-link-active {
            background-color: #243242;
            color:rgb(230, 230, 230);
        }
            .navbar-items .navbar-item i {
                margin-right: 1rem;
            }
            .navbar-items .navbar-item .navbar-item-name {
                font-size: 0.9rem;
                opacity: 0.8;
            }
            .navbar-items .navbar-item:hover .navbar-item-name,
            .navbar-items .navbar-item:focus .navbar-item-name,
            .navbar-items .navbar-item.router-link-active .navbar-item-name {
                opacity: 1;
            }
</style>