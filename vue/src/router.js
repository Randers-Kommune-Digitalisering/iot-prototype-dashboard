import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/Home.vue';
import Devices from '@/views/Devices.vue';

const routes = [
{
	path: '/',
	name: 'Home',
	component: Home
},
{
	path: '/devices',
	name: 'Devices',
	component: Devices
}
];

const router = createRouter({
	history: createWebHistory(),
	routes
});

export default router;
