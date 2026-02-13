import { createRouter, createWebHistory } from 'vue-router'
import Devices from '@/views/Devices.vue'

const routes = [
	{
		path: '/',
		redirect: '/devices'
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
})

export default router
